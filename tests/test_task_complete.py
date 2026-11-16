"""Проверки функции-предшественника для задания F."""

import pytest

from src.tasks import complete_task, create_task


def test_complete_only_requested_task():
    tasks = []
    first = create_task(tasks, "First")
    second = create_task(tasks, "Second")
    assert complete_task(tasks, second["id"]) is second
    assert second["completed"] is True
    assert first["completed"] is False


def test_complete_task_is_idempotent():
    tasks = []
    task = create_task(tasks, "Finish report")
    complete_task(tasks, task["id"])
    assert complete_task(tasks, task["id"]) == task
    assert len(tasks) == 1


def test_unknown_id_leaves_tasks_unchanged():
    tasks = [{"id": 1, "title": "Keep", "completed": False}]
    with pytest.raises(KeyError) as exc:
        complete_task(tasks, 999)
    assert exc.value.args == (999,)
    assert tasks == [{"id": 1, "title": "Keep", "completed": False}]


def test_complete_empty_list():
    with pytest.raises(KeyError):
        complete_task([], 1)
