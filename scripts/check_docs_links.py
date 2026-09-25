#!/usr/bin/env python3
"""Check relative Markdown links across the ecosystem checkout."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LINK_RE = re.compile(r"!?\[[^\]]*\]\((<[^>]+>|[^)]+)\)")
HTML_SRC_RE = re.compile(r"<img\b[^>]*\bsrc=[\"']([^\"']+)[\"']", re.IGNORECASE)
URL_RE = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*:")


def targets(markdown: str):
    for match in LINK_RE.finditer(markdown):
        target = match.group(1).strip()
        if target.startswith("<") and target.endswith(">"):
            target = target[1:-1]
        else:
            target = target.split(maxsplit=1)[0]
        yield target
    yield from HTML_SRC_RE.findall(markdown)


def main() -> int:
    errors: list[str] = []
    for path in sorted(ROOT.rglob("*.md")):
        if ".git" in path.parts:
            continue
        markdown = path.read_text(encoding="utf-8")
        for target in targets(markdown):
            target = target.strip()
            if not target or target.startswith("#") or URL_RE.match(target):
                continue
            target_path = target.split("#", maxsplit=1)[0].split("?", maxsplit=1)[0]
            if not target_path:
                continue
            if Path(target_path).is_absolute():
                errors.append(f"{path.relative_to(ROOT)}: absolute local link: {target}")
                continue
            resolved = (path.parent / target_path).resolve()
            if not resolved.exists():
                errors.append(f"{path.relative_to(ROOT)}: missing target: {target}")

    if errors:
        print("Markdown link check failed:", file=sys.stderr)
        print("\n".join(f"- {error}" for error in errors), file=sys.stderr)
        return 1
    print("Markdown links are valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
