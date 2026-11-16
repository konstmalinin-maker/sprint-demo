"""Зависимая функция: выполнение задачи и сводка текущего состояния."""

from src.stats import task_stats
from src.tasks import complete_task


def complete_and_summarize(tasks: list[dict], task_id: int) -> dict:
    """Выполняет задачу и возвращает снимок задачи и статистики.

    Неизвестный ID вызывает KeyError без изменения списка задач.
    """
    task = complete_task(tasks, task_id)
    return {"task": dict(task), "stats": task_stats(tasks)}
