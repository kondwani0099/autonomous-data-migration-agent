# AGENTS.md — Source of Truth Policy

> **HIGHEST-PRIORITY PROJECT POLICY**
> You MUST read and strictly obey this document before reading any other file or executing any repository change.

---

## 1. Core Engineering Philosophy

AFAC follows a strict, non-negotiable execution protocol:

```text
UNDERSTAND → EXPLORE → PLAN → APPROVE → ACT → VERIFY → REVIEW → DOCUMENT
```

Never default to anti-patterns:
```text
PROMPT → GENERATE CODE → "Done" (FORBIDDEN)
```

---

## 2. Non-Negotiable Rules

### General Rules
1. **Understand Existing Code**: Inspect existing logic, schemas, and dependencies before writing code.
2. **Never Assume Architecture**: Verify contracts and patterns in code via search before making architectural assumptions.
3. **Search Before Creating**: Always search the codebase using `grep_search` before creating new helper functions, utilities, or components.
4. **Reuse Existing Abstractions**: Utilize existing services, utilities, and components instead of re-inventing custom solutions.
5. **Avoid Unnecessary Dependencies**: Do not introduce new third-party packages unless explicitly justified and approved.
6. **Strict Scope Boundaries**: Keep all edits strictly within the user's requested scope.
7. **No Unrelated Refactoring**: Do not touch, clean up, or reformat unrelated files.
8. **Never Silently Change Architecture**: Any structural change requires an Architecture Decision Record (ADR) and explicit human approval.
9. **Never Expose Secrets**: Never commit `.env` files, API keys, tokens, or print credentials to logs.
10. **Mandatory Verification**: Never claim success without empirical runtime verification output from `scripts/verify.py`.

### Critical Prohibitions
Agents must NEVER:
- Fabricate test results or claim a browser test was executed when it was not.
- Claim code was reviewed when it was not.
- Perform destructive database migrations or schema drops without explicit human approval.
- Rewrite unrelated code modules to work around test failures.
- Disable security controls or suppress failing tests to force a green build.
- Modify files outside the task's allowed boundary without prior authorization.

---

## 3. Scope Analysis Protocol

Before initiating implementation, the agent MUST explicitly identify:
```text
1. Requested Scope    : Exact user requirements
2. Affected Files     : Exact list of target files
3. Dependencies       : Related modules/schemas to inspect
4. Side Effects       : Potential impact on API contracts or database models
5. Out-of-Scope Areas : Explicitly prohibited modification zones
```

---

## 4. Delivery Protocol Phases

1. **EXPLORE**: Use `grep_search` and `view_file` to thoroughly map code flow, signatures, and dependencies.
2. **PLAN**: Draft an implementation plan (`docs/plans/<task-name>.md`) detailing objective, changes, risks, and acceptance criteria. Obtain approval for non-trivial tasks.
3. **ACT**: Perform minimal, incremental changes. Follow backend/frontend conventions in `INSTRUCTIONS.md`.
4. **VERIFY**: Run `python scripts/verify.py` and run stack-specific tests (`pytest`, `vitest`, `mypy`, `ruff`, `eslint`).
5. **REVIEW**: Conduct diff inspection (`git diff`) to ensure zero scope leakage or unintended modifications.
6. **DOCUMENT**: Update `docs/walkthroughs/` and produce a structured final report.

---

## 5. Mandatory Sub-Agent Invocation

For specialized tasks, delegate to the appropriate sub-agent persona in `.agents/agents/`:
- **Planning & Strategy**: `planner.md`
- **Implementation**: `implementer.md`
- **Diff & Contract Audit**: `reviewer.md`
- **Security Audit**: `security-auditor.md`
- **Backend & Database**: `backend-specialist.md`
- **Frontend & UI**: `frontend-specialist.md`
- **Testing & Coverage**: `testing-specialist.md`
- **End-to-End Workflow**: `browser-tester.md`

---

<div align="center">
  <sub>AFAC Source of Truth Policy — Enforced for all Antigravity Sessions</sub>
</div>
