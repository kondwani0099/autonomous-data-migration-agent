---
name: testing
description: Guidance for backend pytest strategies, frontend Vitest testing, API contract validation, and edge case coverage.
---

# Testing Skill Directive

<GUIDELINES>
1. **Backend Testing (`pytest`)**: Write tests in `backend/tests/`. Cover API routes, authentication workflows, service logic, and database operations using test fixtures.
2. **Frontend Testing (`Vitest`)**: Write unit and component tests in `frontend/tests/`. Cover Pinia stores, composables, and component rendering.
3. **API Contract Validation**: Verify backend response models match frontend TypeScript interfaces.
4. **Edge Case Coverage**: Test invalid inputs, missing fields, unauthorized requests, expired tokens, and boundary conditions.
5. **No Test Suppression**: Never comment out failing assertions or delete tests to force a green build.
</GUIDELINES>
