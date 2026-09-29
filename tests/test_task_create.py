"""Тесты создания задач."""

import pytest

from src.tasks import create_task


def test_create_task():
    tasks = []

    task = create_task(tasks, "Подготовить отчёт")

    assert task == {
        "id": 1,
        "title": "Подготовить отчёт",
        "completed": False,
    }
    assert tasks == [task]


def test_create_task_unique_id():
    tasks = [
        {"id": 3, "title": "Первая задача", "completed": False},
        {"id": 1, "title": "Вторая задача", "completed": True},
    ]

    task = create_task(tasks, "Новая задача")

    assert task["id"] == 4
    assert len(tasks) == 3


def test_create_task_strips_spaces():
    tasks = []

    task = create_task(tasks, "  Прочитать лекцию  ")

    assert task["title"] == "Прочитать лекцию"


@pytest.mark.parametrize("title", ["", "   "])
def test_create_task_empty_title(title):
    tasks = []

    with pytest.raises(ValueError, match="не должно быть пустым"):
        create_task(tasks, title)

    assert tasks == []