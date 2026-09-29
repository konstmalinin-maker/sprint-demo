"""Тесты модуля auth."""

import pytest

from src.auth import register, login, reset_users


@pytest.fixture(autouse=True)
def clean_users():
    reset_users()
    yield
    reset_users()


def test_register_success():
    assert register("user@example.com", "securepass123") is True


def test_register_invalid_email():
    with pytest.raises(ValueError, match="Некорректный email"):
        register("invalid-email", "securepass123")


def test_register_short_password():
    with pytest.raises(ValueError, match="минимум 8 символов"):
        register("user@example.com", "short")


def test_register_duplicate_email():
    register("user@example.com", "securepass123")
    with pytest.raises(ValueError, match="уже существует"):
        register("user@example.com", "otherpass123")


def test_login_success():
    register("user@example.com", "securepass123")
    assert login("user@example.com", "securepass123") is True


def test_login_wrong_password():
    register("user@example.com", "securepass123")
    assert login("user@example.com", "wrongpass") is False


def test_login_unknown_user():
    assert login("nobody@example.com", "anypassword") is False

@pytest.mark.parametrize(
    "email",
    ["@example.com", "user@", "user@@example.com"],
)
def test_register_invalid_email_parts(email):
    with pytest.raises(ValueError, match="Некорректный email"):
        register(email, "securepass123")