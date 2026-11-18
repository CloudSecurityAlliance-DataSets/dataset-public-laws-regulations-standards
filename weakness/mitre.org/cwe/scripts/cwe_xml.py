"""Load and verify a MITRE CWE XML edition, index its entries and compute views.

Python 3.10+ standard library only. Element access is by local name so the
same code reads schema 7 (namespace cwe-7, Categories) and schema 8
(namespace cwe-8, Groupings).
"""

from __future__ import annotations

import hashlib
import io
import json
import re
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Callable
from xml.etree import ElementTree as ET
from xml.etree.ElementTree import Element


class SourceVerificationError(ValueError):
    """The edition's zip or XML does not match its committed sidecar/version,
    or the catalog cannot be read as one (e.g. no schema version in its namespace)."""


class DuplicateIdError(SourceVerificationError):
    """Two catalog entries share a CWE ID, or two External_Reference entries share a
    Reference_ID; indexing them by ID would silently keep only one."""


class DanglingReferenceError(ValueError):
    """A view names a CWE ID that is absent from the catalog."""


def local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def child(elem: Element | None, name: str) -> Element | None:
    if elem is None:
        return None
    for c in elem:
        if local(c.tag) == name:
            return c
    return None


def children(elem: Element | None, name: str) -> list[Element]:
    if elem is None:
        return []
    return [c for c in elem if local(c.tag) == name]


def text(elem: Element | None) -> str:
    if elem is None or elem.text is None:
        return ""
    return elem.text.strip()


@dataclass(frozen=True)
class Edition:
    version: str
    date: str
    schema_major: int
    edition_dir: Path
    zip_name: str
    sha256: str
    weaknesses: dict[int, Element]
    groups: dict[int, Element]
    views: dict[int, Element]
    references: dict[str, Element]
    group_term: str
    group_dir: str


def load_edition(edition_dir: Path, version: str) -> Edition:
    edition_dir = Path(edition_dir)
    zip_name = f"cwec_v{version}.xml.zip"
    zip_path = edition_dir / zip_name
    sidecar_path = edition_dir / f"{zip_name}-file-metadata.json"
    try:
        sidecar = json.loads(sidecar_path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise SourceVerificationError(f"cannot read sidecar {sidecar_path}: {exc}")
    expected = sidecar.get("sha256")
    if not expected:
        raise SourceVerificationError(f"sidecar {sidecar_path} has no sha256")
    try:
        data = zip_path.read_bytes()
    except OSError as exc:
        raise SourceVerificationError(f"cannot read {zip_path}: {exc}")
    actual = hashlib.sha256(data).hexdigest()
    if actual != expected:
        raise SourceVerificationError(
            f"{zip_name}: sha256 {actual} does not match sidecar {expected}"
        )
    with zipfile.ZipFile(io.BytesIO(data)) as zf:
        names = [n for n in zf.namelist() if not n.endswith("/")]
        if len(names) != 1:
            raise SourceVerificationError(
                f"{zip_name}: expected one member, found {names}"
            )
        root = ET.fromstring(zf.read(names[0]))
    if local(root.tag) != "Weakness_Catalog":
        raise SourceVerificationError(f"{zip_name}: root is {local(root.tag)}")
    if root.get("Version") != version:
        raise SourceVerificationError(
            f"{zip_name}: catalog Version {root.get('Version')!r} != {version!r}"
        )
    ns = root.tag[1 : root.tag.index("}")] if root.tag.startswith("{") else ""
    # MITRE's namespace ends in cwe-<major> (cwe-7, cwe-8); take the leading
    # integer so a future cwe-8.1 still reads as schema 8.
    m = re.match(r"cwe-(\d+)", ns.rsplit("/", 1)[-1])
    if m is None:
        raise SourceVerificationError(
            f"{zip_name}: cannot read the schema major version from namespace {ns!r}"
            " (expected one ending in cwe-<number>)"
        )
    schema_major = int(m.group(1))

    def by_id(container: str, item: str) -> dict[int, Element]:
        out: dict[int, Element] = {}
        for e in children(child(root, container), item):
            i = int(e.get("ID"))
            if i in out:
                raise DuplicateIdError(f"{zip_name}: two {item} entries have ID {i} (CWE-{i})")
            out[i] = e
        return out

    weaknesses = by_id("Weaknesses", "Weakness")
    views = by_id("Views", "View")
    if child(root, "Groupings") is not None:
        group_term, group_dir = "Grouping", "groupings"
        groups = by_id("Groupings", "Grouping")
    else:
        group_term, group_dir = "Category", "categories"
        groups = by_id("Categories", "Category")
    seen: dict[int, str] = {}
    for kind, table in (("Weakness", weaknesses), (group_term, groups), ("View", views)):
        for i in table:
            if i in seen:
                raise DuplicateIdError(f"{zip_name}: CWE-{i} is both a {seen[i]} and a {kind}")
            seen[i] = kind
    references: dict[str, Element] = {}
    for e in children(child(root, "External_References"), "External_Reference"):
        rid = e.get("Reference_ID")
        if rid in references:
            raise DuplicateIdError(
                f"{zip_name}: two External_Reference entries have Reference_ID {rid}"
            )
        references[rid] = e
    return Edition(
        version=version,
        date=root.get("Date", ""),
        schema_major=schema_major,
        edition_dir=edition_dir,
        zip_name=zip_name,
        sha256=actual,
        weaknesses=weaknesses,
        groups=groups,
        views=views,
        references=references,
        group_term=group_term,
        group_dir=group_dir,
    )


def entry_kind(ed: Edition, cwe_id: int) -> str | None:
    if cwe_id in ed.weaknesses:
        return "weakness"
    if cwe_id in ed.groups:
        return ed.group_term.lower()
    if cwe_id in ed.views:
        return "view"
    return None


def _entry(ed: Edition, cwe_id: int) -> Element | None:
    for table in (ed.weaknesses, ed.groups, ed.views):
        if cwe_id in table:
            return table[cwe_id]
    return None


def entry_name(ed: Edition, cwe_id: int) -> str | None:
    e = _entry(ed, cwe_id)
    return None if e is None else e.get("Name")


_DIRS = {"weakness": "weaknesses", "view": "views"}


def entry_path(ed: Edition, cwe_id: int) -> str | None:
    kind = entry_kind(ed, cwe_id)
    if kind is None:
        return None
    folder = ed.group_dir if kind == ed.group_term.lower() else _DIRS[kind]
    return f"{folder}/CWE-{cwe_id}.md"


# ---------------------------------------------------------------- outlines


@dataclass(frozen=True)
class OutlineNode:
    cwe_id: int
    expanded: bool
    children: tuple["OutlineNode", ...] = ()


def explicit_members(ed: Edition, view_id: int) -> list[int]:
    members = child(ed.views[view_id], "Members")
    out: list[int] = []
    for m in children(members, "Has_Member"):
        i = int(m.get("CWE_ID"))
        if i not in out:
            out.append(i)
    return out


def _view_edges(ed: Edition, view_id: int):
    """Return (children_of, primary_parents) for the view's graph."""
    kids: dict[int, set[int]] = {}
    primary: dict[int, set[int]] = {}
    vid = str(view_id)
    for gid, g in ed.groups.items():
        for hm in children(child(g, "Relationships"), "Has_Member"):
            if hm.get("View_ID") == vid:
                kids.setdefault(gid, set()).add(int(hm.get("CWE_ID")))
    for wid, w in ed.weaknesses.items():
        for rw in children(child(w, "Related_Weaknesses"), "Related_Weakness"):
            if rw.get("Nature") == "ChildOf" and rw.get("View_ID") == vid:
                p = int(rw.get("CWE_ID"))
                kids.setdefault(p, set()).add(wid)
                if rw.get("Ordinal") == "Primary":
                    primary.setdefault(wid, set()).add(p)
    return kids, primary


def _view_graph(ed: Edition, view_id: int):
    roots = explicit_members(ed, view_id)
    kids, primary = _view_edges(ed, view_id)
    for i in [*roots, *kids, *(c for cs in kids.values() for c in cs)]:
        if entry_kind(ed, i) is None:
            raise DanglingReferenceError(
                f"view {view_id} names CWE-{i}, which is not in the catalog"
            )
    kids = {p: sorted(cs) for p, cs in kids.items()}
    reachable: set[int] = set()
    parents: dict[int, set[int]] = {}
    stack = list(roots)
    while stack:
        n = stack.pop()
        if n in reachable:
            continue
        reachable.add(n)
        for c in kids.get(n, ()):
            parents.setdefault(c, set()).add(n)
            stack.append(c)
    return roots, kids, primary, reachable, parents


def unreachable_in_view(ed: Edition, view_id: int) -> list[int]:
    """Entries that have a parent edge in the view but are not reachable from
    its roots (e.g. children of a deprecated weakness that is itself outside
    the hierarchy). They are absent from `view_outline`."""
    _, kids, _, reachable, _ = _view_graph(ed, view_id)
    listed = {c for cs in kids.values() for c in cs}
    return sorted(listed - reachable)


def view_outline(ed: Edition, view_id: int) -> tuple[OutlineNode, ...]:
    roots, kids, primary, reachable, parents = _view_graph(ed, view_id)
    root_set = set(roots)
    chosen: dict[int, int] = {}
    for x, ps in parents.items():
        if x in root_set:
            continue
        prim = ps & primary.get(x, set())
        chosen[x] = min(prim) if prim else min(ps)

    def build_tree() -> tuple[list[OutlineNode], set[int]]:
        expanded: set[int] = set()

        def build(n: int) -> OutlineNode:
            expanded.add(n)
            out = []
            for c in kids.get(n, ()):
                if c in expanded or c in root_set or chosen.get(c) != n:
                    out.append(OutlineNode(c, False))
                else:
                    out.append(build(c))
            return OutlineNode(n, True, tuple(out))

        return [build(r) for r in roots if r not in expanded], expanded

    tree, expanded = build_tree()
    # Entries whose chosen-parent chain never reaches a root (a cycle) are
    # re-parented under a parent that is already expanded, so each entry is
    # still expanded exactly once.
    while reachable - expanded:
        missing = min(
            x for x in reachable - expanded if parents[x] & expanded
        )
        chosen[missing] = min(parents[missing] & expanded)
        tree, expanded = build_tree()
    return tuple(tree)


# ---------------------------------------------------------- implicit views


def _all_entries(ed: Edition) -> dict[int, Element]:
    out: dict[int, Element] = {}
    out.update(ed.weaknesses)
    out.update(ed.groups)
    out.update(ed.views)
    return out


def _weak(pred: Callable[[Element], bool]) -> Callable[[Edition], list[int]]:
    return lambda ed: sorted(i for i, w in ed.weaknesses.items() if pred(w))


def _vals(w: Element, path: tuple[str, ...], attr: str | None = None) -> list[str]:
    nodes = [w]
    for name in path:
        nodes = [c for n in nodes for c in children(n, name)]
    return [n.get(attr) if attr else text(n) for n in nodes]


def _lang(name: str):
    return _weak(lambda w: name in _vals(w, ("Applicable_Platforms", "Language"), "Name"))


def _phase(name: str):
    return _weak(
        lambda w: name in _vals(w, ("Modes_Of_Introduction", "Introduction", "Phase"))
    )


def _not_deprecated(w: Element) -> bool:
    return w.get("Status") != "Deprecated"


def _has_maintenance_note(e: Element) -> bool:
    return "Maintenance" in _vals(e, ("Notes", "Note"), "Type")


IMPLICIT_FILTERS: dict[str, Callable[[Edition], list[int]]] = {
    "/Weakness_Catalog/Weaknesses/Weakness[Weakness_Ordinalities/Weakness_Ordinality/Ordinality='Indirect']": _weak(
        lambda w: "Indirect"
        in _vals(w, ("Weakness_Ordinalities", "Weakness_Ordinality", "Ordinality"))
    ),
    "/Weakness_Catalog/*/*[Notes/Note[@Type='Maintenance']]": lambda ed: sorted(
        i for i, e in _all_entries(ed).items() if _has_maintenance_note(e)
    ),
    "/Weakness_Catalog/Weaknesses/Weakness[./Taxonomy_Mappings/Taxonomy_Mapping/@Taxonomy_Name='ISA/IEC 62443']": _weak(
        lambda w: "ISA/IEC 62443"
        in _vals(w, ("Taxonomy_Mappings", "Taxonomy_Mapping"), "Taxonomy_Name")
    ),
    "/Weakness_Catalog/*[not(self::External_References)]/*": lambda ed: sorted(
        _all_entries(ed)
    ),
    "/Weakness_Catalog/*/*[@Status='Deprecated']": lambda ed: sorted(
        i for i, e in _all_entries(ed).items() if e.get("Status") == "Deprecated"
    ),
    "/Weakness_Catalog/Weaknesses/Weakness[./Applicable_Platforms/Language/@Name='C']": _lang("C"),
    "/Weakness_Catalog/Weaknesses/Weakness[./Applicable_Platforms/Language/@Name='C++']": _lang("C++"),
    "/Weakness_Catalog/Weaknesses/Weakness[./Applicable_Platforms/Language/@Name='Java']": _lang("Java"),
    "/Weakness_Catalog/Weaknesses/Weakness[./Applicable_Platforms/Language/@Name='PHP']": _lang("PHP"),
    "/Weakness_Catalog/Weaknesses/Weakness[@Abstraction='Base'][not(@Status='Deprecated')]": _weak(
        lambda w: w.get("Abstraction") == "Base" and _not_deprecated(w)
    ),
    "/Weakness_Catalog/Weaknesses/Weakness[@Structure='Composite'][not(@Status='Deprecated')]": _weak(
        lambda w: w.get("Structure") == "Composite" and _not_deprecated(w)
    ),
    "/Weakness_Catalog/Weaknesses/Weakness[(@Abstraction='Base') or (@Abstraction='Class')][./Modes_Of_Introduction/Introduction/Phase='Architecture and Design']": _weak(
        lambda w: w.get("Abstraction") in ("Base", "Class")
        and "Architecture and Design"
        in _vals(w, ("Modes_Of_Introduction", "Introduction", "Phase"))
    ),
    "/Weakness_Catalog/Weaknesses/Weakness[./Modes_Of_Introduction/Introduction/Phase='Implementation']": _phase("Implementation"),
    "/Weakness_Catalog/Weaknesses/Weakness[@Structure='Chain']": _weak(
        lambda w: w.get("Structure") == "Chain"
    ),
    "/Weakness_Catalog/Weaknesses/Weakness[./Applicable_Platforms/Technology/@Class='Mobile']": _weak(
        lambda w: "Mobile"
        in _vals(w, ("Applicable_Platforms", "Technology"), "Class")
    ),
}


def implicit_members(ed: Edition, view_id: int) -> list[int] | None:
    flt = text(child(ed.views[view_id], "Filter"))
    fn = IMPLICIT_FILTERS.get(flt)
    return None if fn is None else fn(ed)
