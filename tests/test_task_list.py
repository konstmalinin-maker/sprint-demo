"""Тесты просмотра списка задач."""

from src.tasks import list_tasks


def test_list_tasks():
    tasks = [
        {"id": 1, "title": "Подготовить отчёт", "completed": False},
        {"id": 2, "title": "Прочитать лекцию", "completed": True},
    ]

    result = list_tasks(tasks)

    assert result == tasks
    assert result is not tasks


def test_list_tasks_empty():
    assert list_tasks([]) == []

def test_list_tasks_result_does_not_change_source():
    tasks = [
        {"id": 1, "title": "Подготовить отчёт", "completed": False},
        {"id": 2, "title": "Прочитать лекцию", "completed": True},
    ]

    result = list_tasks(tasks)
    result.pop()

    assert len(result) == 1
    assert len(tasks) == 2
    assert tasks[1]["id"] == 2