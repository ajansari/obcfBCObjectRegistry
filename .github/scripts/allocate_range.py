#!/usr/bin/env python3
"""Reserve the first free contiguous Business Central object ID block.

Reads used ranges from ObjectRegistry.md, finds the first contiguous block of
the requested size in 50000–99999, appends a pending app to registry.json, and
regenerates ObjectRegistry.md via build.py.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

SEARCH_LOW = 50000
SEARCH_HIGH = 99999
RANGE_RE = re.compile(r"(\d+)\s*[–-]\s*(\d+)")
ROOT = Path(__file__).resolve().parents[2]


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--count", required=True, help="Number of object IDs to reserve (e.g. 10, 20, 50)")
    p.add_argument("--name", required=True, help="Placeholder project name")
    p.add_argument("--dry-run", action="store_true", help="Print the range without writing files")
    p.add_argument("--output-env", default="", help="Append GitHub Actions outputs to this file")
    p.add_argument("--summary", default="", help="Append a Markdown summary to this file")
    p.add_argument("--registry-md", type=Path, default=ROOT / "ObjectRegistry.md")
    p.add_argument("--registry-json", type=Path, default=ROOT / "registry.json")
    p.add_argument("--build-py", type=Path, default=ROOT / "build.py")
    return p.parse_args()


def parse_count(raw: str) -> int:
    try:
        count = int(str(raw).strip())
    except (TypeError, ValueError) as exc:
        raise SystemExit(f"Object count must be a whole number, got {raw!r}.") from exc
    if count < 1:
        raise SystemExit("Object count must be at least 1.")
    if count > SEARCH_HIGH - SEARCH_LOW + 1:
        raise SystemExit(f"Object count {count} exceeds the 50000–99999 search window.")
    return count


def sanitize_name(raw: str) -> str:
    cleaned = str(raw).translate({ord(c): " " for c in "|`$\"'\\<>"})
    name = " ".join(cleaned.split())
    if not name:
        raise SystemExit("Project name is required.")
    if not name.endswith(" - Pending"):
        name = f"{name} - Pending"
    return name


def registry_table_rows(md: str) -> list[list[str]]:
    rows: list[list[str]] = []
    in_registry = False
    for line in md.splitlines():
        if line.startswith("## "):
            in_registry = line.startswith("## Registry")
            continue
        if not in_registry or not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if not cells or set(cells[0]) <= {"-", ":"}:
            continue
        rows.append(cells)
    return rows


def used_ranges_from_markdown(md: str) -> list[tuple[int, int]]:
    rows = registry_table_rows(md)
    if not rows:
        raise SystemExit("Could not find the registry table in ObjectRegistry.md.")
    header, data = rows[0], rows[1:]
    try:
        range_idx = next(i for i, h in enumerate(header) if "range" in h.lower())
    except StopIteration as exc:
        raise SystemExit("ObjectRegistry.md registry table has no range column.") from exc
    used: list[tuple[int, int]] = []
    for row in data:
        if range_idx >= len(row):
            continue
        for match in RANGE_RE.finditer(row[range_idx]):
            start, end = int(match.group(1)), int(match.group(2))
            if start > end:
                start, end = end, start
            used.append((start, end))
    return used


def merge_used(ranges: list[tuple[int, int]]) -> list[list[int]]:
    clipped: list[tuple[int, int]] = []
    for start, end in ranges:
        lo, hi = max(start, SEARCH_LOW), min(end, SEARCH_HIGH)
        if lo <= hi:
            clipped.append((lo, hi))
    clipped.sort()
    merged: list[list[int]] = []
    for start, end in clipped:
        if not merged or start > merged[-1][1] + 1:
            merged.append([start, end])
        else:
            merged[-1][1] = max(merged[-1][1], end)
    return merged


def first_free_block(used: list[tuple[int, int]], size: int) -> tuple[int, int]:
    cursor = SEARCH_LOW
    for start, end in merge_used(used):
        if start - cursor >= size:
            return cursor, cursor + size - 1
        cursor = max(cursor, end + 1)
    if SEARCH_HIGH - cursor + 1 >= size:
        return cursor, cursor + size - 1
    raise SystemExit(
        f"No contiguous block of {size} object IDs is available between {SEARCH_LOW} and {SEARCH_HIGH}."
    )


def dump_registry(data: dict, path: Path) -> None:
    def dumps(obj) -> str:
        return json.dumps(obj, ensure_ascii=False, separators=(", ", ": "))

    apps = ",\n    ".join(dumps(app) for app in data["apps"])
    notes = ",\n    ".join(dumps(note) for note in data["notes"])
    path.write_text(
        "{\n"
        f'  "asOf": {dumps(data["asOf"])},\n'
        f'  "githubOwner": {dumps(data["githubOwner"])},\n'
        f'  "apps": [\n    {apps}\n  ],\n'
        f'  "notes": [\n    {notes}\n  ]\n'
        "}\n",
        encoding="utf-8",
    )


def append_pending_app(path: Path, name: str, start: int, end: int, issued: str) -> None:
    data = json.loads(path.read_text(encoding="utf-8"))
    data["apps"].append(
        {
            "name": name,
            "appId": "—",
            "ranges": [[start, end]],
            "type": "PTE",
            "repo": "—",
            "visibility": "—",
            "issued": issued,
        }
    )
    dump_registry(data, path)


def write_github_output(path: str, values: dict[str, str]) -> None:
    with open(path, "a", encoding="utf-8") as handle:
        for key, value in values.items():
            handle.write(f"{key}={value}\n")


def write_summary(path: str, name: str, start: int, end: int, count: int, issued: str) -> None:
    with open(path, "a", encoding="utf-8") as handle:
        handle.write(
            "\n".join(
                [
                    "## Object range reserved",
                    "",
                    f"- **Project:** {name}",
                    f"- **Range:** `{start}-{end}`",
                    f"- **Object IDs:** {count}",
                    f"- **Issued:** {issued}",
                    "",
                    f"Reserved the first available contiguous block in 50000–99999 and committed it to `ObjectRegistry.md`.",
                    "",
                ]
            )
        )


def main() -> int:
    args = parse_args()
    count = parse_count(args.count)
    name = sanitize_name(args.name)
    issued = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    md_path = args.registry_md
    if not md_path.is_file():
        raise SystemExit(f"Missing {md_path}")
    used = used_ranges_from_markdown(md_path.read_text(encoding="utf-8"))
    start, end = first_free_block(used, count)
    hyphen_range = f"{start}-{end}"
    print(f"Allocated range: {hyphen_range}")
    print(f"Project: {name}")
    print(f"Issued: {issued}")
    print(f"::notice title=Object range reserved::{hyphen_range} for {name} (issued {issued})")
    if args.output_env:
        write_github_output(
            args.output_env,
            {"range": hyphen_range, "project": name, "issued": issued, "count": str(count)},
        )
    if args.summary:
        write_summary(args.summary, name, start, end, count, issued)
    if args.dry_run:
        return 0
    if not args.registry_json.is_file():
        raise SystemExit(f"Missing {args.registry_json}")
    append_pending_app(args.registry_json, name, start, end, issued)
    subprocess.check_call([sys.executable, str(args.build_py)], cwd=str(args.build_py.parent))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
