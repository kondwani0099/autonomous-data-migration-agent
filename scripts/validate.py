#!/usr/bin/env python3
"""Validate AFAC's Antigravity workspace contracts without third-party packages."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

# Fix stdout/stderr encoding issues on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_PATHS = (
    "AGENTS.md",
    "README.md",
    "INSTRUCTIONS.md",
    "ARCHITECTURE.md",
    "SECURITY.md",
    "TASKS.md",
    "CHANGELOG.md",
    "GEMINI.md",
    "install.sh",
    "install.ps1",
    ".agents/config.json",
    ".agents/TASK_TEMPLATE.md",
    ".agents/brain/soul.md",
    ".agents/brain/rules.md",
    ".agents/brain/schema.md",
    ".agents/brain/env-required.json",
    ".agents/common/utils.md",
    ".agents/mcp_config.json.example",
    ".agents/antigravity-settings.example.json",
    ".agents/antigravity-compatibility.json",
    ".agents/agents/planner.md",
    ".agents/agents/implementer.md",
    ".agents/agents/reviewer.md",
    ".agents/agents/security-auditor.md",
    ".agents/agents/backend-specialist.md",
    ".agents/agents/frontend-specialist.md",
    ".agents/agents/testing-specialist.md",
    ".agents/agents/browser-tester.md",
    ".agents/skills/architecture/SKILL.md",
    ".agents/skills/fastapi/SKILL.md",
    ".agents/skills/vue/SKILL.md",
    ".agents/skills/database/SKILL.md",
    ".agents/skills/security/SKILL.md",
    ".agents/skills/testing/SKILL.md",
    ".agents/skills/code-quality/SKILL.md",
    ".agents/skills/verification/SKILL.md",
    "scripts/validate.py",
    "scripts/verify.py",
    "scripts/project_analyzer.py",
    "scripts/security_check.py",
    "scripts/generate_report.py",
)


def fail(message: str) -> None:
    raise ValueError(message)


def load_json(relative_path: str) -> dict:
    path = ROOT / relative_path
    try:
        with path.open(encoding="utf-8") as handle:
            value = json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"invalid JSON in {relative_path}: {exc}")
    if not isinstance(value, dict):
        fail(f"{relative_path} must contain a JSON object")
    return value


def validate_mcp() -> None:
    target = ".agents/mcp_config.json" if (ROOT / ".agents/mcp_config.json").is_file() else ".agents/mcp_config.json.example"
    config = load_json(target)
    servers = config.get("mcpServers")
    if not isinstance(servers, dict) or not servers:
        fail("MCP config must define mcpServers")
    for name, server in servers.items():
        if not isinstance(server, dict):
            fail(f"MCP server {name} must be an object")
        if "serverURL" in server:
            fail(f"MCP server {name} uses deprecated serverURL; use serverUrl")
        if "serverUrl" not in server and "command" not in server:
            fail(f"MCP server {name} needs serverUrl or command")


def validate_markdown_metadata(directory: str, expected_count: int, required_fields: tuple[str, ...], pattern: str = "*.md") -> None:
    files = sorted((ROOT / directory).glob(pattern))
    if len(files) != expected_count:
        fail(f"expected {expected_count} files in {directory}, found {len(files)}")
    for path in files:
        content = path.read_text(encoding="utf-8")
        match = re.match(r"^---\n(?P<frontmatter>.*?)\n---\n", content, re.DOTALL)
        if not match:
            fail(f"{path.relative_to(ROOT)} is missing YAML frontmatter")
        frontmatter = match.group("frontmatter")
        for field in required_fields:
            if not re.search(rf"^{field}:\s*\S+", frontmatter, re.MULTILINE):
                fail(f"{path.relative_to(ROOT)} is missing frontmatter {field}")


def validate_instruction_budget() -> None:
    bootstrap = (ROOT / "GEMINI.md").read_text(encoding="utf-8")
    if "AGENTS.md" not in bootstrap:
        fail("GEMINI.md must bootstrap AGENTS.md")


def validate_settings() -> None:
    settings = load_json(".agents/antigravity-settings.example.json")
    required = {
        "toolPermission": "proceed-in-sandbox",
        "enableTerminalSandbox": True,
        "allowNonWorkspaceAccess": False,
        "artifactReviewPolicy": "asks-for-review",
    }
    for key, expected in required.items():
        if settings.get(key) != expected:
            fail(f"settings baseline must set {key}={expected!r}")


def validate_compatibility() -> None:
    compatibility = load_json(".agents/antigravity-compatibility.json")
    if not re.fullmatch(r"\d+\.\d+\.\d+", str(compatibility.get("cli_version"))):
        fail("compatibility cli_version must be semantic version text")
    if not compatibility.get("official_docs"):
        fail("compatibility must list official Antigravity documentation URLs")


def validate_manifest() -> None:
    for relative_path in REQUIRED_PATHS:
        if not (ROOT / relative_path).is_file():
            fail(f"missing required file: {relative_path}")


def validate_version() -> None:
    config = load_json(".agents/config.json")
    version = config.get("core_version")
    if not isinstance(version, str) or not re.fullmatch(r"\d+\.\d+\.\d+", version):
        fail("config.json core_version must be semantic version text")
    markers = {
        "README.md": f"version-{version}",
        "install.sh": f'AFAC_REF="v{version}"',
        "install.ps1": f'$AfacRef = "v{version}"',
        ".agents/TASK_TEMPLATE.md": f"AFAC v{version}",
    }
    for relative_path, marker in markers.items():
        content = (ROOT / relative_path).read_text(encoding="utf-8")
        if marker not in content:
            fail(f"{relative_path} does not contain version marker {marker}")
    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    if f"## [{version}]" not in changelog:
        fail(f"CHANGELOG.md does not contain release heading [{version}]")


def main() -> int:
    try:
        validate_manifest()
        load_json(".agents/config.json")
        load_json(".agents/brain/env-required.json")
        load_json(".agents/antigravity-compatibility.json")
        validate_mcp()
        validate_markdown_metadata(".agents/skills", 9, ("name", "description"), "*/SKILL.md")
        validate_markdown_metadata(".agents/agents", 9, ("name", "description", "mode"))
        validate_instruction_budget()
        validate_settings()
        validate_compatibility()
        validate_version()
    except ValueError as exc:
        print(f"FAIL: {exc}")
        return 1
    print("AFAC Antigravity structural validation: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
