#!/bin/bash
# Script to create GitHub labels for SemOps agent workflow
# Uses GitHub CLI (gh) with API calls

set -e

echo "🏷️  SemOps GitHub Labels Setup"
echo "========================================"

# Check if gh is authenticated
if ! gh auth status >/dev/null 2>&1; then
    echo "❌ GitHub CLI not authenticated. Please run: gh auth login"
    exit 1
fi

echo "✅ GitHub CLI is authenticated"

# Function to create a label
create_label() {
    local name="$1"
    local description="$2"
    local color="$3"

    # Try to create the label
    if gh api repos/:owner/:repo/labels \
        --method POST \
        --field name="$name" \
        --field description="$description" \
        --field color="$color" \
        >/dev/null 2>&1; then
        echo "✅ Created label: $name"
        return 0
    else
        # Check if it already exists
        if gh api repos/:owner/:repo/labels/"$name" >/dev/null 2>&1; then
            echo "ℹ️  Label already exists: $name"
            return 0
        else
            echo "❌ Failed to create label: $name"
            return 1
        fi
    fi
}

echo ""
echo "🔨 Creating labels..."

# Status Labels
create_label "status:idea" "New concept, needs planning" "e1e8ed"
create_label "status:ready" "Ready to start work" "0052cc"
create_label "status:in-progress" "Currently being worked on" "fbca04"
create_label "status:review" "Completed, needs review" "d876e3"
create_label "status:handoff" "Ready to hand off to next agent" "f9d0c4"
create_label "status:done" "Completed and accepted" "0e8a16"
create_label "status:blocked" "Cannot proceed, needs help" "d93f0b"

# Priority Labels
create_label "priority:critical" "Critical priority - immediate attention" "b60205"
create_label "priority:high" "High priority" "d93f0b"
create_label "priority:medium" "Medium priority" "fbca04"
create_label "priority:low" "Low priority" "0e8a16"

# Agent Labels
create_label "agent:schema" "Schema Agent responsible" "006b75"
create_label "agent:service" "Service Agent responsible" "1d76db"
create_label "agent:cli" "CLI Agent responsible" "0052cc"
create_label "agent:knowledge" "Knowledge Agent responsible" "5319e7"
create_label "agent:ops" "Ops/QA Agent responsible" "d876e3"

# Contract Labels (ICS-001 through ICS-007)
create_label "contract:ICS-001" "Schema↔Service Contract" "c2e0c6"
create_label "contract:ICS-002" "Service↔CLI Contract" "c2e0c6"
create_label "contract:ICS-003" "Template Contract" "c2e0c6"
create_label "contract:ICS-004" "Knowledge Operations Contract" "c2e0c6"
create_label "contract:ICS-005" "Tooling Contract" "c2e0c6"
create_label "contract:ICS-006" "Documentation Contract" "c2e0c6"
create_label "contract:ICS-007" "Handoff Contract" "c2e0c6"

echo ""
echo "========================================"
echo "🎉 GitHub labels setup complete!"
echo ""
echo "Next steps:"
echo "1. Configure GitHub Project Board automation"
echo "2. Create issue templates"
echo "3. Start creating tasks with: python scripts/task_manager.py"