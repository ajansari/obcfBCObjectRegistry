#!/usr/bin/env python3
"""Delete every data row from the Registry table and reset Free ranges.

Keeps each table's header row and dash separator. After the wipe, the Free
ranges table has one row, 50000–99999, because that whole window is available.
Also clears registry.json so a later render cannot put the rows back. This
cannot be undone from the current files.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONFIRM_PHRASE = "CLEAR ALL DATA"
PTE_LOW, PTE_HIGH = 50000, 99999
EN_DASH = "\u2013"
CLEARED_NOTE = (
    "Registry data was cleared. Every data row was removed from the Registry table. "
    "The Free ranges table lists 50000–99999, because that whole range is available again. "
    "This wipe cannot be reversed from the current files."
)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--confirm",
        required=True,
        help=f"Must be exactly {CONFIRM_PHRASE}. Anything else leaves the files unchanged.",
    )
    p.add_argument("--registry-md", type=Path, default=ROOT / "ObjectRegistry.md")
    p.add_argument("--registry-json", type=Path, default=ROOT / "registry.json")
    p.add_argument("--summary", default="", help="Append a Markdown summary to this file")
    p.add_argument("--dry-run", action="store_true", help="Report what would be deleted without writing")
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
    if table_end - table_start < 2:
        raise SystemExit(f"The {title} table is missing its header or separator row.")
    if is_separator(lines[table_start]) or not is_separator(lines[table_start + 1]):
        raise SystemExit(f"The {title} table must keep a header row followed by a dash separator.")
    return table_start, table_end


def clear_table(lines: list[str], title: str) -> tuple[list[str], int]:
    start, end = find_section(lines, title)
    table_start, table_end = table_bounds(lines, start, end, title)
    removed = max(0, table_end - (table_start + 2))
    return lines[: table_start + 2] + lines[table_end:], removed


def reset_free_ranges(lines: list[str]) -> list[str]:
    """Leave one free-range row for the whole PTE window."""
    start, end = find_section(lines, "Free ranges")
    table_start, table_end = table_bounds(lines, start, end, "Free ranges")
    row = f"| {PTE_LOW}{EN_DASH}{PTE_HIGH} |"
    return lines[: table_start + 2] + [row] + lines[table_end:]


def replace_notes(lines: list[str], note: str) -> list[str]:
    start, end = find_section(lines, "Notes")
    out = lines[: start + 1]
    if start + 1 < end and lines[start + 1] == "":
        out.append("")
    out.append(f"- {note}")
    out.append("")
    out.extend(lines[end:])
    return out


def write_cleared_json(path: Path, note: str) -> int:
    data = json.loads(path.read_text(encoding="utf-8"))
    removed = len(data.get("apps") or [])
    as_of = json.dumps(data.get("asOf", ""), ensure_ascii=False)
    owner = json.dumps(data.get("githubOwner", ""), ensure_ascii=False)
    path.write_text(
        "{\n"
        f'  "asOf": {as_of},\n'
        f'  "githubOwner": {owner},\n'
        '  "apps": [],\n'
        "  \"notes\": [\n"
        f"    {json.dumps(note, ensure_ascii=False)}\n"
        "  ]\n"
        "}\n",
        encoding="utf-8",
    )
    return removed


def write_summary(path: str, registry_rows: int, free_rows: int, apps: int) -> None:
    with open(path, "a", encoding="utf-8") as handle:
        handle.write(
            "\n".join(
                [
                    "## Registry data cleared",
                    "",
                    "This run permanently deleted registry data. It cannot be reversed from the current files.",
                    "",
                    f"- Registry data rows removed: {registry_rows}",
                    f"- Free-range data rows replaced: {free_rows}",
                    f"- Free ranges now: {PTE_LOW}–{PTE_HIGH}",
                    f"- `registry.json` apps removed: {apps}",
                    "",
                    "The header row and dash separator were kept. The Free ranges table has one row because the whole window is available.",
                    "",
                ]
            )
        )


def main() -> int:
    args = parse_args()
    phrase = " ".join(str(args.confirm).split())
    if phrase != CONFIRM_PHRASE:
        raise SystemExit(
            "Refusing to clear. Confirmation phrase did not match "
            f"{CONFIRM_PHRASE!r}. No files were changed."
        )
    md_path = args.registry_md
    json_path = args.registry_json
    if not md_path.is_file():
        raise SystemExit(f"Missing {md_path}")
    if not json_path.is_file():
        raise SystemExit(f"Missing {json_path}")

    lines = md_path.read_text(encoding="utf-8").splitlines()
    lines, registry_rows = clear_table(lines, "Registry")
    lines, free_rows = clear_table(lines, "Free ranges")
    lines = reset_free_ranges(lines)
    lines = replace_notes(lines, CLEARED_NOTE)
    print(f"Registry data rows to remove: {registry_rows}")
    print(f"Free-range data rows replaced: {free_rows}")
    print(f"Free ranges reset to {PTE_LOW}-{PTE_HIGH}.")
    print("::warning title=Irreversible wipe::All registry data rows will be deleted. Free ranges will be reset to 50000-99999.")
    if args.summary:
        write_summary(
            args.summary,
            registry_rows,
            free_rows,
            len(json.loads(json_path.read_text(encoding="utf-8")).get("apps") or []),
        )
    if args.dry_run:
        print("Dry run. No files written.")
        return 0
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    removed_apps = write_cleared_json(json_path, CLEARED_NOTE)
    print(f"Cleared {removed_apps} apps from {json_path.name}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
