#!/usr/bin/env python3
"""Project analyzer script for AFAC workspace metrics and file counting."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def analyze_project() -> dict[str, int]:
    metrics = {
        "python_files": len(list(ROOT.glob("**/*.py"))),
        "ts_files": len(list(ROOT.glob("**/*.ts"))) + len(list(ROOT.glob("**/*.tsx"))),
        "markdown_files": len(list(ROOT.glob("**/*.md"))),
    }
    return metrics

def main() -> int:
    metrics = analyze_project()
    print("Project Metrics:")
    for k, v in metrics.items():
        print(f"  {k}: {v}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
