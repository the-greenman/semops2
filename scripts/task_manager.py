"""Agent task management CLI for SemOps2 MVP workflow.

This script implements the MVP GitHub Issues-based task management described in
`agent_workflow/task_management_plan.md`. It provides local task drafting and
templates that can be easily copied to GitHub Issues.

Usage examples:
    # Create a new task draft
    python scripts/task_manager.py create --contract ICS-001 --title "Add protovalidate annotations" \
        --receiving-agent service-agent --originating-agent schema-agent --priority high

    # Generate handoff comment for an issue
    python scripts/task_manager.py handoff --task-id "ICS-001-001" \
        --message "Schema validation rules implemented" \
        --next-steps "Implement service validation" "Update tests" \
        --tests "buf generate" "pytest tests/contracts"

    # Validate task format (future: validate against contracts)
    python scripts/task_manager.py validate --contract ICS-001
"""

from __future__ import annotations

import argparse
import enum
import json
import logging
import sys
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Optional


LOGGER = logging.getLogger(__name__)


class Priority(enum.Enum):
    """Canonical priority levels mirrored from GitHub labels."""

    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class Status(enum.Enum):
    """Task states aligned with `status:*` labels."""

    IDEA = "idea"
    READY = "ready"
    IN_PROGRESS = "in-progress"
    REVIEW = "review"
    HANDOFF = "handoff"
    DONE = "done"
    BLOCKED = "blocked"


@dataclass
class Task:
    """Lightweight representation of a task matching the MVP GitHub Issues format."""

    task_id: str
    title: str
    contract: str
    originating_agent: str
    receiving_agent: str
    priority: Priority
    status: Status = Status.IDEA
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    notes: Optional[str] = None
    expected_outputs: List[str] = field(default_factory=list)
    tests_required: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict:
        """Convert to dictionary with ISO datetime strings."""
        data = asdict(self)
        data['created_at'] = self.created_at.isoformat()
        data['updated_at'] = self.updated_at.isoformat()
        data['priority'] = self.priority.value
        data['status'] = self.status.value
        return data

    @classmethod
    def from_dict(cls, data: Dict) -> 'Task':
        """Create Task from dictionary."""
        data = data.copy()
        data['created_at'] = datetime.fromisoformat(data['created_at'])
        data['updated_at'] = datetime.fromisoformat(data['updated_at'])
        data['priority'] = Priority(data['priority'])
        data['status'] = Status(data['status'])
        return cls(**data)


def parse_args(argv: Optional[Iterable[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="SemOps agent task manager")
    parser.set_defaults(func=None)

    subparsers = parser.add_subparsers(dest="command", required=True)

    create_parser = subparsers.add_parser("create", help="Draft a new task")
    create_parser.add_argument("--contract", required=True, help="Interface contract ID (e.g. ICS-001)")
    create_parser.add_argument("--title", required=True, help="Short task title")
    create_parser.add_argument("--receiving-agent", required=True, help="GitHub handle or agent name")
    create_parser.add_argument("--originating-agent", required=True, help="Agent initiating the task")
    create_parser.add_argument("--priority", choices=[p.value for p in Priority], default=Priority.MEDIUM.value)
    create_parser.add_argument("--notes", help="Optional notes")
    create_parser.add_argument("--expected-outputs", nargs="*", default=[], help="Expected outputs/deliverables")
    create_parser.add_argument("--tests", nargs="*", default=[], help="Required tests to run")
    create_parser.add_argument("--dependencies", nargs="*", default=[], help="Task dependencies")
    create_parser.add_argument("--format", choices=["github", "json", "summary"], default="github",
                              help="Output format")
    create_parser.set_defaults(func=handle_create)

    list_parser = subparsers.add_parser("list", help="List tasks from local cache")
    list_parser.add_argument("--state", choices=[s.value for s in Status], help="Filter by status")
    list_parser.set_defaults(func=handle_list)

    handoff_parser = subparsers.add_parser("handoff", help="Record a handoff comment stub")
    handoff_parser.add_argument("--task-id", required=True)
    handoff_parser.add_argument("--message", required=True, help="Summary of handoff inputs")
    handoff_parser.add_argument("--next-steps", nargs="*", default=[], help="Checklist for receiving agent")
    handoff_parser.add_argument("--tests", nargs="*", default=[], help="Tests to run")
    handoff_parser.set_defaults(func=handle_handoff)

    update_parser = subparsers.add_parser("update", help="Update task status/priority")
    update_parser.add_argument("--task-id", required=True)
    update_parser.add_argument("--status", choices=[s.value for s in Status])
    update_parser.add_argument("--priority", choices=[p.value for p in Priority])
    update_parser.add_argument("--notes")
    update_parser.set_defaults(func=handle_update)

    # Add validate command for contract validation
    validate_parser = subparsers.add_parser("validate", help="Validate contract exists and is properly formatted")
    validate_parser.add_argument("--contract", required=True, help="Contract ID to validate (e.g. ICS-001)")
    validate_parser.set_defaults(func=handle_validate)

    return parser.parse_args(list(argv) if argv is not None else None)


def handle_create(args: argparse.Namespace) -> None:
    """Create a new task with specified format output."""

    task = Task(
        task_id=_generate_task_id(args.contract),
        title=args.title,
        contract=args.contract,
        originating_agent=args.originating_agent,
        receiving_agent=args.receiving_agent,
        priority=Priority(args.priority),
        notes=args.notes,
        expected_outputs=args.expected_outputs,
        tests_required=args.tests,
        dependencies=args.dependencies,
    )

    # Output in requested format
    if args.format == "github":
        _emit_issue_template(task)
    elif args.format == "json":
        print(json.dumps(task.to_dict(), indent=2))
    elif args.format == "summary":
        _emit_task_summary(task)

    LOGGER.info("Task draft created with ID: %s", task.task_id)


def handle_list(args: argparse.Namespace) -> None:
    """List tasks from local cache (not yet implemented)."""

    # TODO: pull tasks from GitHub or local `tasks/` cache.
    LOGGER.warning("Listing tasks is not implemented yet. Add GitHub integration or local cache parsing.")


def handle_handoff(args: argparse.Namespace) -> None:
    """Generate formatted handoff comment for GitHub Issues."""

    comment_lines = [f"**Handoff for {args.task_id}**"]
    comment_lines.append("")
    comment_lines.append("**Inputs Completed:**")
    comment_lines.append(f"- ✅ {args.message}")
    comment_lines.append("")

    if args.next_steps:
        comment_lines.append("**Your Next Steps:**")
        for step in args.next_steps:
            comment_lines.append(f"- [ ] {step}")
        comment_lines.append("")

    if args.tests:
        comment_lines.append("**Tests to Run:**")
        for test_cmd in args.tests:
            comment_lines.append(f"- `{test_cmd}`")
        comment_lines.append("")

    comment_lines.append("**Questions/Blockers:** None")
    comment_lines.append("")
    comment_lines.append("_Ready for handoff! Please update issue status when you begin._")

    # Output the comment template
    print("\n".join(comment_lines))

    LOGGER.info("Handoff comment generated for task: %s", args.task_id)


def handle_update(args: argparse.Namespace) -> None:
    """Generate commands to update GitHub Issue labels."""

    updates = []
    if args.status:
        updates.append(f"Remove existing status:* label and add status:{args.status}")
    if args.priority:
        updates.append(f"Remove existing priority:* label and add priority:{args.priority}")
    if args.notes:
        updates.append(f"Add comment: {args.notes}")

    if updates:
        print(f"Manual GitHub Issue updates for {args.task_id}:")
        for i, update in enumerate(updates, 1):
            print(f"{i}. {update}")
        print("\nNote: These updates must be made manually in GitHub Issues UI.")
    else:
        print("No updates specified.")

    LOGGER.info("Update instructions generated for task: %s", args.task_id)


def handle_validate(args: argparse.Namespace) -> None:
    """Validate that a contract exists and is properly formatted."""

    contract_path = Path("contracts") / f"{args.contract}.md"

    if not contract_path.exists():
        LOGGER.error("Contract file not found: %s", contract_path)
        print(f"❌ Contract {args.contract} not found at {contract_path}")
        print(f"💡 Create the contract file first or check the contract ID spelling.")
        sys.exit(1)

    # Basic validation - check if file has content
    try:
        content = contract_path.read_text(encoding="utf-8")
        if not content.strip():
            LOGGER.error("Contract file is empty: %s", contract_path)
            print(f"❌ Contract {args.contract} exists but is empty")
            sys.exit(1)

        # Check for basic contract structure
        required_sections = ["Purpose", "Owner", "Scope"]
        missing_sections = [section for section in required_sections
                          if section.lower() not in content.lower()]

        if missing_sections:
            LOGGER.warning("Contract may be incomplete, missing sections: %s", missing_sections)
            print(f"⚠️  Contract {args.contract} exists but may be missing: {', '.join(missing_sections)}")
        else:
            print(f"✅ Contract {args.contract} is valid and properly structured")

        LOGGER.info("Contract validation completed for: %s", args.contract)

    except Exception as e:
        LOGGER.error("Error reading contract file: %s", e)
        print(f"❌ Error reading contract {args.contract}: {e}")
        sys.exit(1)


def _generate_task_id(contract: str) -> str:
    """Generate a task identifier scoped to a contract.

    MVP approach: use timestamp for uniqueness. Replace with sequence
    counter when we add persistent storage.
    """

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    return f"{contract}-{timestamp}"


def _emit_issue_template(task: Task) -> None:
    """Generate GitHub Issue template in markdown format."""

    # Issue title
    print(f"**GitHub Issue Title:**")
    print(f"[{task.contract}] {task.title}")
    print()

    # Issue body
    print("**GitHub Issue Body:**")
    print("```markdown")
    print(f"**Receiving Agent:** @{task.receiving_agent}")
    print(f"**Contract:** {task.contract}")
    print()

    print("**Expected Outputs:**")
    if task.expected_outputs:
        for output in task.expected_outputs:
            print(f"- {output}")
    else:
        print("- <fill in required outputs>")
    print()

    print("**Tests Required:**")
    if task.tests_required:
        for test in task.tests_required:
            print(f"- `{test}`")
    else:
        print("- <fill in required tests>")
    print()

    print("**Dependencies:**")
    if task.dependencies:
        for dep in task.dependencies:
            print(f"- [ ] {dep}")
    else:
        print("- [ ] <fill in dependencies>")
    print()

    if task.notes:
        print("**Notes:**")
        print(task.notes)
        print()

    print(f"**Handoff From:** @{task.originating_agent}")
    print("```")
    print()

    # Labels
    print("**GitHub Labels to Apply:**")
    labels = [
        f"contract:{task.contract}",
        f"agent:{task.receiving_agent}",
        f"status:{task.status.value}",
        f"priority:{task.priority.value}"
    ]
    for label in labels:
        print(f"- {label}")


def _emit_task_summary(task: Task) -> None:
    """Print a concise task summary."""

    print(f"Task: {task.task_id}")
    print(f"Title: {task.title}")
    print(f"Contract: {task.contract}")
    print(f"From: {task.originating_agent} → To: {task.receiving_agent}")
    print(f"Priority: {task.priority.value}")
    print(f"Status: {task.status.value}")
    if task.notes:
        print(f"Notes: {task.notes}")
    print(f"Created: {task.created_at.strftime('%Y-%m-%d %H:%M')}")


def main(argv: Optional[Iterable[str]] = None) -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    args = parse_args(argv)
    if args.func is None:
        raise SystemExit("No command provided")
    args.func(args)


if __name__ == "__main__":
    main()
