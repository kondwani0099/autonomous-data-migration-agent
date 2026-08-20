#!/usr/bin/env python3
"""Security check script for secret scanning and input validation baseline."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SECRET_PATTERNS = [
    re.compile(r"AIzaSy[A-Za-z0-9_-]{33}"),  # Google API key
    re.compile(r"sk-[A-Za-z0-9]{32,}"),       # OpenAI API key
    re.compile(r"ghp_[A-Za-z0-9]{36}"),       # GitHub Personal Access Token
]

def scan_secrets() -> list[str]:
    violations = []
    for path in ROOT.glob("**/*"):
        IGNORED_PARTS = {".git", "node_modules", "venv", "env", ".venv", "dist", "build", ".agents"}
        if path.is_file() and not (set(path.parts) & IGNORED_PARTS):
            try:
                content = path.read_text(encoding="utf-8", errors="ignore")
                for pattern in SECRET_PATTERNS:
                    if pattern.search(content):
                        violations.append(f"Potential secret detected in {path.relative_to(ROOT)}")
            except Exception:
                pass
    return violations

def main() -> int:
    violations = scan_secrets()
    if violations:
        for v in violations:
            print(f"SECURITY FAIL: {v}")
        return 1
    print("Security Check: PASS (No exposed secrets found)")
    return 0

if __name__ == "__main__":
    sys.exit(main())
