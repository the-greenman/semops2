"""Unit tests for scripts.task_manager."""

from __future__ import annotations

import json
from types import SimpleNamespace

import pytest

from scripts import task_manager


def _ns(**kwargs):
    """Helper to build argparse-like namespaces."""

    return SimpleNamespace(**kwargs)


def test_task_serialization_round_trip():
    task = task_manager.Task(
        task_id="ICS-001-20240218120000",
        title="Add protovalidate annotations",
        contract="ICS-001",
        originating_agent="schema-agent",
        receiving_agent="service-agent",
        priority=task_manager.Priority.HIGH,
        status=task_manager.Status.READY,
        notes="Ensure backward compatibility",
        expected_outputs=["schema/semops/v1/core.proto"],
        tests_required=["buf lint schema"],
        dependencies=["ICS-005-setup-ci"],
    )

    payload = task.to_dict()
    restored = task_manager.Task.from_dict(payload)

    assert restored == task


def test_handle_create_json_format(capsys):
    args = _ns(
        contract="ICS-001",
        title="Add protovalidate annotations",
        receiving_agent="service-agent",
        originating_agent="schema-agent",
        priority="high",
        notes=None,
        expected_outputs=["schema/semops/v1/core.proto"],
        tests=["buf lint schema"],
        dependencies=["ICS-005"],
        format="json",
    )

    task_manager.handle_create(args)

    captured = capsys.readouterr()
    data = json.loads(captured.out)

    assert data["contract"] == "ICS-001"
    assert data["expected_outputs"] == ["schema/semops/v1/core.proto"]
    assert data["tests_required"] == ["buf lint schema"]
    assert data["priority"] == "high"


def test_handle_create_issue_template(capsys):
    args = _ns(
        contract="ICS-002",
        title="Wire CLI command",
        receiving_agent="cli-agent",
        originating_agent="service-agent",
        priority="medium",
        notes="",
        expected_outputs=[],
        tests=[],
        dependencies=[],
        format="github",
    )

    task_manager.handle_create(args)

    out = capsys.readouterr().out
    assert "GitHub Issue Title" in out
    assert "[ICS-002] Wire CLI command" in out
    assert "contract:ICS-002" in out
    assert "agent:cli-agent" in out


def test_handle_create_summary_format(capsys):
    args = _ns(
        contract="ICS-003",
        title="Test summary format",
        receiving_agent="test-agent",
        originating_agent="dev-agent",
        priority="low",
        notes="Test notes",
        expected_outputs=["output.txt"],
        tests=["test command"],
        dependencies=["dep1"],
        format="summary",
    )

    task_manager.handle_create(args)

    out = capsys.readouterr().out
    assert "Task: ICS-003-" in out  # Task ID starts with contract
    assert "Title: Test summary format" in out
    assert "Contract: ICS-003" in out
    assert "From: dev-agent → To: test-agent" in out
    assert "Priority: low" in out
    assert "Notes: Test notes" in out


def test_handle_handoff_generates_comment(capsys):
    args = _ns(
        task_id="ICS-001-001",
        message="Schema validation rules implemented",
        next_steps=["Implement service validation", "Update tests"],
        tests=["buf generate", "pytest tests/contracts"],
    )

    task_manager.handle_handoff(args)

    output = capsys.readouterr().out
    assert "Handoff for ICS-001-001" in output
    assert "Implement service validation" in output
    assert "`buf generate`" in output


def test_handle_validate_success(tmp_path, capsys, monkeypatch):
    contracts_dir = tmp_path / "contracts"
    contracts_dir.mkdir()
    contract_file = contracts_dir / "ICS-001.md"
    contract_file.write_text(
        """# ICS-001 Contract\n\n## Purpose\nEnsure service consumes schema.\n\n## Owner\nSchema Agent\n\n## Scope\nSchema and service boundary.\n""",
        encoding="utf-8",
    )

    monkeypatch.chdir(tmp_path)

    args = _ns(contract="ICS-001")
    task_manager.handle_validate(args)

    output = capsys.readouterr().out
    assert "Contract ICS-001 is valid" in output


def test_handle_validate_missing_contract(tmp_path, monkeypatch):
    (tmp_path / "contracts").mkdir()
    monkeypatch.chdir(tmp_path)
    args = _ns(contract="ICS-999")

    with pytest.raises(SystemExit):
        task_manager.handle_validate(args)


def test_handle_validate_incomplete_contract(tmp_path, capsys, monkeypatch):
    contracts_dir = tmp_path / "contracts"
    contracts_dir.mkdir()
    contract_file = contracts_dir / "ICS-002.md"
    contract_file.write_text(
        """# ICS-002 Contract\n\nIncomplete contract missing required sections.\n""",
        encoding="utf-8",
    )

    monkeypatch.chdir(tmp_path)

    args = _ns(contract="ICS-002")
    task_manager.handle_validate(args)

    output = capsys.readouterr().out
    assert "may be missing:" in output
    assert "Purpose" in output or "Owner" in output or "Scope" in output


def test_handle_update_generates_instructions(capsys):
    args = _ns(
        task_id="ICS-001-001",
        status="in-progress",
        priority="high",
        notes="Updated priority due to urgency",
    )

    task_manager.handle_update(args)

    output = capsys.readouterr().out
    assert "Manual GitHub Issue updates for ICS-001-001" in output
    assert "status:in-progress" in output
    assert "priority:high" in output
    assert "Updated priority due to urgency" in output


def test_generate_task_id_format():
    task_id = task_manager._generate_task_id("ICS-001")
    assert task_id.startswith("ICS-001-")
    assert len(task_id) == len("ICS-001-") + 14  # timestamp is 14 digits


def test_priority_enum_values():
    assert task_manager.Priority.CRITICAL.value == "critical"
    assert task_manager.Priority.HIGH.value == "high"
    assert task_manager.Priority.MEDIUM.value == "medium"
    assert task_manager.Priority.LOW.value == "low"


def test_status_enum_values():
    assert task_manager.Status.IDEA.value == "idea"
    assert task_manager.Status.READY.value == "ready"
    assert task_manager.Status.IN_PROGRESS.value == "in-progress"
    assert task_manager.Status.REVIEW.value == "review"
    assert task_manager.Status.HANDOFF.value == "handoff"
    assert task_manager.Status.DONE.value == "done"
    assert task_manager.Status.BLOCKED.value == "blocked"
