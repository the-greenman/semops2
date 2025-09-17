# SemOps Workflow Example

This document demonstrates the complete workflow from task creation to completion.

## Complete Workflow Process

### 1. Task Creation
```bash
# Create a new task with GitHub integration
python scripts/task_manager.py create \
  --contract "ICS-001" \
  --title "Add protovalidate annotations" \
  --receiving-agent "service-agent" \
  --originating-agent "schema-agent" \
  --priority "high" \
  --expected-outputs "schema/semops/v1/core.proto" \
  --tests "buf lint schema" \
  --dependencies "ICS-005-setup-ci" \
  --create-issue
```

### 2. Start Work (Branch Creation)
```bash
# Create and checkout task branch
python scripts/task_manager.py branch --task-id 42 --checkout
```
This automatically:
- Creates branch `task/42-ics-001-add-protovalidate-annotations`
- Updates GitHub issue status to `in-progress`
- Checks out the new branch

### 3. Development Work
- Make code changes
- Run tests locally
- Commit changes with descriptive messages

### 4. Create Pull Request
```bash
# Create PR for review
python scripts/task_manager.py pr --task-id 42 --draft
```
This automatically:
- Creates PR with proper title and template
- Links to the GitHub issue
- Updates issue status to `review`
- Sets appropriate labels

### 5. Review Process
- Team reviews PR
- Make requested changes
- Get approval

### 6. Handoff Documentation
- Add handoff comment to GitHub issue
- Document outputs and next steps
- Tag receiving agent

### 7. Completion
- Merge PR
- Update issue status to `done`
- Close issue when fully complete

## Branch Naming Convention
`task/{issue_number}-{contract}-{title_slug}`

Example: `task/42-ics-001-add-protovalidate-annotations`