"""Интеграция с модулем, от которого зависела заблокированная задача."""

import pytest

from src.task_review import complete_and_summarize
from src.tasks import create_task


def test_completion_summary_uses_updated_status():
    tasks = []
    create_task(tasks, "First")
    create_task(tasks, "Second")
    summary = complete_and_summarize(tasks, 2)
    assert summary == {
        "task": {"id": 2, "title": "Second", "completed": True},
        "stats": {"total": 2, "completed": 1, "pending": 1},
    }
    assert tasks[0]["completed"] is False
    assert tasks[1]["completed"] is True


def test_summary_remains_a_snapshot():
    tasks = []
    create_task(tasks, "Original")
    summary = complete_and_summarize(tasks, 1)
    tasks[0]["title"] = "Renamed"
    create_task(tasks, "Another")
    assert summary["task"]["title"] == "Original"
    assert summary["stats"] == {"total": 1, "completed": 1, "pending": 0}


def test_summary_unknown_id_does_not_modify_tasks():
    tasks = [{"id": 1, "title": "Keep", "completed": False}]
    with pytest.raises(KeyError):
        complete_and_summarize(tasks, 2)
    assert tasks == [{"id": 1, "title": "Keep", "completed": False}]
