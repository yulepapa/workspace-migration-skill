#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


CODE_MARKERS = {
    "package.json",
    "pyproject.toml",
    "requirements.txt",
    "Cargo.toml",
    "go.mod",
    "build.gradle",
    "settings.gradle",
    "pom.xml",
}

GENERATED_DIRS = {
    "node_modules",
    ".next",
    "dist",
    "build",
    ".turbo",
    "test-results",
    ".venv",
    "venv",
    "__pycache__",
}

PROJECT_STATE_DIRS = {".codex", ".claude", ".cursor", ".gemini", ".omx", ".omo", ".vscode"}

DO_NOT_TOUCH_PREFIXES = (
    ".codex",
    ".claude",
    ".antigravity",
    ".antigravity-ide",
    ".gemini/antigravity",
    "Library/Application Support",
)

ASSET_EXTS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".svg",
    ".webp",
    ".mp4",
    ".mov",
    ".m4v",
    ".mp3",
    ".wav",
    ".ttf",
    ".otf",
    ".woff",
    ".woff2",
}

DATA_EXTS = {".csv", ".tsv", ".xlsx", ".xls", ".json", ".jsonl", ".hyper", ".parquet", ".db", ".sqlite"}
DOC_EXTS = {".pdf", ".docx", ".pptx", ".key", ".md", ".txt"}


@dataclass
class Finding:
    path: str
    kind: str
    suggestion: str
    risk: str
    reason: str
    markers: list[str]
    warnings: list[str]


def rel_to_home(path: Path, home: Path) -> str:
    try:
        return "~/" + str(path.relative_to(home))
    except ValueError:
        return str(path)


def is_under_do_not_touch(path: Path, home: Path) -> bool:
    try:
        rel = str(path.relative_to(home))
    except ValueError:
        return False
    return any(rel == prefix or rel.startswith(prefix + os.sep) for prefix in DO_NOT_TOUCH_PREFIXES)


def workspace_parts(path: Path, home: Path) -> tuple[str, ...] | None:
    try:
        parts = path.relative_to(home).parts
    except ValueError:
        return None
    if len(parts) >= 2 and parts[0] == "Workspace":
        return parts
    return None


def is_under_canonical_projects(path: Path, home: Path) -> bool:
    parts = workspace_parts(path, home)
    return bool(parts and len(parts) >= 4 and parts[1] == "2_Work" and parts[2] == "Projects")


def is_under_canonical_library_or_archive(path: Path, home: Path) -> bool:
    parts = workspace_parts(path, home)
    return bool(parts and len(parts) >= 2 and parts[1] in {"3_Library", "4_Archive"})


def is_under_project_state_dir(path: Path, home: Path) -> bool:
    try:
        parts = path.relative_to(home).parts
    except ValueError:
        return False
    return any(part in PROJECT_STATE_DIRS for part in parts)


def has_project_markers(path: Path) -> bool:
    try:
        dirs, files = direct_children(path)
    except OSError:
        return False
    return ".git" in dirs or bool(files & CODE_MARKERS)


def is_inside_detected_project(path: Path, home: Path) -> bool:
    for parent in path.parents:
        if parent == path or parent == home or parent.parent == parent:
            break
        if has_project_markers(parent):
            return True
    return False


def codex_month_for_top_session(path: Path, home: Path) -> str | None:
    try:
        rel_parts = path.relative_to(home / "Documents" / "Codex").parts
    except ValueError:
        return None
    if len(rel_parts) != 1:
        return None
    match = re.match(r"^(20\d{2}-\d{2}-\d{2})", rel_parts[0])
    if not match:
        return None
    return match.group(1)[:7]


def is_nested_codex_session(path: Path, home: Path) -> bool:
    try:
        rel_parts = path.relative_to(home / "Documents" / "Codex").parts
    except ValueError:
        return False
    return len(rel_parts) > 1 and bool(re.match(r"^20\d{2}-\d{2}-\d{2}", rel_parts[0]))


def iter_dirs(root: Path, max_depth: int) -> Iterable[Path]:
    root = root.expanduser()
    if not root.exists() or not root.is_dir():
        return
    root_depth = len(root.parts)
    for current, dirs, _files in os.walk(root):
        path = Path(current)
        depth = len(path.parts) - root_depth
        dirs[:] = [d for d in dirs if d not in GENERATED_DIRS and d != ".git"]
        if depth > max_depth:
            dirs[:] = []
            continue
        yield path


def direct_children(path: Path) -> tuple[set[str], set[str]]:
    dirs: set[str] = set()
    files: set[str] = set()
    try:
        for child in path.iterdir():
            if child.is_dir():
                dirs.add(child.name)
            elif child.is_file():
                files.add(child.name)
    except OSError:
        return dirs, files
    return dirs, files


def count_top_file_exts(path: Path) -> dict[str, int]:
    counts: dict[str, int] = {}
    try:
        for child in path.iterdir():
            if child.is_file():
                suffix = child.suffix.lower()
                if suffix:
                    counts[suffix] = counts.get(suffix, 0) + 1
    except OSError:
        pass
    return counts


def classify(path: Path, home: Path) -> Finding | None:
    pretty = rel_to_home(path, home)
    if path == home or is_under_do_not_touch(path, home):
        return None

    if is_under_project_state_dir(path, home):
        return None

    if is_under_canonical_projects(path, home):
        return None

    if is_under_canonical_library_or_archive(path, home):
        return None

    if is_inside_detected_project(path, home):
        return None

    dirs, files = direct_children(path)
    markers: list[str] = []
    warnings: list[str] = []

    if ".git" in dirs:
        markers.append(".git")
    markers.extend(sorted(files & CODE_MARKERS))
    generated = sorted(dirs & GENERATED_DIRS)
    state_dirs = sorted(dirs & PROJECT_STATE_DIRS)
    if generated:
        warnings.append("contains generated dirs: " + ", ".join(generated))
    if state_dirs:
        warnings.append("contains AI/editor state dirs: " + ", ".join(state_dirs))

    name = path.name.lower()
    path_text = str(path)

    if ".git" in dirs:
        if "mcp" in name or "mcp" in path_text.lower():
            suggestion = "3_Library/Tools/mcp or 2_Work/Projects/mcp"
        elif any(token in path_text.lower() for token in ["tableau", "태블로"]):
            suggestion = "2_Work/Projects/tableau"
        else:
            suggestion = "2_Work/Projects"
        return Finding(pretty, "git-project", suggestion, "medium", "Git repository", markers, warnings)

    if files & CODE_MARKERS:
        if "mcp" in name or "mcp" in path_text.lower():
            suggestion = "3_Library/Tools/mcp or 2_Work/Projects/mcp"
        elif any(token in name for token in ["app", "web", "게임", "노션"]):
            suggestion = "2_Work/Projects/apps"
        else:
            suggestion = "2_Work/Projects"
        return Finding(pretty, "code-project", suggestion, "medium", "Contains project manifest", markers, warnings)

    codex_month = codex_month_for_top_session(path, home)
    if codex_month:
        return Finding(pretty, "ai-lab-session", f"2_Work/Labs/codex/{codex_month}", "low", "Codex dated session folder", markers, warnings)

    if is_nested_codex_session(path, home):
        return None

    codex_session = re.search(r"/Documents/Codex/(20\d{2}-\d{2}-\d{2}-)", path_text)
    if codex_session:
        month = codex_session.group(1)[:7]
        return Finding(pretty, "ai-lab-session", f"2_Work/Labs/codex/{month}", "low", "Codex dated session folder", markers, warnings)

    if "antigravity" in path_text.lower() and "Desktop" in path_text:
        return Finding(pretty, "ai-lab-or-project", "2_Work/Labs/antigravity or 2_Work/Projects", "medium", "Antigravity work area", markers, warnings)

    ext_counts = count_top_file_exts(path)
    if not ext_counts:
        return None

    asset_count = sum(count for ext, count in ext_counts.items() if ext in ASSET_EXTS)
    data_count = sum(count for ext, count in ext_counts.items() if ext in DATA_EXTS)
    doc_count = sum(count for ext, count in ext_counts.items() if ext in DOC_EXTS)

    if data_count >= max(asset_count, doc_count, 1):
        return Finding(pretty, "data-folder", "3_Library/Data", "low", "Top-level files look data-heavy", [], warnings)
    if asset_count >= max(data_count, doc_count, 1):
        return Finding(pretty, "asset-folder", "3_Library/Assets", "low", "Top-level files look asset-heavy", [], warnings)
    if doc_count >= max(data_count, asset_count, 3):
        return Finding(pretty, "knowledge-or-output", "3_Library/Knowledge or 4_Archive/Outputs", "low", "Top-level files look document-heavy", [], warnings)

    return None


def default_roots(home: Path) -> list[Path]:
    candidates = [
        home / "Desktop",
        home / "Downloads",
        home / "Documents",
    ]
    return [p for p in candidates if p.exists()]


def mounted_volume_findings(home: Path) -> list[Finding]:
    volumes = Path("/Volumes")
    if not volumes.exists():
        return []

    findings: list[Finding] = []
    try:
        children = sorted(volumes.iterdir(), key=lambda p: p.name.lower())
    except OSError:
        return findings

    for child in children:
        try:
            resolved = child.resolve()
        except OSError:
            resolved = child
        if child.is_symlink() and resolved == Path("/"):
            continue
        if child.name.startswith("."):
            continue
        findings.append(
            Finding(
                str(child),
                "finder-visible-mounted-volume",
                "verify installed app, eject installer volume, then clean up source .dmg separately",
                "low",
                "Mounted volume may appear on the Desktop but is not a ~/Desktop file or Workspace migration candidate",
                ["mounted-volume"],
                ["do not move /Volumes/* into Workspace"],
            )
        )
    return findings


def render_markdown(findings: list[Finding]) -> str:
    groups: dict[str, list[Finding]] = {}
    for finding in findings:
        groups.setdefault(finding.kind, []).append(finding)

    lines = ["# Workspace Audit", ""]
    lines.append(f"Total findings: {len(findings)}")
    lines.append("")
    for kind in sorted(groups):
        lines.extend([f"## {kind}", ""])
        for item in groups[kind]:
            lines.append(f"- `{item.path}` -> `{item.suggestion}` ({item.risk})")
            lines.append(f"  - reason: {item.reason}")
            if item.markers:
                lines.append(f"  - markers: {', '.join(item.markers)}")
            if item.warnings:
                lines.append(f"  - warnings: {'; '.join(item.warnings)}")
        lines.append("")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Read-only audit for ~/Workspace migration candidates.")
    parser.add_argument("--home", default=str(Path.home()), help="Home directory to scan from.")
    parser.add_argument("--root", action="append", help="Specific root to scan. May be repeated.")
    parser.add_argument("--max-depth", type=int, default=3, help="Maximum directory depth under each root.")
    parser.add_argument("--format", choices=("md", "json"), default="md", help="Output format.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    home = Path(args.home).expanduser().resolve()
    roots = [Path(r).expanduser().resolve() for r in args.root] if args.root else default_roots(home)

    findings: list[Finding] = []
    seen: set[Path] = set()
    for root in roots:
        for path in iter_dirs(root, args.max_depth) or []:
            resolved = path.resolve()
            if resolved in seen:
                continue
            seen.add(resolved)
            finding = classify(resolved, home)
            if finding:
                findings.append(finding)
    findings.extend(mounted_volume_findings(home))

    findings.sort(key=lambda f: (f.kind, f.path))
    if args.format == "json":
        print(json.dumps([asdict(f) for f in findings], ensure_ascii=False, indent=2))
    else:
        print(render_markdown(findings))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
