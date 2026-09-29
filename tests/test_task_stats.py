"""Тесты статистики задач."""

from src.stats import task_stats


def test_stats_mixed_tasks():
    tasks = [
        {"id": 1, "title": "Подготовить отчёт", "completed": False},
        {"id": 2, "title": "Прочитать лекцию", "completed": True},
        {"id": 3, "title": "Сдать практику", "completed": False},
    ]

    assert task_stats(tasks) == {
        "total": 3,
        "completed": 1,
        "pending": 2,
    }


def test_stats_empty_list():
    assert task_stats([]) == {
        "total": 0,
        "completed": 0,
        "pending": 0,
    }


def test_stats_all_completed():
    tasks = [
        {"id": 1, "title": "Прочитать лекцию", "completed": True},
        {"id": 2, "title": "Сдать практику", "completed": True},
    ]

    assert task_stats(tasks) == {
        "total": 2,
        "completed": 2,
        "pending": 0,
    }


def test_stats_all_pending():
    tasks = [
        {"id": 1, "title": "Подготовить отчёт", "completed": False},
        {"id": 2, "title": "Сдать практику", "completed": False},
    ]

    assert task_stats(tasks) == {
        "total": 2,
        "completed": 0,
        "pending": 2,
    }