#!/usr/bin/env python3
"""Convert the upstream FiGHT YAML to JSON.

FiGHT publishes only YAML. The JSON here is a straight serialization of it,
kept for consumers that prefer JSON; it adds no data and applies no transform.

Upstream has no releases and no tags, so the input is pinned by commit SHA:

    curl -sL -o fight.yaml \\
        https://raw.githubusercontent.com/mitre/FiGHT/097cd5f73811/fight.yaml
    python3 convert_fight.py

Re-pinning to a newer commit means updating the SHA above, in README.md, and in
fight-metadata.json (scope.pinned_commit and current_extraction.notes).
"""

import json
import pathlib

import yaml

HERE = pathlib.Path(__file__).parent


def main() -> None:
    src = HERE / "fight.yaml"
    dst = HERE / "fight.json"

    data = yaml.safe_load(src.read_text(encoding="utf-8"))
    dst.write_text(
        json.dumps(data, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    counts = {k: len(v) for k, v in data.items() if isinstance(v, (list, dict))}
    print(f"wrote {dst.name} ({dst.stat().st_size:,} bytes)")
    for key, n in sorted(counts.items()):
        print(f"  {key}: {n}")


if __name__ == "__main__":
    main()
