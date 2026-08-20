---
name: verification
description: Verification workflow execution, stack detection, runner execution via verify.py, and evidence logging.
---

# Verification Skill Directive

<VERIFICATION_WORKFLOW>
1. **Trigger Runner**: Execute `python scripts/verify.py` after code modifications.
2. **Inspect Output**: Check backend tests (`pytest`), linters (`ruff`, `eslint`), type checkers (`mypy`), and build tools (`npm run build`).
3. **Self-Healing Loop**: If verification fails within the requested scope, fix the underlying issue and re-run tests. Maximum automated retry attempts: 3.
4. **Report Failure**: If a failure cannot be resolved or requires out-of-scope changes, stop and report details to the user with exact logs.
</VERIFICATION_WORKFLOW>
