# sprint-demo

[![PR checks](https://github.com/konstmalinin-maker/sprint-demo/actions/workflows/pr-check.yml/badge.svg?branch=main)](https://github.com/konstmalinin-maker/sprint-demo/actions/workflows/pr-check.yml)

Учебный проект для имитации Scrum-спринта. Реализованы регистрация и вход, создание и просмотр задач, фильтрация по статусу и статистика. Все данные хранятся в памяти. Требуется Python 3.12.

## Запуск проверок

```sh
python -m venv .venv
# Linux/macOS:
source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m ruff check src tests
python -m pytest -v --cov=src --cov-report=term-missing
```

Результат проверки 16.11.2026: 28 тестов проходят, покрытие строк — 100% (36 из 36), Ruff без замечаний. Покрытие строк не гарантирует отсутствие всех ошибок. Пустые модули goals, reminders и workouts — заготовки.

## Пример использования

```python
from src.auth import register, login
from src.tasks import create_task, list_tasks
from src.filters import filter_tasks
from src.stats import task_stats

register("user@example.com", "securepass123")
assert login("user@example.com", "securepass123")
tasks = []
create_task(tasks, "Подготовить отчёт")
create_task(tasks, "Прочитать лекцию")
tasks[1]["completed"] = True
print(list_tasks(tasks))
print(filter_tasks(tasks, False))
print(task_stats(tasks))  # {'total': 2, 'completed': 1, 'pending': 1}
```

## Материалы практики №4

- [Полный отчёт со скриншотами и ответами на вопросы](PR4_Отчёт_Малинин.md).
- [Sprint Goal и Definition of Done](docs/sprint-1-goal.md).
- [Sprint Review](docs/review-sprint-1.md).
- [Retrospective](docs/retro-sprint-1.md).
- [Релиз v0.1.0](https://github.com/konstmalinin-maker/sprint-demo/releases/tag/v0.1.0).
- [Задание A: интерактивный rebase, PR #14](https://github.com/konstmalinin-maker/sprint-demo/pull/14).
- [Задание B: CI, PR #15](https://github.com/konstmalinin-maker/sprint-demo/pull/15).
- [CODEOWNERS, PR #16](https://github.com/konstmalinin-maker/sprint-demo/pull/16).

Работа выполнена индивидуально Малининым Константином Николаевичем. Самопроверка не заменяет независимое ревью. Файл CODEOWNERS добавлен; обязательное одобрение Code Owner не подтверждено, задание C выполнено частично. Для выполнения командных требований нужны другие участники.
