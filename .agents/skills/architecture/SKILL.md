---
name: architecture
description: Guidelines for system design, layer isolation, Big-O analysis, statelessness, and Architecture Decision Records (ADR).
---

# Architecture Skill Directive

<ENTERPRISE_STANDARDS>
1. **Scalability (Big-O)**: Analyze time and space complexity of loops, database queries, and caching strategies. Ensure operations scale linearly or logarithmically.
2. **Statelessness**: Enforce stateless service layers. Application servers must be capable of horizontal scaling behind a load balancer without localized state corruption.
3. **Database Performance**: Mandate index utilization for frequent queries. Actively prevent and eliminate N+1 query patterns in ORMs.
4. **Separation of Concerns**: Enforce strict module isolation (routing controllers, business domain logic, data access layers).
</ENTERPRISE_STANDARDS>

<PROCEDURAL_WORKFLOW>
1. **Impact Analysis**: Use code search (`grep_search`) to locate all consumers of the modified schema, interface, or module.
2. **Draft the Contract**: Write proposed schema/API contract.
3. **Review against Constraints**:
   - Is it backwards compatible?
   - Does it violate existing bounded contexts?
   - Does it introduce new stateful dependencies?
4. **ADR Approval**: Present an Architecture Decision Record (ADR) detailing the Blast Radius in `docs/architecture/` before major structural changes.
</PROCEDURAL_WORKFLOW>
