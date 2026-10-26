#!/usr/bin/env python3
"""Checks catalog.json (standard library only). Exit code 1 when something is wrong."""
import json
import re
import sys
from pathlib import Path

root = Path(__file__).resolve().parent
errors, warnings = [], []
try:
    cat = json.loads((root / "catalog.json").read_text("utf-8"))
except (OSError, ValueError) as e:
    sys.exit(f"catalog.json cannot be read: {e}")

ID = re.compile(r"[\w.-]{1,40}")
seen = set()
for kind, req in (("forks", ("id", "name", "repo", "description")),
                  ("patches", ("id", "titleId", "game", "name", "version", "description"))):
    for i, e in enumerate(cat.get(kind, [])):
        where = f"{kind}[{i}] {e.get('id', '?')}"
        for k in req:
            if not e.get(k):
                errors.append(f"{where}: missing '{k}'")
        if not ID.fullmatch(str(e.get("id", ""))):
            errors.append(f"{where}: bad id")
        if (kind, e.get("id")) in seen:
            errors.append(f"{where}: duplicate id")
        seen.add((kind, e.get("id")))
        if kind == "forks":
            if not re.fullmatch(r"[\w.-]+/[\w.-]+", str(e.get("repo", ""))):
                errors.append(f"{where}: repo must look like owner/repo")
        else:
            if not re.fullmatch(r"[A-Z]{4}\d{5}", str(e.get("titleId", ""))):
                errors.append(f"{where}: titleId must look like PPSA21564")
            if not (e.get("file") or e.get("url")):
                errors.append(f"{where}: needs 'file' or 'url'")
            if e.get("file") and (".." in e["file"] or e["file"].startswith("/")):
                errors.append(f"{where}: 'file' must be a relative path inside the repository")
            if not re.fullmatch(r"[0-9a-fA-F]{64}", str(e.get("sha256", ""))):
                errors.append(f"{where}: 'sha256' (64 hex characters) is required so Studio can verify the file")
            if e.get("file") and not (root / e["file"]).is_file():
                warnings.append(f"{where}: {e['file']} is not in this repository (fine if authors did not allow redistribution)")
for w in warnings:
    print("warning:", w)
for e in errors:
    print("error:  ", e)
print(f"{len(cat.get('forks', []))} forks, {len(cat.get('patches', []))} patches, {len(errors)} error(s), {len(warnings)} warning(s)")
sys.exit(1 if errors else 0)
