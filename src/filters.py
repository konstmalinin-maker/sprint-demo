"""Модуль фильтрации задач."""


def filter_tasks(tasks: list[dict], completed: bool) -> list[dict]:
    """Возвращает задачи с указанным статусом выполнения."""
    return [task for task in tasks if task["completed"] == completed]