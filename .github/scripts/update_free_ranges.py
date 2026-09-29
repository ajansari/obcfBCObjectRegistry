#!/usr/bin/env python3
"""Rebuild the Free ranges table from the Registry table.

Reads every object range in ObjectRegistry.md and replaces the Free ranges
data rows with the gaps left in 50000–99999. Use this after a hand edit so a
removed or changed app is no longer missing from, or still blocking, the free
list. Registry rows are not changed.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PTE_LOW, PTE_HIGH = 50000, 99999
EN_DASH = "\u2013"
RANGE_RE = re.compile(r"(\d+)\s*[–-]\s*(\d+)")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--registry-md", type=Path, default=ROOT / "ObjectRegistry.md")
    p.add_argument("--summary", default="", help="Append a Markdown summary to this file")
    p.add_argument("--dry-run", action="store_true", help="Report the rebuilt rows without writing")
    return p.parse_args()


def find_section(lines: list[str], title: str) -> tuple[int, int]:
    start = None
    for i, line in enumerate(lines):
        if not line.startswith("## "):
            continue
        heading = line[3:].strip()
        if heading == title or heading.startswith(title + " "):
            start = i
            break
    if start is None:
        raise SystemExit(f"Could not find a '## {title}' section in ObjectRegistry.md.")
    end = len(lines)
    for j in range(start + 1, len(lines)):
        if lines[j].startswith("## "):
            end = j
            break
    return start, end


def is_separator(line: str) -> bool:
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", c) for c in cells)


def table_bounds(lines: list[str], start: int, end: int, title: str) -> tuple[int, int]:
    table_start = next((i for i in range(start, end) if lines[i].lstrip().startswith("|")), None)
    if table_start is None:
        raise SystemExit(f"The {title} section has no table.")
    table_end = table_start
    while table_end < end and lines[table_end].lstrip().startswith("|"):
        table_end += 1
    if table_end - table_start < 2 or not is_separator(lines[table_start + 1]):
        raise SystemExit(f"The {title} table must have a header row and a dash separator.")
    return table_start, table_end


def split_cells(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def cell_ranges(text: str) -> list[tuple[int, int]]:
    found: list[tuple[int, int]] = []
    for match in RANGE_RE.finditer(text or ""):
        start, end = int(match.group(1)), int(match.group(2))
        if start > end:
            start, end = end, start
        found.append((start, end))
    return found


def used_ranges(lines: list[str]) -> list[tuple[int, int]]:
    start, end = find_section(lines, "Registry")
    table_start, table_end = table_bounds(lines, start, end, "Registry")
    header = split_cells(lines[table_start])
    try:
        range_idx = next(i for i, name in enumerate(header) if "range" in name.lower())
    except StopIteration as exc:
        raise SystemExit("Registry table has no range column.") from exc
    used: list[tuple[int, int]] = []
    for line in lines[table_start + 2 : table_end]:
        cells = split_cells(line)
        if range_idx >= len(cells):
            print(f"::warning::Skipping a registry row with no range cell: {line}")
            continue
        spans = cell_ranges(cells[range_idx])
        if not spans:
            print(f"::warning::Registry row has no object range: {line}")
        used.extend(spans)
    return used


def free_ranges(used: list[tuple[int, int]]) -> list[tuple[int, int]]:
    clipped = sorted((max(a, PTE_LOW), min(b, PTE_HIGH)) for a, b in used if b >= PTE_LOW and a <= PTE_HIGH)
    free: list[tuple[int, int]] = []
    cursor = PTE_LOW
    for start, end in clipped:
        if start > cursor:
            free.append((cursor, start - 1))
        cursor = max(cursor, end + 1)
    if cursor <= PTE_HIGH:
        free.append((cursor, PTE_HIGH))
    return free


def format_row(start: int, end: int) -> str:
    return f"| {start}{EN_DASH}{end} |"


def write_summary(path: str, before: int, gaps: list[tuple[int, int]], changed: bool) -> None:
    shown = "\n".join(f"- {start}–{end}" for start, end in gaps) or "- none — 50000–99999 is fully allocated"
    status = "Free ranges were rewritten." if changed else "Free ranges were already correct. No file change."
    with open(path, "a", encoding="utf-8") as handle:
        handle.write(
            "\n".join(
                [
                    "## Free ranges updated",
                    "",
                    status,
                    "",
                    f"- Previous free-range rows: {before}",
                    f"- Free-range rows now: {len(gaps)}",
                    "",
                    shown,
                    "",
                ]
            )
        )


def main() -> int:
    args = parse_args()
    md_path = args.registry_md
    if not md_path.is_file():
        raise SystemExit(f"Missing {md_path}")
    lines = md_path.read_text(encoding="utf-8").splitlines()
    used = used_ranges(lines)
    gaps = free_ranges(used)
    free_start, free_end = find_section(lines, "Free ranges")
    table_start, table_end = table_bounds(lines, free_start, free_end, "Free ranges")
    new_rows = [format_row(start, end) for start, end in gaps]
    old_rows = lines[table_start + 2 : table_end]
    changed = old_rows != new_rows
    print(f"Registry ranges read: {len(used)}")
    print(f"Free-range rows before: {len(old_rows)}")
    print(f"Free-range rows after: {len(new_rows)}")
    for row in new_rows:
        print(f"  {row}")
    if args.summary:
        write_summary(args.summary, len(old_rows), gaps, changed)
    if not changed:
        print("Free ranges already match the Registry table. Nothing to write.")
        return 0
    if args.dry_run:
        print("Dry run. No files written.")
        return 0
    updated = lines[: table_start + 2] + new_rows + lines[table_end:]
    md_path.write_text("\n".join(updated) + "\n", encoding="utf-8")
    print("Rebuilt the Free ranges table from the Registry table.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
