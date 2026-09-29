"""Модуль аутентификации пользователей."""

import hashlib
from typing import Dict, Optional


# Имитация хранилища пользователей (в реальном проекте — БД)
_users: Dict[str, str] = {}


def _hash_password(password: str) -> str:
    """Возвращает хэш пароля (упрощённо, для учебных целей)."""
    return hashlib.sha256(password.encode()).hexdigest()


def register(email: str, password: str) -> bool:
    """Регистрирует нового пользователя.

    Args:
        email: Email пользователя.
        password: Пароль (минимум 8 символов).

    Returns:
        True, если регистрация успешна.

    Raises:
        ValueError: если email занят или пароль слишком короткий.
    """
    if "@" not in email:
        raise ValueError("Некорректный email")

    if len(password) < 8:
        raise ValueError("Пароль должен содержать минимум 8 символов")

    if email in _users:
        raise ValueError("Пользователь с таким email уже существует")

    _users[email] = _hash_password(password)
    return True


def login(email: str, password: str) -> bool:
    """Проверяет учётные данные пользователя.

    Returns:
        True, если email и пароль совпадают.
    """
    if email not in _users:
        return False

    return _users[email] == _hash_password(password)


def reset_users() -> None:
    """Очищает хранилище (для тестов)."""
    _users.clear()