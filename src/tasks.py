"""Модуль создания и просмотра задач."""


def list_tasks(tasks: list[dict]) -> list[dict]:
    """Возвращает копию списка задач."""
    return list(tasks)


def create_task(tasks: list[dict], title: str) -> dict:
    """Создаёт задачу и добавляет её в список.

    Raises:
        ValueError: если название задачи пустое.
    """
    title = title.strip()
    if not title:
        raise ValueError("Название задачи не должно быть пустым")

    task_id = max((task["id"] for task in tasks), default=0) + 1
    task = {
        "id": task_id,
        "title": title,
        "completed": False,
    }
    tasks.append(task)
    return task

def complete_task(tasks: list[dict], task_id: int) -> dict:
    """Отмечает задачу выполненной; неизвестный ID вызывает KeyError."""
    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = True
            return task
    raise KeyError(task_id)
