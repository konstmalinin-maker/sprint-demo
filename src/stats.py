"""Модуль статистики задач."""


def task_stats(tasks: list[dict]) -> dict:
    """Возвращает количество всех, выполненных и невыполненных задач."""
    total = len(tasks)
    completed = sum(1 for task in tasks if task["completed"])

    return {
        "total": total,
        "completed": completed,
        "pending": total - completed,
    }