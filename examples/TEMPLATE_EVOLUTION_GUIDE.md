# Template Evolution Guide

## Why Template Evolution Matters

**The Reality**: In early adoption, templates WILL change rapidly as organizations learn what information they need to track.

**Without Template Evolution**:
- ❌ Entities become outdated and incompatible with new templates
- ❌ Validation fails, blocking creation of new entities
- ❌ Manual fixes are error-prone and time-consuming
- ❌ Fear of changing templates leads to suboptimal structures
- ❌ Chaos as templates and entities diverge

**With Template Evolution**:
- ✅ Controlled, tracked evolution with clear versioning
- ✅ LLM-assisted migration infers new field values from context
- ✅ Human review ensures accuracy
- ✅ No data loss - everything backed up with rollback capability
- ✅ Audit trail of all changes
- ✅ Confidence to improve templates as understanding grows

## Template Versioning

### Workspace-Wide Versioning

All entity types use the same template version:

```yaml
# workspace_config.yaml
workspace:
  template_version: "1.0.0"

# When you bump to 1.1.0, ALL entity packages migrate together
workspace:
  template_version: "1.1.0"
```

**Why workspace-wide?** Ensures consistency and prevents version fragmentation.

### Semantic Versioning

Follow semantic versioning (MAJOR.MINOR.PATCH):

- **MAJOR** (1.0.0 → 2.0.0): Breaking changes, significant restructuring
- **MINOR** (1.0.0 → 1.1.0): Adding fields, non-breaking enhancements
- **PATCH** (1.0.0 → 1.0.1): Bug fixes, template typos, minor tweaks

## Migration Strategies

### 1. Automated Migration

**When to use**: Simple field mappings with no inference needed

```yaml
migrations:
  "1.0.0 → 1.0.1":
    strategy: "automated"
    breaking: false

    changes:
      renamed_fields:
        - old: "decision_maker"
          new: "primary_decision_maker"

      added_fields:
        - field: "created_by"
          default: "system"
```

**Process**:
1. Backup entity
2. Apply field mappings
3. Validate
4. Commit

**No human review required.**

### 2. LLM-Assisted Migration

**When to use**: New fields that can be inferred from existing content

```yaml
migrations:
  "1.0.0 → 1.1.0":
    strategy: "llm_assisted"
    breaking: false

    changes:
      added_fields:
        - field: "authority_level"
          type: "string"
          required: true
          infer_from: ["domain_name", "purpose", "scope_included"]
          prompt: |
            Based on the domain name, purpose, and scope, determine the
            authority level for this domain. Options: HIGH, MEDIUM, LOW.

            HIGH: Involves governance, security, compliance, constitutional
            MEDIUM: Core operational domains with significant impact
            LOW: Supporting or exploratory domains

            Provide only the authority level (HIGH, MEDIUM, or LOW).
```

**Process**:
1. Backup entity
2. Load entity + relationships + knowledge sources (full context)
3. LLM analyzes context and infers field value
4. Apply new template
5. Validate
6. Commit

**No human review, but LLM logs reasoning for audit.**

### 3. LLM-Assisted with Review

**When to use**: Same as LLM-assisted, but you want human oversight

```yaml
migrations:
  "1.0.0 → 1.1.0":
    strategy: "llm_assisted_with_review"
    breaking: false
    # ... same changes as above
```

**Process**:
1. Backup entity
2. Load full context
3. LLM infers field value
4. **Generate preview** (before/after)
5. **Human reviews and approves/rejects/edits**
6. Apply new template
7. Commit

**Human approval required before committing.**

### 4. Manual Migration

**When to use**: Complex changes that require human judgment

```yaml
migrations:
  "1.0.0 → 2.0.0":
    strategy: "manual"
    breaking: true

    changes:
      restructured:
        description: "Split stakeholders into separate accountable/consulted/informed sections"
        guide: |
          1. Review current "stakeholders" field
          2. Categorize each stakeholder:
             - Accountable: Has ultimate responsibility
             - Consulted: Must be consulted for decisions
             - Informed: Should be aware of changes
          3. Move into new structure
```

**Process**:
1. Backup entity
2. Generate migration guide
3. **Human manually edits entity**
4. Validate new format
5. Commit

**Fully manual process with guidance.**

## Migration Workflow

### Step 1: Check for Outdated Entities

```bash
$ semops migrate check

Checking template versions across workspace...

Current workspace version: 1.1.0

Found entities using older templates:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Entity Type: domain
  v1.0.0: 5 entities
    • DOM-governance (created 3 months ago)
    • DOM-operations (created 3 months ago)
    • DOM-engineering (created 2 months ago)
    • DOM-marketing (created 1 month ago)
    • DOM-exploration (created 1 week ago)

Entity Type: decision
  v1.0.0: 12 entities
  (use --verbose to list all)

Entity Type: policy
  v1.0.0: 3 entities
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Total entities needing migration: 20

Next step:
  semops migrate preview  # Preview changes before migrating
```

### Step 2: Preview Migration

```bash
$ semops migrate preview --entity-type domain

Previewing migration: domain v1.0.0 → v1.1.0
Strategy: llm_assisted_with_review

[1/5] DOM-governance
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Current (v1.0.0):
  domain_name: "Governance"
  purpose: "Organizational governance and decision-making"
  scope_included:
    - "Constitutional matters"
    - "Policy development"
    - "Decision-making processes"
  scope_excluded:
    - "Day-to-day operations"

Proposed (v1.1.0):
  domain_name: "Governance"
  purpose: "Organizational governance and decision-making"
  scope_included:
    - "Constitutional matters"
    - "Policy development"
    - "Decision-making processes"
  scope_excluded:
    - "Day-to-day operations"
  authority_level: "HIGH"  ← ADDED (inferred by LLM)

LLM Reasoning:
  "Domain handles constitutional matters and policy development,
   which are foundational governance activities requiring high
   authority. Decisions in this domain affect the entire organization."

Confidence: 95%
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[2/5] DOM-operations
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Current (v1.0.0):
  domain_name: "Operations"
  purpose: "Day-to-day operational activities"
  ...

Proposed (v1.1.0):
  ...
  authority_level: "MEDIUM"  ← ADDED (inferred by LLM)

LLM Reasoning:
  "Operational domain with significant impact on daily activities
   but not foundational governance. Medium authority appropriate."

Confidence: 90%
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[... previews for remaining 3 domains ...]

Summary:
  • Entities to migrate: 5
  • Strategy: llm_assisted_with_review
  • New fields: authority_level
  • Estimated time: 5-10 minutes (with human review)

Proceed with migration?
  semops migrate run --entity-type domain
```

### Step 3: Run Migration

```bash
$ semops migrate run --entity-type domain --strategy llm_assisted_with_review

Migrating 5 domain entities from v1.0.0 → v1.1.0...

[1/5] DOM-governance
  ✓ Backed up to .semops/backups/migrations/20260226-143022/DOM-governance
  ✓ Loaded context (entity + 8 relationships + 3 knowledge sources)
  ✓ LLM inferred authority_level: "HIGH" (confidence: 95%)

  Preview:
  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  domain_name: "Governance"
  purpose: "Organizational governance and decision-making"
  scope_included: [...]
  authority_level: "HIGH"  ← NEW FIELD
  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Actions:
    [1] Approve
    [2] Edit value
    [3] Skip this entity
    [4] Abort migration

  Your choice: 1

  ✓ Applied template v1.1.0
  ✓ Validated migration (all required fields present)
  ✓ Committed changes
  ✓ Restored 8 relationships

[2/5] DOM-operations
  ✓ Backed up
  ✓ Loaded context (entity + 5 relationships + 1 knowledge source)
  ✓ LLM inferred authority_level: "MEDIUM" (confidence: 90%)

  Preview:
  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  domain_name: "Operations"
  purpose: "Day-to-day operational activities"
  scope_included: [...]
  authority_level: "MEDIUM"  ← NEW FIELD
  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Actions: ...
  Your choice: 1

  ✓ Migration completed

[3/5] DOM-engineering
  ✓ Backed up
  ✓ Loaded context
  ✓ LLM inferred authority_level: "MEDIUM" (confidence: 85%)

  Preview:
  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  domain_name: "Engineering"
  purpose: "Software development and technical infrastructure"
  scope_included: [...]
  authority_level: "MEDIUM"  ← NEW FIELD
  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Actions: ...
  Your choice: 2  # Edit value

  Current value: "MEDIUM"
  Enter new value: LOW

  ✓ Value updated to "LOW"
  ✓ Migration completed

[4/5] DOM-marketing
  ✓ Backed up
  ✓ LLM inferred authority_level: "LOW" (confidence: 92%)
  Your choice: 1
  ✓ Migration completed

[5/5] DOM-exploration
  ✓ Backed up
  ✓ LLM inferred authority_level: "LOW" (confidence: 98%)
  Your choice: 1
  ✓ Migration completed

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Migration Summary
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Entity Type: domain
Template Version: 1.0.0 → 1.1.0
Strategy: llm_assisted_with_review

Results:
  • Migrated: 5/5 entities (100%)
  • Approved as-is: 4
  • Edited: 1 (DOM-engineering: MEDIUM → LOW)
  • Skipped: 0
  • Failed: 0

Backup:
  Location: .semops/backups/migrations/20260226-143022/
  Retention: 90 days
  Rollback: Available

Total time: 3m 42s
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

All domain entities now use template v1.1.0.

Next: Migrate other entity types or update workspace version.
```

### Step 4: Rollback (If Needed)

```bash
$ semops migrate rollback --migration-id 20260226-143022

Rolling back migration 20260226-143022...

Found backup for 5 entities:
  • DOM-governance
  • DOM-operations
  • DOM-engineering
  • DOM-marketing
  • DOM-exploration

Restoring entities to template v1.0.0...

[1/5] DOM-governance
  ✓ Restored entity from backup
  ✓ Restored 8 relationships
  ✓ Restored 3 knowledge sources
  ✓ Validated entity

[... restores remaining 4 entities ...]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Rollback Summary
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  • Restored: 5/5 entities
  • Template version: 1.1.0 → 1.0.0
  • Relationships restored: 22 total
  • Knowledge sources restored: 5 total
  • Failed: 0

All entities rolled back successfully.
Backup retained at: .semops/backups/migrations/20260226-143022/
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Migration Rules Configuration

### Example: Adding a Required Field

```yaml
# entity_packages/domain/migration_rules.yaml

current_version: "1.1.0"

migrations:

  "1.0.0 → 1.1.0":
    breaking: false
    strategy: "llm_assisted_with_review"

    changes:
      added_fields:
        - field: "authority_level"
          type: "string"
          required: true
          enum: ["HIGH", "MEDIUM", "LOW"]
          infer_from: ["domain_name", "purpose", "scope_included", "primary_stakeholders"]

          prompt: |
            Analyze this domain and determine its authority level.

            Context:
            - Domain Name: {domain_name}
            - Purpose: {purpose}
            - Scope: {scope_included}
            - Stakeholders: {primary_stakeholders}

            Authority Levels:
            - HIGH: Constitutional, governance, security, compliance domains
            - MEDIUM: Core operational domains with significant impact
            - LOW: Supporting, exploratory, or narrow-scope domains

            Based on the context, what authority level should this domain have?
            Provide ONLY the level (HIGH, MEDIUM, or LOW) and a brief one-sentence justification.

    validation:
      - check: "authority_level in ['HIGH', 'MEDIUM', 'LOW']"
        error_message: "authority_level must be HIGH, MEDIUM, or LOW"

      - check: "len(authority_level) > 0"
        error_message: "authority_level cannot be empty"

    rollback_supported: true
    backup_retention_days: 90
```

### Example: Restructuring Fields

```yaml
"1.1.0 → 2.0.0":
  breaking: true
  strategy: "manual"

  changes:
    restructured:
      - description: "Split stakeholders into accountable/consulted/informed"
        old_structure:
          field: "primary_stakeholders"
          type: "array[object]"

        new_structure:
          fields:
            - "accountable_roles"
            - "consulted_roles"
            - "informed_roles"
          type: "array[object]" # for each

        migration_guide: |
          1. Review current "primary_stakeholders" list
          2. For each stakeholder, determine their involvement:
             - Accountable: Has ultimate responsibility and decision authority
             - Consulted: Must be consulted before decisions
             - Informed: Should be kept aware of changes
          3. Move each stakeholder into appropriate new field
          4. Ensure at least one accountable role exists

    validation:
      - check: "len(accountable_roles) > 0"
        error_message: "Domain must have at least one accountable role"

  rollback_supported: true
  backup_retention_days: 365  # Longer retention for breaking changes
```

## Best Practices

### 1. Start Small, Iterate Quickly
**Early adoption**: Make small, frequent template changes as you learn
**Don't fear changes**: Migration system is designed for this

### 2. Use LLM-Assisted with Review Initially
Start with human review until confident in LLM inference quality, then switch to llm_assisted for routine changes.

### 3. Test Migrations on Subset
```bash
# Migrate just one entity first to test
semops migrate run --entity-id DOM-test --strategy llm_assisted_with_review

# If successful, migrate all
semops migrate run --entity-type domain --strategy llm_assisted_with_review
```

### 4. Keep Backup Retention Generous
90 days is reasonable for minor changes, 365 days for breaking changes.

### 5. Document Migration Reasoning
Add comments in migration_rules.yaml explaining WHY you're adding/changing fields.

### 6. Validate After Migration
```bash
# Check all entities validate correctly
semops validate --entity-type domain

# Check relationships still intact
semops relationships validate
```

## Common Scenarios

### Scenario 1: Adding Optional Metadata

```yaml
"1.0.0 → 1.0.1":
  strategy: "automated"  # No inference needed
  breaking: false

  changes:
    added_fields:
      - field: "last_reviewed_date"
        type: "date"
        required: false
        default: null  # Will be filled in later
```

### Scenario 2: Renaming for Clarity

```yaml
"1.0.0 → 1.0.1":
  strategy: "automated"
  breaking: false

  changes:
    renamed_fields:
      - old: "decision_maker"
        new: "primary_decision_maker"

      - old: "stakeholders"
        new: "affected_stakeholders"
```

### Scenario 3: Adding Calculated Field

```yaml
"1.0.0 → 1.1.0":
  strategy: "llm_assisted"
  breaking: false

  changes:
    added_fields:
      - field: "complexity_level"
        type: "string"
        enum: ["SIMPLE", "MODERATE", "COMPLEX"]
        infer_from: ["scope_included", "stakeholders", "dependencies"]

        prompt: |
          Rate this domain's complexity based on:
          - Scope breadth (how many responsibilities)
          - Number of stakeholders involved
          - Number of dependencies on other domains

          SIMPLE: Narrow scope, few stakeholders, minimal dependencies
          MODERATE: Moderate scope, several stakeholders, some dependencies
          COMPLEX: Broad scope, many stakeholders, extensive dependencies

          Provide only: SIMPLE, MODERATE, or COMPLEX
```

## Troubleshooting

### Migration Fails Validation

```bash
Error: Migration failed validation for DOM-governance
  - Missing required field: authority_level
  - authority_level must be one of: HIGH, MEDIUM, LOW

Solution:
1. Check LLM response in logs: .semops/logs/migrations/20260226-143022.log
2. If LLM didn't provide valid value, use manual override:
   semops migrate edit DOM-governance --field authority_level --value HIGH
3. Re-run validation:
   semops migrate validate DOM-governance
```

### LLM Inference Low Confidence

```bash
Warning: Low confidence (62%) for DOM-exploration.authority_level

Recommended action:
  Review and edit this entity manually during migration
```

### Relationship Restoration Fails

```bash
Error: Could not restore relationship "part_of" for DOM-governance → DOM-root

Cause: Target entity DOM-root no longer exists

Solution:
1. Identify new target: semops domain list
2. Update relationship: semops relationship add part_of DOM-governance DOM-new-root
```

## Summary

Template evolution is **critical** for early adoption success:
- ✅ Enables rapid learning and iteration
- ✅ Prevents template-entity fragmentation
- ✅ LLM assistance reduces manual work
- ✅ Human review ensures accuracy
- ✅ Rollback provides safety net
- ✅ Audit trail for all changes

Don't fear changing templates. The migration system is designed to support your organization's evolution.
