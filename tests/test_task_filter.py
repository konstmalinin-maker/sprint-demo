"""Тесты фильтрации задач."""

from src.filters import filter_tasks


def test_filter_completed_tasks():
    tasks = [
        {"id": 1, "title": "Подготовить отчёт", "completed": False},
        {"id": 2, "title": "Прочитать лекцию", "completed": True},
    ]

    assert filter_tasks(tasks, completed=True) == [tasks[1]]


def test_filter_pending_tasks():
    tasks = [
        {"id": 1, "title": "Подготовить отчёт", "completed": False},
        {"id": 2, "title": "Прочитать лекцию", "completed": True},
    ]

    assert filter_tasks(tasks, completed=False) == [tasks[0]]


def test_filter_empty_list():
    assert filter_tasks([], completed=True) == []


def test_filter_no_matches():
    tasks = [
        {"id": 1, "title": "Подготовить отчёт", "completed": False},
    ]

    assert filter_tasks(tasks, completed=True) == []