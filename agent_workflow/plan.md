# Agent Workflow Plan: Conway's Law + VSM Integration

## Purpose
- Establish shared coordination scaffolding so specialized SemOps agents can operate safely.
- Map agent responsibilities to Conway-aligned interfaces and the Viable System Model (VSM).
- Ensure communication patterns mirror organizational structure (Conway's Law).
- Implement viable system model for sustainable agent collaboration.

## Conway's Law Integration Principles

### System Boundary Alignment
**Conway's Law**: "Organizations design systems that mirror their communication structure."

- **Agent boundaries** align with **interface boundaries** to minimize cross-cutting concerns
- **Communication patterns** between agents match **protocol definitions** in contracts
- **Responsibility ownership** follows **system module boundaries** to reduce coordination overhead

### Interface Ownership Mapping
```
Schema Agent ↔ Protobuf Schema Boundaries
Service Agent ↔ gRPC Service Boundaries
CLI Agent ↔ Command Interface Boundaries
Knowledge Agent ↔ Template/RAG Boundaries
Ops/QA Agent ↔ Pipeline/Testing Boundaries
```

### Communication Architecture
- **Formal interfaces** (ICS contracts) for high-stakes coordination
- **Informal channels** (handoffs, notifications) for operational coordination
- **Escalation paths** when boundary violations occur

## Phase 0 – Foundations 
1. **Contract Baseline**
   - Draft ICS-001 … ICS-007 interface contracts (schema↔service, service↔CLI, templates, knowledge ops, docs, tooling, handoffs).
   - Store contracts in `contracts/` with version headers and `#contract-change` workflow.
2. **Shared Tooling Guardrails**
   - Finalize `scripts/test-runner.sh`, Buf pipelines, and git hooks.
   - Add CI job that hashes contract docs and enforces handoff notes.
3. **Handoff Template**
   - Create `handoffs/handoff-template.md` with required fields (inputs, outputs, tests, contract version, next agent).

## VSM Framework Implementation

### System 1: Operational Units (Specialized Agents)
Each agent owns a specific system boundary and interface contract:

#### Schema Agent (System 1a) - Proto Boundary Owner
- **Primary Responsibility**: Protobuf schema evolution and validation
- **Interface Contracts**: ICS-001 (Schema↔Service), ICS-007 (Handoffs)
- **Communication Pattern**: Schema changes → Service Agent notification → Validation
- **Boundary**: All `.proto` files, `buf.lock`, protovalidate annotations
- **Viability Metrics**: Schema compilation success, breaking change detection

#### Service Agent (System 1b) - Business Logic Boundary Owner
- **Primary Responsibility**: gRPC service implementation and business logic
- **Interface Contracts**: ICS-001 (Schema↔Service), ICS-002 (Service↔CLI)
- **Communication Pattern**: Schema updates → Service implementation → CLI generation
- **Boundary**: All gRPC service implementations, business logic, data persistence
- **Viability Metrics**: Service health, test coverage, performance benchmarks

#### CLI Agent (System 1c) - User Interface Boundary Owner
- **Primary Responsibility**: Dynamic command generation and user experience
- **Interface Contracts**: ICS-002 (Service↔CLI), ICS-006 (Docs)
- **Communication Pattern**: Service changes → CLI regeneration → User documentation
- **Boundary**: Command definitions, help text, output formatting, user workflows
- **Viability Metrics**: Command success rate, user error frequency, help relevance

#### Knowledge Agent (System 1d) - Template/RAG Boundary Owner
- **Primary Responsibility**: Template management and knowledge operations
- **Interface Contracts**: ICS-003 (Templates), ICS-004 (Knowledge Ops)
- **Communication Pattern**: Entity changes → Template updates → Knowledge indexing
- **Boundary**: Jinja2 templates, RAG workflows, knowledge ingestion, vector stores
- **Viability Metrics**: Template compilation, knowledge retrieval accuracy, ingestion throughput

#### Ops/QA Agent (System 1e) - Pipeline Boundary Owner
- **Primary Responsibility**: CI/CD pipeline health and quality assurance
- **Interface Contracts**: ICS-005 (Tooling), ICS-007 (Handoffs)
- **Communication Pattern**: Code changes → Pipeline validation → Release packaging
- **Boundary**: Test runners, CI/CD configs, deployment scripts, monitoring
- **Viability Metrics**: Pipeline success rate, test coverage, deployment frequency

### System 2: Coordination Mechanisms
- **Contract Change Notifications**: Automated alerts when ICS contracts are modified
- **Handoff Validation**: Automated verification that handoff requirements are met
- **Workload Balancing**: Monitor agent capacity and distribute tasks accordingly
- **Conflict Resolution**: Escalation path when agents disagree on boundary ownership

### System 3: Control and Audit
- **Contract Maintainer Rotation**: Rotate responsibility for contract governance
- **Merge Gate Enforcement**: Block merges that violate contract requirements
- **Quarterly Audits**: Verify contract compliance and boundary integrity
- **Performance Monitoring**: Track viability metrics across all agents

### System 4: Intelligence and Strategy
- **Architecture Working Group**: Monitor system evolution and future interface needs
- **Backlog Grooming**: Prioritize work based on system viability requirements
- **Trend Analysis**: Identify patterns in contract violations and boundary disputes
- **Future Planning**: Anticipate new agent roles and interface requirements

### System 5: Policy and Identity
- **SemOps Charter**: "Proto-first, agent-safe, VSM-aligned"
- **Governance Policies**: Rules for contract changes, agent onboarding, boundary disputes
- **Identity Management**: Clear role definitions and authority boundaries
- **Cultural Norms**: Principles for agent collaboration and conflict resolution

## Interface Contract Specifications (ICS)

### ICS-001: Schema↔Service Contract
**Purpose**: Define protobuf schema evolution and service implementation coordination
**Owner**: Schema Agent (primary) + Service Agent (secondary)
**Scope**: Protobuf files, generated code, service implementations

**Contract Requirements**:
- Schema changes MUST include impact analysis and migration path
- Breaking changes MUST follow semantic versioning and deprecation timeline
- Service implementation MUST validate against schema before merge
- Generated code MUST NOT be manually edited (protobuf-first principle)

**Handoff Protocol**: Schema Agent validates → Service Agent implements → QA Agent tests

### ICS-002: Service↔CLI Contract
**Purpose**: Ensure CLI commands stay synchronized with service capabilities
**Owner**: Service Agent (primary) + CLI Agent (secondary)
**Scope**: gRPC service methods, CLI command generation, user interfaces

**Contract Requirements**:
- New service methods MUST have corresponding CLI commands generated
- CLI parameter validation MUST match service validation rules
- Error messages MUST be user-friendly and actionable
- Help text MUST reflect current service capabilities

**Handoff Protocol**: Service Agent exposes → CLI Agent generates → Knowledge Agent documents

### ICS-003: Template Contract
**Purpose**: Maintain consistency across entity templates and rendering
**Owner**: Knowledge Agent (primary) + Schema Agent (secondary)
**Scope**: Jinja2 templates, entity schemas, template variables

**Contract Requirements**:
- Template variables MUST be defined in protobuf schemas
- Template syntax MUST be validated before deployment
- Template changes MUST include sample outputs and test cases
- Entity frontmatter MUST conform to schema definitions

**Handoff Protocol**: Schema Agent defines → Knowledge Agent implements → CLI Agent validates

### ICS-004: Knowledge Operations Contract
**Purpose**: Coordinate knowledge ingestion, indexing, and retrieval
**Owner**: Knowledge Agent (primary) + Service Agent (secondary)
**Scope**: RAG workflows, vector stores, knowledge sources, retrieval APIs

**Contract Requirements**:
- Knowledge sources MUST have stable, deterministic IDs
- Ingestion pipelines MUST handle schema evolution gracefully
- Retrieval APIs MUST provide provenance and confidence scores
- Knowledge updates MUST preserve entity relationship integrity

**Handoff Protocol**: Service Agent triggers → Knowledge Agent processes → QA Agent validates

### ICS-005: Tooling Contract
**Purpose**: Maintain shared development and deployment tooling
**Owner**: Ops/QA Agent (primary) + All Agents (secondary)
**Scope**: CI/CD pipelines, test frameworks, build tools, deployment scripts

**Contract Requirements**:
- Tool changes MUST be backward compatible or include migration path
- Pipeline failures MUST provide actionable error messages and remediation steps
- Testing frameworks MUST cover all interface contracts
- Deployment processes MUST be idempotent and rollback-capable

**Handoff Protocol**: Any Agent requests → Ops/QA Agent implements → All Agents validate

### ICS-006: Documentation Contract
**Purpose**: Ensure documentation stays current with system capabilities
**Owner**: CLI Agent (primary) + Knowledge Agent (secondary)
**Scope**: User documentation, API docs, architecture docs, runbooks

**Contract Requirements**:
- Documentation MUST be generated from authoritative sources (schemas, code)
- User guides MUST include working examples and common workflows
- API documentation MUST reflect current service capabilities
- Architecture docs MUST be updated when interface contracts change

**Handoff Protocol**: Any Agent changes → CLI Agent updates → Knowledge Agent reviews

### ICS-007: Handoff Contract
**Purpose**: Standardize work handoffs between agents
**Owner**: All Agents (shared responsibility)
**Scope**: Task transitions, work validation, communication protocols

**Contract Requirements**:
- All handoffs MUST include: inputs, outputs, tests, contract version, next agent
- Handoff recipients MUST acknowledge within 1 business day
- Handoff failures MUST escalate to System 3 (Control) for resolution
- Handoff metrics MUST be tracked for system health monitoring

**Handoff Protocol**: Originating Agent prepares → Receiving Agent validates → QA Agent monitors

## Agent Capability Matrix & RACI Mappings

### RACI Matrix: Interface Contract Ownership

| Contract | Schema Agent | Service Agent | CLI Agent | Knowledge Agent | Ops/QA Agent |
|----------|-------------|---------------|-----------|-----------------|---------------|
| ICS-001 (Schema↔Service) | **R**esponsible | **A**ccountable | Informed | Informed | **C**onsulted |
| ICS-002 (Service↔CLI) | Informed | **R**esponsible | **A**ccountable | Consulted | Consulted |
| ICS-003 (Template) | **A**ccountable | Informed | Consulted | **R**esponsible | Consulted |
| ICS-004 (Knowledge Ops) | Consulted | **A**ccountable | Informed | **R**esponsible | Consulted |
| ICS-005 (Tooling) | Consulted | Consulted | Consulted | Consulted | **R**/**A** |
| ICS-006 (Documentation) | Informed | Informed | **R**esponsible | **A**ccountable | Consulted |
| ICS-007 (Handoffs) | **R** | **R** | **R** | **R** | **A** |

**Legend**: R = Responsible (does the work), A = Accountable (ensures completion), C = Consulted (input sought), I = Informed (kept updated)

### Agent Interaction Protocols

#### Schema Agent Capabilities
- **Input Processing**: Protobuf schema modifications, validation rule updates
- **Output Generation**: Compiled schemas, generated types, breaking change reports
- **Communication**: Formal notifications to Service Agent for implementation impact
- **Escalation**: Breaking changes require Architecture Working Group approval
- **Tools**: `buf`, protobuf compiler, validation generators, schema linters

#### Service Agent Capabilities
- **Input Processing**: Schema updates, business logic requirements, API specifications
- **Output Generation**: gRPC service implementations, business logic, data models
- **Communication**: Service capability announcements to CLI Agent for command generation
- **Escalation**: Performance issues or scalability concerns to Ops/QA Agent
- **Tools**: gRPC frameworks, service testing, performance monitoring, database tools

#### CLI Agent Capabilities
- **Input Processing**: Service method definitions, user experience requirements
- **Output Generation**: CLI commands, help text, output formatters, user workflows
- **Communication**: User feedback and usability reports to Service Agent
- **Escalation**: Complex UX requirements to Architecture Working Group
- **Tools**: CLI frameworks, command generators, user testing, documentation tools

#### Knowledge Agent Capabilities
- **Input Processing**: Entity schema changes, template requirements, knowledge sources
- **Output Generation**: Jinja2 templates, RAG workflows, knowledge indexes, retrieval APIs
- **Communication**: Template capability updates to CLI Agent for user guidance
- **Escalation**: Knowledge quality issues to Architecture Working Group
- **Tools**: Template engines, vector databases, RAG frameworks, knowledge validators

#### Ops/QA Agent Capabilities
- **Input Processing**: Code changes, deployment requirements, quality metrics
- **Output Generation**: CI/CD pipelines, test results, deployment packages, monitoring dashboards
- **Communication**: Pipeline status and quality reports to all agents
- **Escalation**: System-wide failures to System 3 (Control) for immediate attention
- **Tools**: CI/CD platforms, testing frameworks, monitoring tools, deployment automation

### Agent Onboarding Protocol
1. **Capability Assessment**: Verify agent has required tools and skills for assigned contracts
2. **Boundary Training**: Ensure agent understands interface ownership and communication patterns
3. **Contract Validation**: Test agent's ability to fulfill contract requirements in sandbox environment
4. **Integration Testing**: Verify agent can successfully hand off work to other agents
5. **Production Readiness**: Confirm agent can handle failure scenarios and escalation procedures

### Conflict Resolution Procedures
1. **Boundary Disputes**: When agents disagree on interface ownership
   - Escalate to Contract Maintainer for clarification
   - If unresolved, escalate to Architecture Working Group
   - Document resolution and update interface contracts

2. **Quality Disagreements**: When agents have different quality standards
   - Escalate to QA Agent for authoritative quality determination
   - If systemic, escalate to System 3 (Control) for policy clarification
   - Update quality criteria in relevant contracts

3. **Resource Conflicts**: When agents compete for shared resources
   - Escalate to System 2 (Coordination) for workload balancing
   - If persistent, escalate to System 4 (Intelligence) for capacity planning
   - Implement resource allocation policies

## Phase 1 – Agent Roles Implementation

## Enhanced Coordination Mechanisms

### Automated Handoff Validation
- **Handoff Completeness Check**: CI validates all required fields are present
- **Contract Version Verification**: Ensure handoff references current contract versions
- **Dependency Validation**: Verify prerequisite work is completed before accepting handoff
- **Quality Gate Enforcement**: Block handoffs that don't meet quality criteria

### Contract Change Impact Analysis
- **Dependency Mapping**: Automatically identify which agents are affected by contract changes
- **Impact Assessment**: Generate reports showing scope and risk of changes
- **Notification Cascade**: Alert affected agents in order of dependency
- **Migration Planning**: Provide automated migration recommendations

### Workload Coordination
- **Capacity Monitoring**: Track agent workload and availability
- **Priority Balancing**: Distribute high-priority work across agents
- **Bottleneck Detection**: Identify and resolve coordination bottlenecks
- **Load Shedding**: Automatic task redistribution when agents are overloaded

### Communication Protocols
- **Formal Channels**: Contract changes, escalations, policy updates
- **Informal Channels**: Status updates, quick questions, coordination needs
- **Emergency Channels**: System failures, security issues, urgent escalations
- **Archive Channels**: Historical decisions, lessons learned, reference materials

## Enhanced Handoff Protocols

### Standard Handoff Template
```yaml
handoff_id: "HO-{timestamp}-{originating_agent}-{receiving_agent}"
originating_agent: "{agent_name}"
receiving_agent: "{agent_name}"
contract_version: "{ICS-XXX-v1.2.3}"
priority: "{high|medium|low}"
estimated_effort: "{hours}"

inputs:
  - artifact: "{path/to/input}"
    description: "{what this input contains}"
    validation: "{how to verify input quality}"

outputs_required:
  - artifact: "{path/to/expected/output}"
    description: "{what output should contain}"
    acceptance_criteria: "{how to validate completion}"

tests_required:
  - test_type: "{unit|integration|contract}"
    description: "{what needs to be tested}"
    success_criteria: "{how to determine test passes}"

dependencies:
  - dependency: "{prerequisite work}"
    status: "{completed|in_progress|blocked}"
    agent: "{responsible_agent}"

context:
  background: "{why this work is needed}"
  constraints: "{limitations or requirements}"
  risks: "{potential issues to watch for}"

validation_checklist:
  - [ ] All inputs present and validated
  - [ ] Contract version current
  - [ ] Dependencies satisfied
  - [ ] Tests defined
  - [ ] Acceptance criteria clear
```

### Handoff Lifecycle
1. **Preparation Phase**
   - Originating agent completes handoff template
   - Automated validation of handoff requirements
   - Impact analysis for receiving agent's workload

2. **Notification Phase**
   - Receiving agent notified via formal channel
   - SLA timer starts (1 business day acknowledgment)
   - Backup escalation scheduled if no response

3. **Acknowledgment Phase**
   - Receiving agent validates handoff completeness
   - Questions/clarifications handled via informal channel
   - Formal acceptance or rejection with reasons

4. **Execution Phase**
   - Receiving agent begins work
   - Progress updates via coordination channel
   - Informal consultation as needed

5. **Completion Phase**
   - Receiving agent marks work complete
   - Quality validation by Ops/QA Agent
   - Handoff closure and metrics recording

### Handoff Quality Metrics
- **Completeness Rate**: Percentage of handoffs with all required fields
- **Acknowledgment Time**: Average time to acknowledge handoffs
- **Rejection Rate**: Percentage of handoffs rejected for quality issues
- **Cycle Time**: Average time from handoff to completion
- **Rework Rate**: Percentage of handoffs requiring additional work

## Phase 2 – Coordination & Governance Implementation 

### System 2 (Coordination) Implementation
1. **Kanban Board Setup**
   - Contract-linked issue labels and workflows
   - Agent workload visualization and capacity planning
   - Automated task routing based on agent capabilities

2. **Notification System**
   - Contract change alerts with impact analysis
   - Handoff notifications with SLA tracking
   - Escalation alerts for missed deadlines

3. **Coordination Dashboard**
   - Real-time agent status and availability
   - Handoff queue and processing times
   - Contract compliance metrics

### System 3 (Control) Implementation
1. **Contract Governance**
   - Contract Maintainer rotation schedule
   - Merge gate enforcement with contract validation
   - Quarterly audit procedures and reporting

2. **Quality Control**
   - Automated quality gates for all handoffs
   - Contract compliance monitoring and alerts
   - Performance metrics tracking and reporting

3. **Risk Management**
   - Early warning systems for contract violations
   - Escalation procedures for system failures
   - Backup agent assignment for critical paths

### System 4 (Intelligence) Implementation
1. **Architecture Working Group**
   - Monthly roadmap reviews and interface planning
   - Trend analysis of contract violations and improvements
   - Future agent role and capability planning

2. **Continuous Improvement**
   - Retrospective analysis of handoff failures
   - Contract evolution recommendations
   - Process optimization suggestions

### System 5 (Policy) Implementation
1. **Charter Documentation**
   - "Proto-first, agent-safe, VSM-aligned" principles
   - Governance policies and decision-making authority
   - Cultural norms and collaboration expectations

2. **Policy Enforcement**
   - Automated policy compliance checking
   - Training and onboarding procedures
   - Policy violation handling and resolution

## Phase 3 – Execution Loop (Ongoing)
1. Agent picks task → references contract version.
2. Runs required tooling, updates artifacts, prepares handoff note.
3. Next agent confirms receipt; QA agent verifies pipeline.
4. Monthly VSM retrospective: ensure coordination/control layers remain viable.

## Enhanced Success Metrics

### Conway's Law Alignment Metrics
- **Boundary Violations**: < 5% of changes cross agent boundaries without proper handoff
- **Communication Efficiency**: Agent-to-agent communication follows defined protocols 95% of time
- **Interface Stability**: Contract violations detected before merge 100% of time

### VSM Viability Metrics
- **System 1 (Operations)**: 100% contract changes follow ICS checklist
- **System 2 (Coordination)**: Average handoff acknowledgment < 1 business day
- **System 3 (Control)**: CI success rate > 95% (failures only for real regressions)
- **System 4 (Intelligence)**: Quarterly audits show no drift between contracts and code
- **System 5 (Policy)**: Zero unresolved policy violations > 1 week old

### Agent Performance Metrics
- **Handoff Quality**: < 10% rejection rate, < 5% rework rate
- **Contract Compliance**: 100% adherence to interface contract requirements
- **Response Times**: Escalations resolved within defined SLA timeframes
- **Capability Utilization**: Agent workload balanced within 20% variance

### System Health Indicators
- **Coordination Effectiveness**: Bottlenecks resolved within 2 business days
- **Quality Consistency**: Test coverage > 80% across all interface contracts
- **Feedback Loop Integrity**: Monthly VSM retrospectives identify and resolve systemic issues
- **Adaptation Capability**: New requirements integrated without contract violations

## Implementation Risks & Mitigation

### High Risk: Agent Boundary Confusion
- **Risk**: Agents work outside their assigned interface boundaries
- **Mitigation**: Clear RACI matrix, automated boundary violation detection, regular training
- **Indicator**: Increase in cross-boundary changes without proper handoffs

### Medium Risk: Contract Evolution Complexity
- **Risk**: Contract changes become too complex to manage effectively
- **Mitigation**: Incremental change approach, impact analysis automation, rollback procedures
- **Indicator**: Increase in contract change rejection rate or time to implement

### Medium Risk: Handoff Bottlenecks
- **Risk**: Agent handoffs become a coordination bottleneck
- **Mitigation**: Automated handoff validation, SLA monitoring, backup agent assignment
- **Indicator**: Increase in handoff acknowledgment time or rejection rate

### Low Risk: VSM Layer Coordination
- **Risk**: Higher-level VSM systems (Intelligence, Policy) become disconnected from operations
- **Mitigation**: Regular retrospectives, clear escalation paths, feedback loop monitoring
- **Indicator**: Decrease in issue resolution effectiveness or policy adherence

## Resolved Questions & Decisions

### Agent Staffing Strategy
**Decision**: Hybrid approach with human oversight and LLM agent execution
- Critical contracts (ICS-001, ICS-002) require human validation
- Routine operations can be automated with LLM agents
- Human agents maintain oversight and exception handling

### External Integration Contracts
**Decision**: Defer additional contracts until Phase 3
- Current ICS-001 through ICS-007 cover internal coordination
- External integration contracts (REST/MCP) added when system stabilizes
- Monitor for need during Phase 2 implementation

### Handoff Record Storage
**Decision**: Git-based handoff records with external dashboard
- Handoff templates stored in `agent_workflow/handoffs/` directory
- Automated dashboard pulls from Git for visualization and metrics
- Maintains audit trail while providing operational visibility

## Next Steps for Implementation

1. **Phase 1**: Set up contracts directory structure and initial ICS documents
2. **Phase 2**: Implement handoff template and validation automation
3. **Phase 3**: Deploy agent capability assessment and onboarding procedures
4. **Phase 4**: Launch coordination dashboard and notification system
5. **Phase 5**: Begin monthly VSM retrospectives and continuous improvement cycle

