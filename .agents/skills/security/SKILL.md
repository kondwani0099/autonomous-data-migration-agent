---
name: security
description: Security auditing directives, secret scanning, input validation, SQL injection prevention, and vulnerability classification.
---

# Security Skill Directive

<SECURITY_DIRECTIVES>
1. **Secret Scanning**: Verify no passwords, API tokens, JWT secrets, or cloud keys are present in code or `.env` files.
2. **Parameterized Queries**: Verify ORM / SQL calls prevent SQL injection vulnerabilities.
3. **Authentication & Authorization**: Verify endpoints enforce security dependencies (`get_current_user`, `get_current_active_admin`).
4. **Input Sanitization**: Validate API payloads via Pydantic schemas and sanitize UI inputs against XSS.
5. **Classify Severity**: Mark issues as `CRITICAL`, `HIGH`, `MEDIUM`, `LOW`, or `INFO`. Block delivery on `CRITICAL` or `HIGH`.
</SECURITY_DIRECTIVES>
