"""Регрессия: одинаковые пароли не должны давать одинаковые записи."""

from src import auth


def test_equal_passwords_have_distinct_salted_records():
    auth.reset_users()
    try:
        auth.register("alice@example.com", "same-password")
        auth.register("bob@example.com", "same-password")
        assert auth._users["alice@example.com"] != auth._users["bob@example.com"]
        assert auth.login("alice@example.com", "same-password")
        assert auth.login("bob@example.com", "same-password")
        assert not auth.login("bob@example.com", "wrong-password")
    finally:
        auth.reset_users()
