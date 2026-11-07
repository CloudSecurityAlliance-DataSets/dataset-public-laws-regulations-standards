#!/usr/bin/env python3
"""Batch 1A: Extract and structure all remaining on-disk Markdown-only, raw PDF/text,
CSV-only, and JSON-only dataset editions across dataset-public-laws-regulations-standards
and dataset-private-laws-regulations-standards.
"""
import csv
import json
import re
import subprocess
import sys
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

UTILS_DIR = Path(__file__).resolve().parent
PUB_ROOT = UTILS_DIR.parent.parent
PRIV_ROOT = PUB_ROOT.parent / "dataset-private-laws-regulations-standards"

sys.path.insert(0, str(UTILS_DIR))
from extract_track2_corpus import pdf_bytes_to_markdown
from extract_track2_wave2 import ensure_hierarchical_headings
from parse_regulatory_sections import HEADING_RE

PARSE_SCRIPT = UTILS_DIR / "parse_regulatory_sections.py"


def run_parse_sections(doc_dir: Path, stem: str) -> int:
    """Run parse_regulatory_sections.py on doc_dir and return row count."""
    subprocess.run(
        [sys.executable, str(PARSE_SCRIPT), str(doc_dir), "--out-stem", stem],
        check=True,
        capture_output=True,
        text=True,
    )
    jpath = doc_dir / f"{stem}-sections.json"
    if jpath.exists():
        return len(json.loads(jpath.read_text(encoding="utf-8")))
    return 0


def write_dict_list_to_csv(rows: list[dict], csv_path: Path) -> None:
    """Write a list of dicts to CSV preserving key order across all rows."""
    if not rows:
        return
    fieldnames: list[str] = []
    seen: set[str] = set()
    for r in rows:
        if isinstance(r, dict):
            for k in r.keys():
                if k not in seen:
                    seen.add(k)
                    fieldnames.append(k)
    flat_rows = []
    for r in rows:
        if not isinstance(r, dict):
            continue
        fr = {}
        for k in fieldnames:
            v = r.get(k, "")
            if isinstance(v, (dict, list)):
                s_val = json.dumps(v, ensure_ascii=False)
            elif v is None:
                s_val = ""
            else:
                s_val = str(v)
            s_val = "\n".join(l.rstrip() for l in s_val.replace("\r\n", "\n").replace("\r", "\n").splitlines()).strip()
            fr[k] = s_val
        flat_rows.append(fr)
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, quoting=csv.QUOTE_ALL, lineterminator="\n")
        w.writeheader()
        w.writerows(flat_rows)


def process_private_json_no_csv() -> int:
    """Generate <stem>-controls.csv for the 10 JSON-only control editions in dataset-private."""
    count = 0
    for mp in sorted(PRIV_ROOT.rglob("*-metadata.json")):
        parent = mp.parent
        files = [
            f.name
            for f in parent.iterdir()
            if f.is_file()
            and f.name != "README.md"
            and not f.name.startswith(".")
            and not f.name.endswith(("-metadata.json", "-metadata.md", "_meta.json"))
        ]
        jsons = [f for f in files if f.endswith("-controls.json")]
        csvs = [f for f in files if f.endswith(".csv")]
        if jsons and not csvs:
            jpath = parent / jsons[0]
            data = json.loads(jpath.read_text(encoding="utf-8"))
            rows = data.get("controls", []) if isinstance(data, dict) else data
            if isinstance(rows, list) and rows:
                cpath = parent / jsons[0].replace("-controls.json", "-controls.csv")
                write_dict_list_to_csv(rows, cpath)
                count += 1
                print(f"[PRIVATE json->csv] {cpath.relative_to(PRIV_ROOT)} ({len(rows)} rows)")
    return count


def process_public_json_no_csv() -> int:
    """Generate companion CSVs for the 9 JSON-only editions in dataset-public."""
    count = 0
    targets = [
        ("control/cloudsecurityalliance.org/aicm/1.0.3", "aicm-1.0.3.json", "controls", "aicm-1.0.3-controls.csv"),
        ("control/cloudsecurityalliance.org/aicm-caiq/1.0.2", "aicm-caiq-1.0.2.json", "questions", "aicm-caiq-1.0.2-questions.csv"),
        ("control/cloudsecurityalliance.org/ccm/4.0.13", "ccm-4.0.13-Controls.json", None, "ccm-4.0.13-controls.csv"),
        ("control/cloudsecurityalliance.org/ccm/4.1.0", "ccm-4.1.0.json", "controls", "ccm-4.1.0-controls.csv"),
        ("control/cloudsecurityalliance.org/ccm-caiq/3.1", "ccm-caiq-3.1.json", "questions", "ccm-caiq-3.1-questions.csv"),
        ("control/cloudsecurityalliance.org/ccm-caiq/4.1.0", "ccm-caiq-4.1.0.json", "questions", "ccm-caiq-4.1.0-questions.csv"),
        ("reference/mitre.org/ctid/cve", "cve-10.21.2021_attack-9.0-enterprise.json", "mapping_objects", "ctid-cve-mapping.csv"),
        ("reference/mitre.org/cve-program/cna-partners", "cve-cna-partners-list.json", "partners", "cve-cna-partners-list.csv"),
        ("ttp/mitre.org/fight", "fight.json", "techniques", "fight-techniques.csv"),
    ]
    for rel, jfn, key, cfn in targets:
        d = PUB_ROOT / rel
        jpath = d / jfn
        if not jpath.exists():
            continue
        data = json.loads(jpath.read_text(encoding="utf-8"))
        rows = data.get(key, []) if key and isinstance(data, dict) else data
        if isinstance(rows, list) and rows:
            cpath = d / cfn
            write_dict_list_to_csv(rows, cpath)
            count += 1
            print(f"[PUBLIC json->csv] {cpath.relative_to(PUB_ROOT)} ({len(rows)} rows)")
    return count


def disambiguate_csv_headers(raw_headers: list[str]) -> list[tuple[str, bool]]:
    """Return list of (col_name, is_empty_header) preserving every CSV column without collision.
    For repeated 'Gap Level' / 'Addendum' columns following a '<Framework> Control Mapping' column,
    prefixes the column name with the framework prefix so each framework's gap assessment is preserved.
    """
    result: list[tuple[str, bool]] = []
    seen_counts: dict[str, int] = {}
    used_names: set[str] = set()
    last_mapping_fw = ""
    for i, raw_h in enumerate(raw_headers):
        h = (raw_h or "").strip()
        if not h:
            col_name = f"_col_{i + 1}"
            while col_name in used_names:
                i += 1
                col_name = f"_col_{i + 1}"
            used_names.add(col_name)
            result.append((col_name, True))
            continue
        if h.endswith("Control Mapping"):
            last_mapping_fw = h[: -len("Control Mapping")].strip()
            col_name = h
        elif h in (
            "Scope Applicability (Mappings)_Gap Level",
            "Scope Applicability (Mappings)_Addendum",
            "Gap Level",
            "Addendum",
        ) and last_mapping_fw:
            suffix = "Gap Level" if h.endswith("Gap Level") else "Addendum"
            col_name = f"{last_mapping_fw} {suffix}"
        else:
            col_name = h
        base_name = col_name
        if col_name in used_names:
            idx = seen_counts.get(base_name, 1) + 1
            while f"{base_name}_{idx}" in used_names:
                idx += 1
            seen_counts[base_name] = idx
            col_name = f"{base_name}_{idx}"
        else:
            seen_counts[base_name] = 1
        used_names.add(col_name)
        result.append((col_name, False))
    return result


def process_public_csv_no_json() -> int:
    """Generate companion JSON files for the 18 CSV-only editions in dataset-public."""
    count = 0
    for mp in sorted(PUB_ROOT.rglob("*-metadata.json")):
        parent = mp.parent
        files = [
            f.name
            for f in parent.iterdir()
            if f.is_file()
            and f.name != "README.md"
            and not f.name.startswith(".")
            and not f.name.endswith(("-metadata.json", "-metadata.md", "_meta.json"))
        ]
        stem = mp.name[: -len("-metadata.json")]
        jsons = [f for f in files if f.endswith(".json") and f not in ("README.json", f"{stem}-items.json")]
        csvs = sorted(f for f in files if f.endswith(".csv") and not f.endswith("-sections.csv"))
        if csvs and (not jsons or f"{stem}-items.json" in files):
            all_rows = []
            for cfn in csvs:
                cpath = parent / cfn
                sheet_name = cfn[:-4]
                with cpath.open("r", encoding="utf-8", errors="replace") as f:
                    reader = csv.reader(f)
                    raw_headers = next(reader, [])
                    if not raw_headers:
                        continue
                    col_specs = disambiguate_csv_headers(raw_headers)
                    for raw_row in reader:
                        cleaned: dict[str, str] = {}
                        for idx, val in enumerate(raw_row):
                            sval = (val or "").strip()
                            if idx < len(col_specs):
                                col_name, is_empty_hdr = col_specs[idx]
                            else:
                                col_name, is_empty_hdr = f"_col_{idx + 1}", True
                            if is_empty_hdr and not sval:
                                continue
                            cleaned[col_name] = sval
                        if any(cleaned.values()):
                            if len(csvs) > 1:
                                cleaned["_sheet"] = sheet_name
                            all_rows.append(cleaned)
            jpath = parent / f"{stem}-items.json"
            jpath.write_text(json.dumps(all_rows, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
            count += 1
            print(f"[PUBLIC csv->json] {jpath.relative_to(PUB_ROOT)} ({len(all_rows)} rows from {len(csvs)} CSVs)")
    return count


def promote_japanese_txt_headings(txt: str, doc_title: str) -> str:
    """Convert raw Japanese/English text files into clean Markdown with hierarchical headings."""
    lines = txt.splitlines()
    out = [f"# {doc_title}", ""]
    for line in lines:
        s = line.strip()
        if not s:
            out.append("")
            continue
        # Chapter / Part / Article in Japanese
        if re.match(r"^第[一二三四五六七八九十百千0-9０-９]+[章篇编部編]?(?:[\s　]|$)", s) and len(s) < 90:
            out.append(f"## {s}")
        elif re.match(r"^第[一二三四五六七八九十百千0-9０-９]+[节節](?:[\s　]|$)", s):
            out.append(f"### {s}")
        elif re.match(r"^第[一二三四五六七八九十百千0-9０-９]+[条條](?:の[一二三四五六七八九十0-9０-９]+)?(?:[\s　（\(]|$)", s):
            out.append(f"#### {s}")
        elif re.match(r"^[（\(][一二三四五六七八九十0-9０-９]+[）\)]\s*[^。]{2,70}$", s):
            out.append(f"### {s}")
        elif re.match(r"^(?:Chapter|Part|Section|CHAPTER|PART|SECTION)\s+(?:[IVXLCDM]+|\d+)\b", s) and len(s) < 120:
            out.append(f"## {s}")
        elif re.match(r"^(?:\d{1,2}\.\d{1,2}(?:\.\d{1,2})?)\s+[A-Z\u3000-\u9fff]", s) and len(s) < 120 and ".." not in s:
            depth = 2 + min(s.split()[0].rstrip(".").count("."), 2)
            out.append(f"{'#' * depth} {s}")
        elif re.match(r"^(?:[1-9]|1\d)[\.．]\s+[^\d\.]{2,80}$", s) and ".." not in s:
            out.append(f"## {s}")
        else:
            out.append(line)
    return "\n".join(out) + "\n"


def extract_cryptrec_ciphers_list(ciphers_dir: Path) -> str:
    """Extract CRYPTREC Ciphers List PDF tables and accompanying notes into structured Markdown
    preserving every table row, category, subcategory, algorithm name, parameter set, and note.
    """
    import pymupdf

    pdf_path = ciphers_dir / "ciphers-list.pdf"
    doc = pymupdf.open(pdf_path)

    def extract_3col_cipher_table(page_indices: list[int]) -> tuple[list[tuple[str, str, str]], dict[str, list[tuple[str, str]]]]:
        rows_out: list[tuple[str, str, str]] = []
        by_cat: dict[str, list[tuple[str, str]]] = {}
        cur_cat = ""
        cur_sub = ""
        for p_idx in page_indices:
            tabs = doc[p_idx].find_tables().tables
            if not tabs:
                continue
            for r in tabs[0].extract():
                c0 = " ".join((r[0] or "").split())
                c1 = " ".join((r[1] or "").split()) if len(r) > 1 else ""
                c2 = " ".join((r[2] or "").split()).replace("_ ", "").replace(" _", "").replace("v1 5", "v1_5") if len(r) > 2 else ""
                if c0 == "技術分類" or "次ページに続く" in c0:
                    continue
                if c0:
                    cur_cat = c0
                    cur_sub = c1
                elif c1:
                    cur_sub = c1
                if c2:
                    rows_out.append((cur_cat, cur_sub, c2))
                    by_cat.setdefault(cur_cat, []).append((cur_sub, c2))
        return rows_out, by_cat

    lines = [
        "# 電子政府における調達のために参照すべき暗号のリスト（CRYPTREC暗号リスト / CRYPTREC Ciphers List）",
        "",
        "CRYPTREC LS-0001-2022R2（令和５年３月30日 デジタル庁・総務省・経済産業省、最終更新：令和８年３月30日）",
        "",
        "## 1. 電子政府推奨暗号リスト (e-Government Recommended Ciphers List)",
        "",
        "暗号技術検討会（脚注１）及び関連委員会（以下「CRYPTREC」という。）により安全性（セキュリティ）及び実装性能が確認された暗号技術（脚注２）について、市場における利用実績が十分であるか今後の普及が見込まれると判断され、当該技術の利用を推奨するもののリスト。なお、利用する鍵長について、「暗号強度要件（アルゴリズム及び鍵長選択）に関する設定基準」（脚注３）の規定に合致しない鍵長を用いた場合には、電子政府推奨暗号リストの暗号技術を利用しているとは見なされないことに留意すること。",
        "",
        "- （脚注１）デジタル庁統括官、総務省サイバーセキュリティ統括官及び経済産業省商務情報政策局長が有識者の参集を求め、暗号技術の普及による情報セキュリティ対策の推進を図る観点から、専門家による意見等を聴取することにより、デジタル庁、総務省及び経済産業省における施策の検討に資することを目的として開催。",
        "- （脚注２）暗号利用モード、メッセージ認証コード、エンティティ認証は、他の技術分類の暗号技術と組み合わせて利用することとされているが、その場合、CRYPTREC暗号リストに掲載されたいずれかの暗号技術と組み合わせること。",
        "- （脚注３）CRYPTREC, 暗号強度要件（アルゴリズム及び鍵長選択）に関する設定基準, https://www.cryptrec.go.jp/list.html なお、当該設定基準の見直しの検討を行う予定であり、当面の間、表２（耐量子計算機暗号（PQC）リスト）の公開鍵暗号は、当該設定基準を適用しない。",
        "",
        "### 1.1 表１ 現行暗号リスト (Table 1: Current Ciphers List)",
        "",
        "| 技術分類（大分類） | 技術分類（小分類） | 暗号技術 |",
        "| --- | --- | --- |",
    ]
    t1_rows, t1_by_cat = extract_3col_cipher_table([0, 1])
    for cat, sub, alg in t1_rows:
        lines.append(f"| {cat} | {sub or '－'} | {alg} |")
    lines.extend([
        "",
        "- （注１）FIPS PUB 186-5では廃止されているが、本リスト掲載時から安全性・利用実績の状況に大きな変化がないため、掲載を継続する。",
        "- （注２）使用するMACはHMAC又はCMACに限る。",
        "- （注３）CRYPTREC暗号リストにおいて、64ビットブロック暗号により、同一の鍵を用いて暗号化する場合、2^20ブロックまで、同一の鍵を用いてCMACでメッセージ認証コードを生成する場合、2^21ブロックまでとする。",
        "- （注４）ハッシュ長は256ビット以上とすること。",
        "- （注５）ブロック暗号には、CRYPTREC暗号リスト掲載128ビットブロック暗号を使う。利用用途はストレージデバイスの暗号化に限り、実装方法はNIST SP800-38Eに従うこと。",
        "- （注６）CRYPTREC暗号リスト掲載のブロック暗号を、認証付き秘匿モードと組み合わせて、「認証暗号」として使うことができる。",
        "- （注７）初期化ベクトル長は96ビットを推奨する。",
        "",
    ])
    for idx_cat, (cat, items) in enumerate(t1_by_cat.items(), start=1):
        lines.append(f"#### 1.1.{idx_cat} {cat}")
        lines.append("")
        for sub, alg in items:
            lines.append(f"- **{alg}**" + (f"（{sub}）" if sub else ""))
        lines.append("")

    # Table 2: PQC list on page 3 (index 2)
    lines.extend([
        "### 1.2 表２ 耐量子計算機暗号（PQC）リスト (Table 2: Post-Quantum Cryptography List)",
        "",
        "現行暗号の解読に利用可能な水準の量子計算機（CRQC: Cryptographically Relevant Quantum Computer）への耐性を有することが確認された暗号技術のリスト。",
        "",
        "| 技術分類（大分類） | 技術分類（小分類） | 暗号技術（名称） | パラメーターセット（注８） |",
        "| --- | --- | --- | --- |",
    ])
    tabs_p3 = doc[2].find_tables().tables
    if tabs_p3:
        cur_cat = ""
        cur_sub = ""
        for r in tabs_p3[0].extract()[2:]:
            c0 = " ".join((r[0] or "").split())
            c1 = " ".join((r[1] or "").split())
            c2 = " ".join((r[2] or "").split())
            c3 = " ".join((r[3] or "").split())
            if c0:
                cur_cat = c0
                cur_sub = c1
            elif c1:
                cur_sub = c1
            lines.append(f"| {cur_cat} | {cur_sub or '－'} | {c2} | {c3} |")
    lines.extend([
        "",
        "- （注８）セキュリティのカテゴリを合わせて記載する。各カテゴリはNISTの“Submission Requirements and Evaluation Criteria for the Post-Quantum Cryptography Standardization Process”に従い、カテゴリ名の右に記載の鍵探索又は衝突探索と同程度以上の計算資源が攻撃に必要であることを意味する（Category 1: 128ビット鍵ブロック暗号、Category 2: 256ビットハッシュ関数、Category 3: 192ビット鍵ブロック暗号、Category 4: 384ビットハッシュ関数、Category 5: 256ビット鍵ブロック暗号）。 https://csrc.nist.gov/CSRC/media/Projects/Post-Quantum-Cryptography/documents/call-for-proposals-final-dec-2016.pdf （令和８年３月25日現在）",
        "- （脚注４）暗号技術の耐量子計算機暗号（PQC）リストへの追加について検討中である。 https://www.cryptrec.go.jp/report/cryptrec-mt-1501-2026.pdf",
        "",
        "## 2. 推奨候補暗号リスト (Candidate Recommended Ciphers List)",
        "",
        "CRYPTRECにより安全性及び実装性能が確認され、今後、電子政府推奨暗号リストに掲載される可能性のある暗号技術（脚注５）のリスト。なお、本リストに記載されている暗号技術を利用する際は、「暗号強度要件（アルゴリズム及び鍵長選択）に関する設定基準」（脚注６）の規定に合致する鍵長を用いることが求められることに留意すること。",
        "",
        "- （脚注５）暗号利用モード、メッセージ認証コード、エンティティ認証は、他の技術分類の暗号技術と組み合わせて利用することとされているが、その場合、CRYPTREC暗号リストに掲載されたいずれかの暗号技術と組み合わせること。",
        "- （脚注６）CRYPTREC, 暗号強度要件（アルゴリズム及び鍵長選択）に関する設定基準, https://www.cryptrec.go.jp/list.html",
        "",
        "| 技術分類（大分類） | 技術分類（小分類） | 暗号技術 |",
        "| --- | --- | --- |",
    ])
    t2_rows, t2_by_cat = extract_3col_cipher_table([3])
    for cat, sub, alg in t2_rows:
        lines.append(f"| {cat} | {sub or '－'} | {alg} |")
    lines.extend([
        "",
        "- （注９）KEM (Key Encapsulating Mechanism) – DEM (Data Encapsulating Mechanism) 構成における利用を前提とする。",
        "- （注10）CRYPTREC暗号リストにおいて、64ビットブロック暗号により、同一の鍵を用いて暗号化する場合、2^20ブロックまで、同一の鍵を用いてCMACでメッセージ認証コードを生成する場合、2^21ブロックまでとする。",
        "- （注11）平文サイズは64ビットの倍数に限る。",
        "- （注12）CRYPTREC暗号リスト掲載のブロック暗号を、認証付き秘匿モードと組み合わせて、「認証暗号」として使うことができる。",
        "",
    ])
    for idx_cat, (cat, items) in enumerate(t2_by_cat.items(), start=1):
        lines.append(f"### 2.{idx_cat} {cat}")
        lines.append("")
        for sub, alg in items:
            lines.append(f"- **{alg}**" + (f"（{sub}）" if sub else ""))
        lines.append("")

    lines.extend([
        "## 3. 運用監視暗号リスト (Monitored Ciphers List)",
        "",
        "実際に解読されるリスクが高まるなど、推奨すべき状態ではなくなったとCRYPTRECにより確認された暗号技術（脚注７）のうち、互換性維持（脚注８）のために継続利用を容認するもののリスト。互換性維持以外の目的での利用は推奨しない。なお、本リストに記載されている暗号技術を利用する際は、「暗号強度要件（アルゴリズム及び鍵長選択）に関する設定基準」（脚注９）の規定に合致する鍵長を用いることが求められることに留意すること。",
        "",
        "- （脚注７）暗号利用モード、メッセージ認証コード、エンティティ認証は、他の技術分類の暗号技術と組み合わせて利用することとされているが、その場合、CRYPTREC暗号リストに掲載されたいずれかの暗号技術と組み合わせること。",
        "- （脚注８）既に稼働中のシステムやアプリケーション等との間での相互運用を継続すること。",
        "- （脚注９）CRYPTREC, 暗号強度要件（アルゴリズム及び鍵長選択）に関する設定基準, https://www.cryptrec.go.jp/list.html",
        "",
        "| 技術分類（大分類） | 技術分類（小分類） | 暗号技術 |",
        "| --- | --- | --- |",
    ])
    t3_rows, t3_by_cat = extract_3col_cipher_table([4])
    for cat, sub, alg in t3_rows:
        lines.append(f"| {cat} | {sub or '－'} | {alg} |")
    lines.extend([
        "",
        "- （注13）TLS 1.0, 1.1, 1.2で利用実績があることから当面の利用を認める。",
        "- （注14）CRYPTREC暗号リストにおいて、64ビットブロック暗号により、同一の鍵を用いて暗号化する場合、2^20ブロックまで、同一の鍵を用いてCMACでメッセージ認証コードを生成する場合、2^21ブロックまでとする。",
        "- （注15）SP 800-67 Revision 2では廃止されているが、本リスト掲載時から安全性・利用実績の状況に大きな変化がないため、掲載を継続する。",
        "- （注16）CRYPTREC暗号リスト掲載のブロック暗号を、認証付き秘匿モードと組み合わせて、「認証暗号」として使うことができる。",
        "- （注17）安全性の観点から、メッセージ長を固定して利用すべきである。",
        "",
    ])
    for idx_cat, (cat, items) in enumerate(t3_by_cat.items(), start=1):
        lines.append(f"### 3.{idx_cat} {cat}")
        lines.append("")
        for sub, alg in items:
            lines.append(f"- **{alg}**" + (f"（{sub}）" if sub else ""))
        lines.append("")

    # Section 4: Revision history from pages 6-7 (indices 5, 6)
    lines.extend([
        "## 4. 更新履歴情報 (Revision History)",
        "",
        "| 更新日付 | 更新箇所 | 更新前の記述 | 更新後の記述 |",
        "| --- | --- | --- | --- |",
    ])
    merged_hist: list[list[str]] = []
    cur_date = ""
    for p_idx in (5, 6):
        tabs = doc[p_idx].find_tables().tables
        if not tabs:
            continue
        for r in tabs[0].extract():
            c0 = " ".join((r[0] or "").split())
            c1 = " ".join((r[1] or "").split())
            c2 = " ".join((r[2] or "").split()).replace("_ ", "").replace(" _", "")
            c3 = " ".join((r[3] or "").split()).replace("_ ", "").replace(" _", "")
            if c0 == "更新日付":
                continue
            if c0:
                cur_date = c0
            if c1:
                merged_hist.append([cur_date, c1, c2, c3])
            elif merged_hist:
                if c2:
                    merged_hist[-1][2] = (merged_hist[-1][2] + " " + c2).strip()
                if c3:
                    merged_hist[-1][3] = (merged_hist[-1][3] + " " + c3).strip()
    for d_str, loc_str, before_str, after_str in merged_hist:
        lines.append(f"| {d_str} | {loc_str} | {before_str or '－'} | {after_str or '－'} |")
    lines.append("")

    # Section 5: English overview & evaluation method from accompanying text files
    list_page_txt = ciphers_dir / "cryptrec-list-page.txt"
    method_txt = ciphers_dir / "cryptrec-method.txt"
    if list_page_txt.exists():
        lines.extend([
            "## 5. CRYPTREC Ciphers List Overview (English Reference)",
            "",
            list_page_txt.read_text(encoding="utf-8", errors="replace").strip(),
            "",
        ])
    if method_txt.exists():
        lines.extend([
            "## 6. Cryptographic Technique Evaluation in CRYPTREC",
            "",
            method_txt.read_text(encoding="utf-8", errors="replace").strip(),
            "",
        ])
    return "\n".join(lines) + "\n"


def extract_jc_star_requirements(jc_dir: Path) -> str:
    """Extract JC-STAR STAR-1 Conformance Requirements from jc-star-star1-requirements-raw.txt
    promoting Sections 1..3, all 16 Conformance Requirements [S1.1-01..S1.1-16], and Appendices A..B.
    """
    raw_txt = (jc_dir / "jc-star-star1-requirements-raw.txt").read_text(encoding="utf-8", errors="replace")
    out = [
        "# Japan Cyber-Security Technical Assessment Requirements (JC-STAR): STAR-1 Conformance Requirements and Assessment Methods",
        "",
        "JST-CR-01-01-2024R1 (December 2024, Information-technology Promotion Agency, Japan (IPA))",
        "",
    ]
    in_toc = False
    for line in raw_txt.splitlines():
        s = line.strip()
        if not s:
            out.append("")
            continue
        if re.match(r"^\d+\s*/\s*\d+$", s):
            continue
        if s == "Table of Contents":
            in_toc = True
            continue
        if in_toc:
            if re.match(r"^1\.\s+Introduction$", s):
                in_toc = False
            else:
                continue
        if re.match(r"^[123]\.\s+(?:Introduction|Concept of Conformance|STAR-1 Conformance Requirements)\b", s) and ".." not in s:
            out.append(f"## {s}")
        elif re.match(r"^[12]\.\d+\s+[A-Z]", s) and ".." not in s:
            out.append(f"### {s}")
        elif m_req := re.match(r"^\[STAR-1\s+Conformance\s+Requirement\s+(S\d+\.\d+-\d+)\]$", s, re.I):
            req_id = m_req.group(1).upper()
            out.append(f"### {req_id}: STAR-1 Conformance Requirement {req_id}")
        elif re.match(r"^Appendix\s+[AB]\b", s) and ".." not in s:
            out.append(f"## {s}")
        else:
            out.append(line)
    return "\n".join(out) + "\n"


def process_raw_on_disk() -> int:
    """Extract and structure the 28 Japanese raw PDF/text directories and 2 parent reference dirs."""
    count = 0
    # First handle reference/cisa.gov/govcar and reference/mitre.org/cve-program
    for rel in ["reference/cisa.gov/govcar", "reference/mitre.org/cve-program"]:
        d = PUB_ROOT / rel
        mp = next(d.glob("*-metadata.json"))
        stem = mp.name[: -len("-metadata.json")]
        child_mds = sorted(
            p
            for p in d.rglob("*.md")
            if p.parent != d and p.name != "README.md" and not p.name.endswith("-metadata.md")
        )
        if child_mds:
            parts = []
            for cmd in child_mds:
                parts.append(f"## {cmd.stem.replace('_', ' ')}\n\n" + cmd.read_text(encoding="utf-8", errors="replace"))
            md_path = d / f"{stem}.md"
            md_path.write_text("\n\n".join(parts) + "\n", encoding="utf-8")
            nrows = run_parse_sections(d, stem)
            count += 1
            print(f"[PARENT stitched] {rel} -> {nrows} sections")

    # Dedicated table-preserving extractors for CRYPTREC ciphers-list and IPA JC-STAR
    ciphers_dir = PUB_ROOT / "control/cryptrec.go.jp/ciphers-list"
    if ciphers_dir.exists():
        md_text = extract_cryptrec_ciphers_list(ciphers_dir)
        (ciphers_dir / "ciphers-list.md").write_text(md_text, encoding="utf-8")
        nrows = run_parse_sections(ciphers_dir, "ciphers-list")
        count += 1
        print(f"[CRYPTREC TABLE->MD+SECTIONS] control/cryptrec.go.jp/ciphers-list -> {nrows} sections")

    jc_dir = PUB_ROOT / "control/ipa.go.jp/jc-star"
    if jc_dir.exists():
        md_text = extract_jc_star_requirements(jc_dir)
        (jc_dir / "jc-star-star1-requirements.md").write_text(md_text, encoding="utf-8")
        nrows = run_parse_sections(jc_dir, "jc-star-star1-requirements")
        count += 1
        print(f"[JC-STAR->MD+SECTIONS] control/ipa.go.jp/jc-star -> {nrows} sections")

    # Now handle the remaining raw PDF/text directories
    for mp in sorted(PUB_ROOT.rglob("*-metadata.json")):
        parent = mp.parent
        if parent in (ciphers_dir, jc_dir):
            continue
        files = [
            f.name
            for f in parent.iterdir()
            if f.is_file()
            and f.name != "README.md"
            and not f.name.startswith(".")
            and not f.name.endswith(("-metadata.json", "-metadata.md", "_meta.json"))
        ]
        jsons = [f for f in files if f.endswith(".json") and f != "README.json"]
        csvs = [f for f in files if f.endswith(".csv")]
        mds = [f for f in files if f.endswith(".md")]
        pdfs = sorted(f for f in files if f.endswith(".pdf"))
        txts = sorted(f for f in files if f.endswith(".txt"))
        if jsons or csvs or mds or (not pdfs and not txts):
            continue
        stem = mp.name[: -len("-metadata.json")]
        md_meta = json.loads(mp.read_text(encoding="utf-8"))
        doc_title = md_meta.get("name") or stem

        md_text = ""
        if pdfs:
            raw_md, _ = pdf_bytes_to_markdown((parent / pdfs[0]).read_bytes(), doc_title)
            md_text = ensure_hierarchical_headings(raw_md, doc_title, "")
        if (not md_text or len(HEADING_RE.findall(md_text)) <= 1) and txts:
            # Prefer *-raw.txt if present
            raw_txts = [t for t in txts if t.endswith("-raw.txt")] or txts
            combined_txt = "\n\n".join((parent / t).read_text(encoding="utf-8", errors="replace") for t in raw_txts)
            md_text = promote_japanese_txt_headings(combined_txt, doc_title)
            md_text = ensure_hierarchical_headings(md_text, doc_title, "")

        if not HEADING_RE.search(md_text):
            md_text = f"# {doc_title}\n\n" + md_text

        md_path = parent / f"{stem}.md"
        md_path.write_text(md_text, encoding="utf-8")
        nrows = run_parse_sections(parent, stem)
        count += 1
        print(f"[RAW->MD+SECTIONS] {parent.relative_to(PUB_ROOT)} -> {nrows} sections")
    return count


def normalize_statute_markdown(md_text: str, doc_title: str, rel_path: str) -> str:
    """Normalize plain-text statute/bill/whitepaper Markdown files so all structural
    sections have proper `#` headings before running parse_regulatory_sections.py.
    """
    # 1. Strip huge base64 data:image blobs (e.g., wa.gov/my-health-my-data-act)
    md_text = re.sub(r"!\[[^\]]*\]\(data:image/[^)]+\)", "", md_text)
    md_text = re.sub(r"data:image/[a-zA-Z0-9.+/-]+;base64,[A-Za-z0-9+/=\s]{100,}", "", md_text)

    # 2. Unwrap single outer ``` code block if the statute body was pasted inside ``` ... ```
    # (e.g., iowa.gov/icdpa, tn.gov/tipa, maryland.gov/facial-recognition-laws)
    fences = list(re.finditer(r"^```[^\n]*$", md_text, re.MULTILINE))
    if len(fences) == 2 and fences[1].end() - fences[0].start() > len(md_text) * 0.6:
        before = md_text[: fences[0].start()]
        inside = md_text[fences[0].end() : fences[1].start()]
        after = md_text[fences[1].end() :]
        md_text = before + "\n" + inside + "\n" + after

    # 3. Promote plain-text statute/directive/memorandum headings when heading count is low (< 5)
    headings = HEADING_RE.findall(md_text)
    if len(headings) < 5 or rel_path in (
        "regulation/congress.gov/chips-act",
        "regulation/illinois.gov/bipa",
        "regulation/iowa.gov/icdpa",
        "regulation/tn.gov/tipa",
        "regulation/maryland.gov/facial-recognition-laws",
        "regulation/whitehouse.gov/nsm-ai",
        "regulation/europa.eu/eprivacy",
        "regulation/ny.gov/shield-act",
        "regulation/florida.gov/biometric-privacy-laws",
        "regulation/wa.gov/my-health-my-data-act",
    ):
        # In GPO statutes (e.g., CHIPS Act), inline <<NOTE: ...>> inside DIVISION/Subtitle headers can span lines
        md_text = re.sub(
            r"\b(DIVISION|TITLE|Subtitle|PART)\s+(<<NOTE:[^>]+>>)\s*([A-Z0-9]+)--([^\n]+)",
            lambda m: f"{m.group(1)} {m.group(3)}--{m.group(4).strip()} {' '.join(m.group(2).split())}",
            md_text,
        )
        lines = md_text.splitlines()
        new_lines = []
        in_toc = False
        for line in lines:
            s = line.strip()
            if not s:
                new_lines.append(line)
                continue
            s_unhashed = re.sub(r"^#+\s+", "", s)
            # Detect GPO Table of Contents sections ("SECTION 1. TABLE OF CONTENTS.", "SEC. 10000. TABLE OF CONTENTS.")
            if re.match(r"^(?:SECTION|SEC\.)\s+\d+\.\s+TABLE OF CONTENTS\.$", s_unhashed):
                new_lines.append(f"#### {s_unhashed}")
                in_toc = True
                continue
            if in_toc:
                # Real GPO statutory body sections after TOC use uppercase "SEC. <N>." (whereas TOC entries use "Sec. <N>.")
                if re.match(r"^SEC\.\s+\d+\.", s_unhashed):
                    in_toc = False
                    new_lines.append(f"#### {s_unhashed}")
                else:
                    new_lines.append(s_unhashed if s.startswith("#") else line)
                continue
            if s.startswith("#"):
                # Un-promote false-positive prose amendment lines like "#### Section 41201 of the ..."
                if re.match(r"^Section\s+\d+\s+of\s+", s_unhashed):
                    new_lines.append(s_unhashed)
                else:
                    new_lines.append(line)
                continue
            # GPO / Congressional bills: DIVISION A--..., TITLE I--..., Subtitle A--..., SEC. 101. ...
            if re.match(r"^DIVISION\s+[A-Z]\b", s) and len(s) < 160 and ".." not in s:
                new_lines.append(f"## {s}")
            elif re.match(r"^(?:TITLE|Title)\s+(?:[IVXLCDM]+|\d+)\b", s) and len(s) < 160 and ".." not in s:
                new_lines.append(f"### {s}")
            elif re.match(r"^(?:SUBTITLE|Subtitle|SUBCHAPTER|Subchapter|CHAPTER|Chapter|PART|Part)\s+(?:[A-Z]|[IVXLCDM]+|\d+[A-Za-z]?)\b", s) and len(s) < 160 and ".." not in s:
                new_lines.append(f"### {s}")
            elif re.match(r"^(?:SEC\.|Sec\.|SECTION|Section)\s+\d+[A-Za-z\-]*\.(?:\s|$)", s) and len(s) < 200 and ".." not in s:
                new_lines.append(f"#### {s}")
            elif re.match(r"^(?:Article|ARTICLE)\s+\d+[a-z]?\b", s) and len(s) < 120:
                new_lines.append(f"### {s}")
            elif re.match(r"^(?:715D\.\d+|47-18-\d+|501\.\d+|RCW\s+19\.373\.\d+|§+\s*\d+[\dA-Za-z\.\-]*)\b", s) and len(s) < 180:
                new_lines.append(f"### {s}")
            elif re.match(r"^\*\*(?:[1-9]\d?(?:\.\d+)*\s+)?[A-Z][^*]{3,90}\*\*$", s):
                clean_b = s.strip("*").strip()
                new_lines.append(f"## {clean_b}")
            else:
                new_lines.append(line)
        md_text = "\n".join(new_lines)

    if not HEADING_RE.search(md_text):
        md_text = f"# {doc_title}\n\n" + md_text.lstrip()

    return md_text


def process_markdown_only() -> int:
    """Structure all 193 Markdown-only editions in dataset-public into <stem>-sections.{json,csv}."""
    count = 0
    force_rels = {
        "regulation/congress.gov/chips-act",
    }
    for mp in sorted(PUB_ROOT.rglob("*-metadata.json")):
        parent = mp.parent
        rel_path = str(parent.relative_to(PUB_ROOT))
        files = [
            f.name
            for f in parent.iterdir()
            if f.is_file()
            and f.name != "README.md"
            and not f.name.startswith(".")
            and not f.name.endswith(("-metadata.json", "-metadata.md", "_meta.json"))
        ]
        jsons = [f for f in files if f.endswith(".json") and f != "README.json"]
        csvs = [f for f in files if f.endswith(".csv")]
        mds = sorted(f for f in files if f.endswith(".md"))
        if ((jsons or csvs) and rel_path not in force_rels) or not mds:
            continue

        stem = mp.name[: -len("-metadata.json")]
        md_meta = json.loads(mp.read_text(encoding="utf-8"))
        doc_title = md_meta.get("name") or stem

        # Pick canonical .md (preferring <stem>.md or non-"-processed"/"-definitions" if multiple)
        chosen_md = parent / mds[0]
        if f"{stem}.md" in mds:
            chosen_md = parent / f"{stem}.md"
        elif len(mds) > 1:
            non_proc = [m for m in mds if not m.endswith(("-processed.md", "-definitions.md"))]
            if non_proc:
                chosen_md = parent / non_proc[0]

        raw_txt = chosen_md.read_text(encoding="utf-8", errors="replace")
        norm_txt = normalize_statute_markdown(raw_txt, doc_title, rel_path)
        if norm_txt != raw_txt:
            chosen_md.write_text(norm_txt, encoding="utf-8")

        nrows = run_parse_sections(parent, stem)
        count += 1
        print(f"[MD->SECTIONS] {rel_path} ({chosen_md.name}) -> {nrows} sections")
    return count


def _append_egov_article(lines: list[str], art: ET.Element, heading_prefix: str = "###", id_prefix: str = "") -> None:
    art_t = "".join(art.find("ArticleTitle").itertext()).strip() if art.find("ArticleTitle") is not None else ""
    art_c = "".join(art.find("ArticleCaption").itertext()).strip() if art.find("ArticleCaption") is not None else ""
    lines.append(f"{heading_prefix} {id_prefix}{art_t} {art_c}".strip())
    lines.append("")
    for para in art.findall("Paragraph"):
        p_txt = " ".join("".join(para.itertext()).split())
        if p_txt:
            lines.append(p_txt)
            lines.append("")


def egov_xml_to_md(law_id: str, title: str) -> str:
    """Fetch and convert Japan e-Gov Law API v1 XML into hierarchical Markdown,
    including both MainProvision and all SupplProvision (附則) sections.
    """
    url = f"https://laws.e-gov.go.jp/api/1/lawdata/{law_id}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=20) as r:
        root = ET.fromstring(r.read())
    lines = [f"# {title}", ""]
    main_prov = root.find(".//MainProvision")
    if main_prov is None:
        return ""
    chapters = main_prov.findall("Chapter")
    if chapters:
        for ch in chapters:
            ch_t = "".join(ch.find("ChapterTitle").itertext()).strip() if ch.find("ChapterTitle") is not None else ""
            if ch_t:
                lines.append(f"## {ch_t}")
                lines.append("")
            for child in list(ch):
                if child.tag == "Section":
                    sec_t = "".join(child.find("SectionTitle").itertext()).strip() if child.find("SectionTitle") is not None else ""
                    if sec_t:
                        lines.append(f"### {sec_t}")
                        lines.append("")
                    for art in child.findall("Article"):
                        _append_egov_article(lines, art, "####")
                elif child.tag == "Article":
                    _append_egov_article(lines, child, "###")
    else:
        for art in main_prov.findall("Article"):
            _append_egov_article(lines, art, "##")

    # Traverse all SupplProvision (附則) elements so supplementary provisions and amendments are preserved
    for sp in root.findall(".//SupplProvision"):
        raw_lbl = "".join(sp.find("SupplProvisionLabel").itertext()).strip() if sp.find("SupplProvisionLabel") is not None else "附則"
        lbl = re.sub(r"[\s　]+", "", raw_lbl) or "附則"
        amend_num = sp.attrib.get("AmendLawNum", "").strip()
        sp_heading = f"{lbl}（{amend_num}）" if amend_num else lbl
        lines.append(f"## {sp_heading}")
        lines.append("")
        for child in list(sp):
            if child.tag == "Chapter":
                ch_t = "".join(child.find("ChapterTitle").itertext()).strip() if child.find("ChapterTitle") is not None else ""
                if ch_t:
                    lines.append(f"### {sp_heading} {ch_t}")
                    lines.append("")
                for art in child.findall(".//Article"):
                    _append_egov_article(lines, art, "####", id_prefix=f"{sp_heading}")
            elif child.tag == "Article":
                _append_egov_article(lines, child, "###", id_prefix=f"{sp_heading}")
            elif child.tag == "Paragraph":
                p_txt = " ".join("".join(child.itertext()).split())
                if p_txt:
                    lines.append(p_txt)
                    lines.append("")
    return "\n".join(lines) + "\n"


_CW_HEADER_KEYWORDS = (
    "ai rmf",
    "nist",
    "iso/iec",
    "framework",
    "identifier",
    "topic",
    "characteristics",
    "trustworthiness",
    "principle",
    "verify",
    "oecd",
    "guidebook",
    "eu ai act",
    "blueprint",
    "eo 13960",
)


def _is_cw_header_row(cells: list[str]) -> bool:
    non_empty = [re.sub(r"\*+", "", c).strip() for c in cells if c.strip()]
    if not non_empty:
        return False
    for c in non_empty:
        if re.match(r"^(?:GOVERN|MAP|MEASURE|MANAGE)\b(?:\s+\d+(?:\.\d+)?|\s*:)", c, re.I):
            return False
        if len(c) > 95 and "conceptual topics derived" not in c.lower():
            return False
    joined = " ".join(non_empty).lower()
    if "conceptual topics derived" in joined:
        return False
    return any(k in joined for k in _CW_HEADER_KEYWORDS)


def _normalize_cw_headers(cells: list[str]) -> list[str]:
    cleaned = [re.sub(r"\s+", " ", re.sub(r"\*+", "", c)).strip() for c in cells]
    out = []
    for i, c in enumerate(cleaned):
        if c:
            out.append(c)
        elif i + 1 < len(cleaned) and cleaned[i + 1]:
            out.append(f"{cleaned[i + 1]} ID")
        elif i > 0 and cleaned[i - 1]:
            out.append(f"{cleaned[i - 1]} Detail")
        else:
            out.append(f"Column {i + 1}")
    return out


def process_crosswalk_tables_and_statutes() -> int:
    """Structure Markdown pipe-table crosswalks (reference/nist.gov/ai-rmf-crosswalks/*)
    and re-parse supply-chain-partnership, maryland/facial-recognition-laws, and Japan e-Gov XML laws.
    """
    count = 0
    # 1. Re-run supply-chain-partnership from supply-chain-partnership-raw.txt
    scp_dir = PUB_ROOT / "control/meti.go.jp/supply-chain-partnership"
    if scp_dir.exists():
        raw_txt = (scp_dir / "supply-chain-partnership-raw.txt").read_text(encoding="utf-8", errors="replace")
        md_meta = json.loads((scp_dir / "supply-chain-partnership-metadata.json").read_text(encoding="utf-8"))
        md_text = promote_japanese_txt_headings(raw_txt, md_meta.get("name", "Supply Chain Partnership"))
        (scp_dir / "supply-chain-partnership.md").write_text(md_text, encoding="utf-8")
        nrows = run_parse_sections(scp_dir, "supply-chain-partnership")
        count += 1
        print(f"[RE-EXTRACT] control/meti.go.jp/supply-chain-partnership -> {nrows} sections")

    # 2. Maryland HB 338 (strip leading bill line numbers inside the bill block and promote 2-501..2-510 and SECTION 1..2)
    md_law_dir = PUB_ROOT / "regulation/maryland.gov/facial-recognition-laws"
    if md_law_dir.exists():
        md_path = md_law_dir / "facial-recognition-laws.md"
        txt = md_path.read_text(encoding="utf-8", errors="replace")
        txt = re.sub(r"^```[^\n]*\n?", "", txt, flags=re.MULTILINE)
        lines = []
        for l in txt.splitlines():
            clean_l = re.sub(r"^\s*\d{1,2}\s{3,}", "", l).strip()
            if re.match(r"^SECTION\s+\d+\.\s+(?:BE\s+IT\s+ENACTED|AND\s+BE\s+IT\s+FURTHER\s+ENACTED)", clean_l):
                lines.append(f"### {clean_l}")
            elif re.match(r"^2[–\-]5\d{2}\.\s*$", clean_l):
                sec_num = clean_l.rstrip(".").replace("–", "-")
                lines.append(f"#### Section {sec_num}")
            else:
                lines.append(re.sub(r"^\s*\d{1,2}\s{3,}", "", l))
        md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        nrows = run_parse_sections(md_law_dir, "facial-recognition-laws")
        count += 1
        print(f"[RE-EXTRACT] regulation/maryland.gov/facial-recognition-laws -> {nrows} sections")

    # 3. NIST AI RMF Crosswalks (parse Markdown pipe tables into structured rows with per-table header reset and continuation merging)
    cw_root = PUB_ROOT / "reference/nist.gov/ai-rmf-crosswalks"
    if cw_root.exists():
        for mp in sorted(cw_root.rglob("*-metadata.json")):
            parent = mp.parent
            if parent == cw_root:
                continue
            stem = mp.name[: -len("-metadata.json")]
            md_files = [p for p in parent.glob("*.md") if p.name != "README.md" and not p.name.endswith("-metadata.md")]
            if not md_files:
                continue
            txt = md_files[0].read_text(encoding="utf-8", errors="replace")
            blocks: list[list[str]] = []
            cur_block: list[str] = []
            for line in txt.splitlines():
                s = line.strip()
                if s.startswith("|") and s.endswith("|"):
                    cur_block.append(s)
                else:
                    if cur_block:
                        blocks.append(cur_block)
                        cur_block = []
            if cur_block:
                blocks.append(cur_block)

            rows = []
            headers: list[str] = []
            for b in blocks:
                for r_idx, line in enumerate(b):
                    cells = [re.sub(r"<br\s*/?>", "\n", c).strip() for c in line.strip("|").split("|")]
                    if all(re.match(r"^[:\-\s]*$", c) for c in cells):
                        continue
                    if r_idx == 0 and (_is_cw_header_row(cells) or not headers):
                        if _is_cw_header_row(cells):
                            # Check if Marker merged a repeated page header with a numbered clause continuation line
                            # (e.g., "ISO/IEC FDIS 23894\n6.7 Recording and reporting" in crosswalk_AI_RMF_1_0_ISO_IEC_23894)
                            hdr_only_cells = []
                            overflow_parts = []
                            for idx_c, cell_val in enumerate(cells):
                                c_lines = [cl.strip() for cl in cell_val.splitlines() if cl.strip()]
                                if len(c_lines) >= 2 and re.match(r"^\d+\.\d+(?:\.\d+)?\s+", c_lines[-1]):
                                    hdr_only_cells.append(" ".join(c_lines[:-1]))
                                    overflow_parts.append((idx_c, c_lines[-1]))
                                else:
                                    hdr_only_cells.append(cell_val)
                            headers = _normalize_cw_headers(hdr_only_cells)
                            if overflow_parts and rows:
                                cont_strs = [
                                    f"{headers[idx_c] if idx_c < len(headers) else f'Column {idx_c + 1}'}: {val_s}"
                                    for idx_c, val_s in overflow_parts
                                ]
                                rows[-1]["body"] += "\n\n" + " | ".join(cont_strs)
                            continue
                        elif not headers:
                            headers = [f"Column {i + 1}" for i in range(len(cells))]
                    if len(cells) != len(headers) and _is_cw_header_row(cells):
                        headers = _normalize_cw_headers(cells)
                        continue
                    # Handle 2-line split header continuations across crosswalk tables
                    c_stripped = [re.sub(r"\*+", "", c).strip() for c in cells]
                    if r_idx <= 2 and headers:
                        is_split_hdr = (
                            (len(c_stripped) == 4 and c_stripped[0] == "References" and c_stripped[2] == "References")
                            or (len(c_stripped) >= 2 and c_stripped[0] == "Trustworthiness" and c_stripped[1] == "Trustworthiness")
                            or (c_stripped[0].startswith("Trustworthy AI Systems") and headers[0].endswith("Characteristics of"))
                        )
                        if is_split_hdr:
                            headers = [
                                f"{headers[i]} {c_stripped[i]}".strip() if i < len(headers) else c_stripped[i]
                                for i in range(len(c_stripped))
                            ]
                            continue
                    non_empty = [c for c in cells if c]
                    if not non_empty:
                        continue
                    c0 = c_stripped[0] if c_stripped else ""
                    c1 = c_stripped[1] if len(c_stripped) > 1 else ""
                    non_empty_0 = re.sub(r"\*+", "", non_empty[0]).strip()
                    has_tta_id = bool(re.match(r"^\(?(?:Requirement\s+\d+(?:-\d+)?|\d{2}-\d[a-z])\)?(?:\s|$)", non_empty_0, re.I))
                    # Check if this row is a continuation row of the previous logical mapping row
                    is_cont = False
                    if rows and not has_tta_id:
                        if not c0:
                            if not c1 or (headers and "ID" not in headers[0] and headers[0] not in ("Column 1", "#")):
                                is_cont = True
                            elif rows[-1]["section_id"] and not re.match(r"^(?:GOVERN|MAP|MEASURE|MANAGE)\b", c1, re.I):
                                is_cont = True
                        elif (
                            rows[-1]["section_id"]
                            and headers
                            and headers[0] in ("AI RMF 1.0", "AI RMF 1.0 Function")
                            and not re.match(r"^(?:GOVERN|MAP|MEASURE|MANAGE)\b", c0, re.I)
                        ):
                            # Wrapped text fragment in col 0 of a GOVERN/MAP/MEASURE/MANAGE table
                            is_cont = True
                    if is_cont:
                        cont_parts = []
                        for idx_c, cell_val in enumerate(cells):
                            if not cell_val:
                                continue
                            hdr = headers[idx_c] if idx_c < len(headers) else f"Column {idx_c + 1}"
                            cont_parts.append(f"{hdr}: {cell_val}")
                        if cont_parts:
                            rows[-1]["body"] += "\n\n" + " | ".join(cont_parts)
                        continue

                    primary = c0 or c1 or non_empty_0
                    if re.match(r"^\d+$", primary) and c1:
                        primary = c1
                    if has_tta_id:
                        primary = non_empty_0
                    m_id = re.match(r"^((?:GOVERN|MAP|MEASURE|MANAGE)\b(?:\s+\d+(?:\.\d+)?)?)\s*[:\-–—]?\s*(.*)$", primary, re.I | re.S)
                    m_tta = re.match(r"^\(?(Requirement\s+\d+(?:-\d+)?|\d{2}-\d[a-z])\)?\s*(.*)$", primary, re.I | re.S)
                    if m_id:
                        sid = m_id.group(1).upper()
                        sname = m_id.group(2).strip() or (c1 if c0 and c1 else sid)
                        ikind = "numbered"
                    elif m_tta:
                        sid = m_tta.group(1)
                        sname = m_tta.group(2).strip() or (c_stripped[2] if len(c_stripped) > 2 else sid)
                        ikind = "numbered"
                    else:
                        sid = ""
                        sname = primary.replace("\n", " ")[:120]
                        ikind = ""
                    body_parts = []
                    for idx_c, cell_val in enumerate(cells):
                        if not cell_val:
                            continue
                        hdr = headers[idx_c] if idx_c < len(headers) else f"Column {idx_c + 1}"
                        body_parts.append(f"{hdr}: {cell_val}")
                    rows.append({
                        "depth": 2,
                        "section_id": sid,
                        "section_name": sname.replace("\n", " ")[:160],
                        "id_kind": ikind,
                        "parent_id": "",
                        "body": "\n\n".join(body_parts),
                    })
            if len(rows) > 2:
                jpath = parent / f"{stem}-sections.json"
                cpath = parent / f"{stem}-sections.csv"
                fields = ["depth", "section_id", "section_name", "id_kind", "parent_id", "body"]
                with cpath.open("w", newline="", encoding="utf-8") as f:
                    w = csv.DictWriter(f, fieldnames=fields, quoting=csv.QUOTE_ALL, lineterminator="\n")
                    w.writeheader()
                    w.writerows(rows)
                jpath.write_text(json.dumps(rows, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
                count += 1
                print(f"[CROSSWALK TABLE] {parent.relative_to(PUB_ROOT)} -> {len(rows)} rows")

    # 4. Japan e-Gov Law XML statutes (Basic Act on Cybersecurity + Active Cyber Defense Act)
    for rel, stem, law_id, title in [
        (
            "regulation/cyber.go.jp/basic-act-cybersecurity",
            "basic-act-cybersecurity",
            "426AC1000000104",
            "サイバーセキュリティ基本法 (Basic Act on Cybersecurity, Act No. 104 of 2014)",
        ),
        (
            "regulation/cyber.go.jp/active-cyber-defense-act",
            "active-cyber-defense-act",
            "507AC0000000042",
            "重要電子計算機に対する不正な行為による被害の防止に関する法律 (Active Cyber Defense Act, Act No. 42 of 2025)",
        ),
    ]:
        d = PUB_ROOT / rel
        if d.exists():
            md_text = egov_xml_to_md(law_id, title)
            if len(md_text) > 1000:
                (d / f"{stem}.md").write_text(md_text, encoding="utf-8")
                nrows = run_parse_sections(d, stem)
                count += 1
                print(f"[EGOV XML] {rel} -> {nrows} sections")
    return count


def main():
    c_priv = process_private_json_no_csv()
    c_pub_j2c = process_public_json_no_csv()
    c_pub_c2j = process_public_csv_no_json()
    c_raw = process_raw_on_disk()
    c_md = process_markdown_only()
    c_cw = process_crosswalk_tables_and_statutes()
    print(
        f"\nBatch 1A summary: private_json->csv={c_priv}, public_json->csv={c_pub_j2c}, "
        f"public_csv->json={c_pub_c2j}, raw_extracted={c_raw}, md_structured={c_md}, crosswalk_statutes={c_cw}"
    )


if __name__ == "__main__":
    main()
