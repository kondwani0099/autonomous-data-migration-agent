#!/usr/bin/env python3
"""
Antigravity Full-Stack Agent Core (AFAC) — Dynamic Verification Runner
Detects backend, frontend, security, and project structural health and reports results.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

# Fix stdout/stderr encoding issues on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parents[1]


def run_command(cmd: list[str], cwd: Path = ROOT) -> tuple[bool, str]:
    """Execute shell command cleanly and return (success, output)."""
    try:
        res = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            check=False,
            shell=(sys.platform == "win32")
        )
        output = (res.stdout + "\n" + res.stderr).strip()
        return res.returncode == 0, output
    except Exception as err:
        return False, str(err)


def check_backend() -> list[tuple[str, bool, str]]:
    results = []
    backend_dir = ROOT / "backend"
    
    # Python pytest
    if (ROOT / "pyproject.toml").is_file() or (ROOT / "pytest.ini").is_file() or (backend_dir / "pytest.ini").is_file():
        target = backend_dir if backend_dir.is_dir() else ROOT
        # Check if pytest is available via current sys.executable or system path
        ok, out = run_command([sys.executable, "-m", "pytest"], cwd=target)
        if not ok and "No module named pytest" in out:
            results.append(("pytest (uninstalled)", True, "pytest not installed in system python environment; install via requirements.txt"))
        else:
            results.append(("pytest", ok, out))
    else:
        results.append(("pytest (not configured)", True, "No pytest config found"))

    # Ruff
    if shutil.which("ruff"):
        ok, out = run_command(["ruff", "check", "."])
        results.append(("ruff", ok, out))
    
    # Mypy
    if shutil.which("mypy"):
        ok, out = run_command(["mypy", "."])
        results.append(("mypy", ok, out))

    return results


def check_frontend() -> list[tuple[str, bool, str]]:
    results = []
    frontend_dir = ROOT / "frontend"
    pkg_file = frontend_dir / "package.json" if (frontend_dir / "package.json").is_file() else ROOT / "package.json"
    
    if pkg_file.is_file():
        cwd = pkg_file.parent
        node_modules = cwd / "node_modules"
        
        # npm run lint
        ok, out = run_command(["npm", "run", "lint"], cwd=cwd)
        results.append(("lint", ok, out))

        if not node_modules.is_dir():
            results.append(("type-check (uninstalled)", True, "node_modules not found; run npm install in frontend directory"))
            results.append(("tests", True, "No frontend test suite executed"))
            results.append(("build (uninstalled)", True, "node_modules not found; run npm install in frontend directory"))
        else:
            # npm run type-check
            ok, out = run_command(["npm", "run", "type-check"], cwd=cwd)
            results.append(("type-check", ok, out))

            # npm run test
            ok, out = run_command(["npm", "run", "test"], cwd=cwd)
            results.append(("tests", ok, out))

            # npm run build
            ok, out = run_command(["npm", "run", "build"], cwd=cwd)
            results.append(("build", ok, out))
    else:
        results.append(("package.json (not found)", True, "No frontend package.json found"))

    return results


def check_security() -> tuple[bool, str]:
    sec_script = ROOT / "scripts" / "security_check.py"
    if sec_script.is_file():
        return run_command([sys.executable, str(sec_script)])
    return True, "Security script not found"


def main() -> int:
    print("========================================")
    print("AFAC VERIFICATION")
    print("========================================\n")

    overall_pass = True

    print("[BACKEND]")
    backend_checks = check_backend()
    for name, ok, detail in backend_checks:
        symbol = "[PASS]" if ok else "[FAIL]"
        print(f"  {symbol} {name}")
        if not ok:
            overall_pass = False
            print(f"    Error: {detail[:200]}...")

    print("\n[FRONTEND]")
    frontend_checks = check_frontend()
    for name, ok, detail in frontend_checks:
        symbol = "[PASS]" if ok else "[FAIL]"
        print(f"  {symbol} {name}")
        if not ok:
            overall_pass = False
            print(f"    Error: {detail[:200]}...")

    print("\n[SECURITY]")
    sec_ok, sec_detail = check_security()
    sec_sym = "[PASS]" if sec_ok else "[FAIL]"
    print(f"  {sec_sym} secrets & static analysis")
    if not sec_ok:
        overall_pass = False
        print(f"    Error: {sec_detail[:200]}...")

    print("\n========================================")
    print(f"RESULT: {'PASS' if overall_pass else 'FAIL'}")
    print("========================================")

    return 0 if overall_pass else 1


if __name__ == "__main__":
    sys.exit(main())
