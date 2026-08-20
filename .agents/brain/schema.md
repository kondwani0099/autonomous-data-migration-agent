# AFAC v1.0.0 State Contracts

## Active Plan

`docs/plans/<slug>.md` is required for multi-file/architectural work. It contains `## Decisions` and a `## Tasks` checklist. Completed plans are archived or tracked in `TASKS.md`.

## Antigravity Files

- `.agents/agents/<name>.md`: custom sub-agent persona with YAML frontmatter `name`, `description`, and `mode`.
- `.agents/skills/<name>/SKILL.md`: concise domain skill with YAML frontmatter `name` and `description`.
- `.agents/mcp_config.json`: workspace MCP config using `mcpServers`; remote servers use `serverUrl`.
- `.agents/antigravity-settings.example.json`: global settings example; copy manually to the Antigravity settings path.

## Verification

`python scripts/verify.py` detects the stack and reports checks across backend, frontend, and security static audits.
