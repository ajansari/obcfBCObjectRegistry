#!/usr/bin/env python3
"""Append one app to the Registry table and refresh the Free ranges table.

The new row is always the last data row. Optional repo name, URL, and
visibility may be omitted. A repo URL is written as a hyperlink on the repo
name with target=\"_blank\".
"""
from __future__ import annotations

import argparse
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PTE_LOW, PTE_HIGH = 50000, 99999
EN_DASH = "\u2013"
RANGE_RE = re.compile(r"(\d+)\s*[-\u2013]\s*(\d+)")
URL_RE = re.compile(r"^https?://[^\s\"'<>|]+$")
SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS))
from allocate_range import dump_registry  # noqa: E402


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--name", required=True, help="App name")
    p.add_argument("--app-id", required=True, help="App ID")
    p.add_argument("--ranges", required=True, help="Object range(s), for example 50000-50010")
    p.add_argument("--type", required=True, dest="app_type", help="PTE or AppSource")
    p.add_argument("--repo-name", default="", help="GitHub or DevOps repo name, if available")
    p.add_argument("--repo-url", default="", help="Repo URL, if available")
    p.add_argument("--visibility", default="", help="Public, Private, or blank")
    p.add_argument("--registry-md", type=Path, default=ROOT / "ObjectRegistry.md")
    p.add_argument("--registry-json", type=Path, default=ROOT / "registry.json")
    p.add_argument("--output-env", default="", help="Append GitHub Actions outputs to this file")
    p.add_argument("--summary", default="", help="Append a Markdown summary to this file")
    p.add_argument("--dry-run", action="store_true", help="Print the row without writing files")
    return p.parse_args()


def plain(raw: str, label: str, required: bool) -> str:
    text = " ".join(str(raw or "").split())
    if required and not text:
        raise SystemExit(f"{label} is required.")
    if "|" in text:
        raise SystemExit(f"{label} cannot contain a pipe character.")
    return text


def parse_ranges(raw: str) -> list[tuple[int, int]]:
    text = str(raw or "").replace("\u2013", "-").replace("\u2014", "-")
    ranges: list[tuple[int, int]] = []
    for part in re.split(r"[;,]", text):
        part = part.strip()
        if not part:
            continue
        match = re.fullmatch(r"(\d+)\s*-\s*(\d+)", part)
        if not match:
            raise SystemExit(
                f"Could not parse object range {part!r}. "
                "Use 50000-50010 or 50000-50010; 50100-50120."
            )
        start, end = int(match.group(1)), int(match.group(2))
        if start < 1 or end < 1:
            raise SystemExit("Object IDs must be positive.")
        if start > end:
            raise SystemExit(f"Range start {start} is after end {end}.")
        ranges.append((start, end))
    if not ranges:
        raise SystemExit("At least one object range is required, for example 50000-50010.")
    return ranges


def parse_type(raw: str) -> str:
    value = " ".join(str(raw or "").split()).lower()
    if value == "pte":
        return "PTE"
    if value == "appsource":
        return "AppSource"
    raise SystemExit("Type must be PTE or AppSource.")


def parse_visibility(raw: str) -> str:
    value = " ".join(str(raw or "").split())
    if value.lower() in {"", "not provided", "—", "-", "n/a", "na", "none"}:
        return "—"
    if value.lower() == "public":
        return "Public"
    if value.lower() == "private":
        return "Private"
    raise SystemExit("Visibility must be Public, Private, or left blank.")


def parse_url(raw: str) -> str:
    url = " ".join(str(raw or "").split())
    if not url:
        return ""
    if not URL_RE.fullmatch(url):
        raise SystemExit("Repo URL must be an http or https URL with no spaces.")
    return url


def display_ranges(ranges: list[tuple[int, int]]) -> str:
    return "; ".join(f"{start}{EN_DASH}{end}" for start, end in ranges)


def repo_display_name(name: str, url: str) -> str:
    if name:
        return name
    if not url:
        return ""
    tail = url.rstrip("/").rsplit("/", 1)[-1]
    return tail or url


def repo_cell(name: str, url: str) -> str:
    if not name:
        return "—"
    safe_name = html.escape(name)
    if not url:
        return f"<code>{safe_name}</code>"
    return (
        f'<a href="{html.escape(url, quote=True)}" target="_blank" rel="noopener">'
        f"<code>{safe_name}</code></a>"
    )


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


def split_cells(line: str) -> list[str]:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def join_cells(cells: list[str]) -> str:
    return "| " + " | ".join(cells) + " |"


def is_separator(line: str) -> bool:
    cells = split_cells(line)
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


def column_index(header: list[str], needle: str) -> int:
    for i, name in enumerate(header):
        if needle in name.lower():
            return i
    raise SystemExit(f"Registry table has no {needle!r} column.")


def cell_ranges(text: str) -> list[tuple[int, int]]:
    found: list[tuple[int, int]] = []
    for match in RANGE_RE.finditer(text or ""):
        start, end = int(match.group(1)), int(match.group(2))
        if start > end:
            start, end = end, start
        found.append((start, end))
    return found


def intersects(left: list[tuple[int, int]], right: list[tuple[int, int]]) -> bool:
    return any(a <= d and c <= b for a, b in left for c, d in right)


def add_overlap(cell: str, name: str) -> str:
    if not cell or cell == "—":
        return name
    names = [part.strip() for part in cell.split(";") if part.strip() and part.strip() != "—"]
    if name not in names:
        names.append(name)
    return "; ".join(names) if names else "—"


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


def warn_range_window(app_type: str, ranges: list[tuple[int, int]]) -> None:
    for start, end in ranges:
        in_pte = PTE_LOW <= start <= PTE_HIGH and PTE_LOW <= end <= PTE_HIGH
        in_appsource = start >= 70000000 and end >= 70000000
        if app_type == "PTE" and not in_pte:
            print(f"::warning::PTE range {start}-{end} is outside 50000-99999.")
        if app_type == "AppSource" and not in_appsource:
            print(f"::warning::AppSource range {start}-{end} is below 70000000.")


def write_github_output(path: str, values: dict[str, str]) -> None:
    with open(path, "a", encoding="utf-8") as handle:
        for key, value in values.items():
            handle.write(f"{key}={value}\n")


def write_summary(path: str, name: str, app_id: str, ranges: str, app_type: str, repo: str, visibility: str, gaps: list[tuple[int, int]]) -> None:
    shown = ", ".join(f"{start}–{end}" for start, end in gaps) or "none — 50000–99999 is fully allocated"
    with open(path, "a", encoding="utf-8") as handle:
        handle.write(
            "\n".join(
                [
                    "## Registry row added",
                    "",
                    f"- **App name:** {name}",
                    f"- **App ID:** `{app_id}`",
                    f"- **Object range(s):** {ranges}",
                    f"- **Type:** {app_type}",
                    f"- **Repo:** {repo}",
                    f"- **Visibility:** {visibility}",
                    f"- **Free ranges now:** {shown}",
                    "",
                    "The new row is the last row of the Registry table. Its range was removed from the Free ranges table, which can shorten a row, split one row into two, or remove a row.",
                    "",
                ]
            )
        )


def main() -> int:
    args = parse_args()
    name = plain(args.name, "App name", required=True)
    app_id = plain(args.app_id, "App ID", required=True).strip("`")
    if not app_id:
        raise SystemExit("App ID is required.")
    ranges = parse_ranges(args.ranges)
    app_type = parse_type(args.app_type)
    repo_name = plain(args.repo_name, "Repo name", required=False)
    repo_url = parse_url(args.repo_url)
    visibility = parse_visibility(args.visibility)
    repo_name = repo_display_name(repo_name, repo_url)
    warn_range_window(app_type, ranges)

    md_path = args.registry_md
    json_path = args.registry_json
    if not md_path.is_file():
        raise SystemExit(f"Missing {md_path}")
    if not json_path.is_file():
        raise SystemExit(f"Missing {json_path}")

    lines = md_path.read_text(encoding="utf-8").splitlines()
    reg_start, reg_end = find_section(lines, "Registry")
    table_start, table_end = table_bounds(lines, reg_start, reg_end, "Registry")
    header = split_cells(lines[table_start])
    name_idx = column_index(header, "app name")
    id_idx = column_index(header, "app id")
    range_idx = column_index(header, "range")
    type_idx = column_index(header, "type")
    overlap_idx = column_index(header, "overlap")
    repo_idx = column_index(header, "repo")
    vis_idx = column_index(header, "visibility")
    issued_idx = next((i for i, col in enumerate(header) if "issued" in col.lower()), None)

    data_lines = lines[table_start + 2 : table_end]
    existing: list[tuple[str, list[str]]] = []
    for line in data_lines:
        cells = split_cells(line)
        if len(cells) < len(header):
            cells.extend("—" for _ in range(len(header) - len(cells)))
        existing.append((line, cells))
        if cells[name_idx].casefold() == name.casefold():
            raise SystemExit(f"An app named {name!r} is already in the Registry table.")

    new_ranges = ranges
    overlap_names = [
        cells[name_idx]
        for _, cells in existing
        if intersects(new_ranges, cell_ranges(cells[range_idx]))
    ]
    updated_lines: list[str] = []
    for original, cells in existing:
        if intersects(new_ranges, cell_ranges(cells[range_idx])):
            cells = cells[:]
            cells[overlap_idx] = add_overlap(cells[overlap_idx], name)
            updated_lines.append(join_cells(cells))
        else:
            updated_lines.append(original)

    new_cells = ["—"] * len(header)
    new_cells[name_idx] = name
    new_cells[id_idx] = f"`{app_id}`"
    new_cells[range_idx] = display_ranges(ranges)
    new_cells[type_idx] = app_type
    new_cells[overlap_idx] = "; ".join(overlap_names) if overlap_names else "—"
    new_cells[repo_idx] = repo_cell(repo_name, repo_url)
    new_cells[vis_idx] = visibility
    if issued_idx is not None:
        new_cells[issued_idx] = "—"
    updated_lines.append(join_cells(new_cells))

    used = [span for _, cells in existing for span in cell_ranges(cells[range_idx])]
    used.extend(ranges)
    gaps = free_ranges(used)
    free_start, free_end = find_section(lines, "Free ranges")
    free_table_start, free_table_end = table_bounds(lines, free_start, free_end, "Free ranges")
    free_lines = [join_cells([f"{start}{EN_DASH}{end}"]) for start, end in gaps]

    def splice(source: list[str], start: int, end: int, replacement: list[str]) -> list[str]:
        return source[:start] + replacement + source[end:]

    edits = sorted(
        (
            (table_start + 2, table_end, updated_lines),
            (free_table_start + 2, free_table_end, free_lines),
        ),
        key=lambda item: item[0],
        reverse=True,
    )
    for start, end, replacement in edits:
        lines = splice(lines, start, end, replacement)

    range_text = display_ranges(ranges)
    print(f"Appending row: {name} | {app_id} | {range_text} | {app_type}")
    print(f"Repo: {repo_name or '—'} {repo_url}".rstrip())
    print(f"Free ranges remaining: {len(gaps)}")
    for start, end in gaps:
        print(f"  free {start}-{end}")
    if args.output_env:
        write_github_output(
            args.output_env,
            {"app": name, "ranges": range_text.replace("\u2013", "-"), "type": app_type},
        )
    if args.summary:
        write_summary(
            args.summary,
            name,
            app_id,
            range_text,
            app_type,
            repo_cell(repo_name, repo_url) if repo_name else "—",
            visibility,
            gaps,
        )
    if args.dry_run:
        print(join_cells(new_cells))
        print("Dry run. No files written.")
        return 0

    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    data = json.loads(json_path.read_text(encoding="utf-8"))
    app = {
        "name": name,
        "appId": app_id,
        "ranges": [[start, end] for start, end in ranges],
        "type": app_type,
        "repo": repo_name or "—",
        "visibility": visibility,
    }
    if repo_url:
        app["url"] = repo_url
    elif repo_name:
        app["url"] = ""
    data.setdefault("apps", []).append(app)
    dump_registry(data, json_path)
    print(f"Appended {name} as the last registry row and updated free ranges.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
