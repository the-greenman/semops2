"""Agent task management CLI skeleton.

This script mirrors the workflow described in
`agent_workflow/task_management_plan.md`.  It does not implement
GitHub integration yet; instead, it provides the structure for future
automation (API calls, validation, etc.).

Usage examples:
    python scripts/task_manager.py create --contract ICS-001 --title "Add protovalidate annotations" \
        --receiving-agent service --priority high

    python scripts/task_manager.py list --state ready

    python scripts/task_manager.py handoff --task-id ICS-001-001 --message "Inputs complete" \
        --next-steps "Run buf generate"
"""

from __future__ import annotations

import argparse
import enum
import logging
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Iterable, List, Optional


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
    """Lightweight representation of a task.

    This mirrors the metadata we capture via GitHub Issues.  In the
    MVP the script can emit this structure to stdout, or serialize it
    to JSON/YAML for future automation.
    """

    task_id: str
    title: str
    contract: str
    originating_agent: str
    receiving_agent: str
    priority: Priority
    status: Status = Status.IDEA
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    notes: Optional[str] = None


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
    create_parser.add_argument("--notes", help="Optional notes" )
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

    return parser.parse_args(list(argv) if argv is not None else None)


def handle_create(args: argparse.Namespace) -> None:
    """Placeholder for task creation logic."""

    task = Task(
        task_id=_generate_task_id(args.contract),
        title=args.title,
        contract=args.contract,
        originating_agent=args.originating_agent,
        receiving_agent=args.receiving_agent,
        priority=Priority(args.priority),
        notes=args.notes,
    )

    # TODO: integrate with GitHub Issues API (create issue, apply labels)
    # For now, just log the task to stdout so the agent can copy into GitHub.
    LOGGER.info("Draft task created: %s", task)
    _emit_issue_template(task)


def handle_list(args: argparse.Namespace) -> None:
    """List tasks from local cache (not yet implemented)."""

    # TODO: pull tasks from GitHub or local `tasks/` cache.
    LOGGER.warning("Listing tasks is not implemented yet. Add GitHub integration or local cache parsing.")


def handle_handoff(args: argparse.Namespace) -> None:
    """Emit a handoff comment template for the given task."""

    # TODO: fetch task metadata if available to include in comment.
    comment_lines = [f"@{args.task_id} handoff summary:"]
    comment_lines.append("")
    comment_lines.append("**Inputs Completed:**")
    comment_lines.append(args.message)
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

    LOGGER.info("\n".join(comment_lines))


def handle_update(args: argparse.Namespace) -> None:
    """Update an existing task (placeholder)."""

    # TODO: implement GitHub issue update logic or local cache edits.
    LOGGER.warning(
        "Update requested for %s (status=%s priority=%s notes=%s) – not implemented",
        args.task_id,
        args.status,
        args.priority,
        args.notes,
    )


def _generate_task_id(contract: str) -> str:
    """Generate a task identifier scoped to a contract.

    MVP approach: use timestamp for uniqueness. Replace with sequence
    counter when we add persistent storage.
    """

    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    return f"{contract}-{timestamp}"


def _emit_issue_template(task: Task) -> None:
    """Print the GitHub Issue body template for the new task."""

    template_lines: List[str] = ["---", f"title: [{task.contract}] {task.title}"]
    template_lines.append("body: |-")
    template_lines.append(f"  **Receiving Agent:** @{task.receiving_agent}")
    template_lines.append(f"  **Contract:** {task.contract}")
    template_lines.append("")
    template_lines.append("  **Expected Outputs:**")
    template_lines.append("  - <fill in>")
    template_lines.append("")
    template_lines.append("  **Tests Required:**")
    template_lines.append("  - <fill in>")
    template_lines.append("")
    template_lines.append("  **Dependencies:**")
    template_lines.append("  - [ ] <fill in>")
    template_lines.append("")
    template_lines.append("  **Handoff From:** @" + task.originating_agent)
    template_lines.append("labels:")
    template_lines.append(f"  - contract:{task.contract}")
    template_lines.append(f"  - agent:{task.originating_agent}")
    template_lines.append(f"  - agent:{task.receiving_agent}")
    template_lines.append(f"  - status:{task.status.value}")
    template_lines.append(f"  - priority:{task.priority.value}")

    output_path = Path("agent_workflow") / "draft_issue.yaml"
    output_path.write_text("\n".join(template_lines), encoding="utf-8")
    LOGGER.info("Draft issue template written to %s", output_path)


def main(argv: Optional[Iterable[str]] = None) -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    args = parse_args(argv)
    if args.func is None:
        raise SystemExit("No command provided")
    args.func(args)


if __name__ == "__main__":
    main()
