"""Модуль аутентификации пользователей."""

import hashlib

# Имитация хранилища пользователей.
_users: dict[str, str] = {}


def _hash_password(password: str) -> str:
    """Возвращает хэш пароля (упрощённо, для учебных целей)."""
    return hashlib.sha256(password.encode()).hexdigest()


def register(email: str, password: str) -> bool:
    """Регистрирует пользователя.

    Raises:
        ValueError: если email некорректен, занят или пароль слишком короткий.
    """
    parts = email.split("@")
    if len(parts) != 2 or not all(part.strip() for part in parts):
        	raise ValueError("Некорректный email")
    if len(password) < 8:
        raise ValueError("Пароль должен содержать минимум 8 символов")
    if email in _users:
        raise ValueError("Пользователь с таким email уже существует")

    _users[email] = _hash_password(password)
    return True


def login(email: str, password: str) -> bool:
    """Возвращает True, если email и пароль совпадают."""
    if email not in _users:
        return False
    return _users[email] == _hash_password(password)


def reset_users() -> None:
    """Очищает хранилище для тестов."""
    _users.clear()