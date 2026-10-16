# core/auth.py

from dataclasses import dataclass
from typing import Optional

@dataclass
class User:
    username: str
    role: str  # فعلاً: "admin", "user", "guest" (بعداً کامل می‌کنیم)

class AuthManager:
    """مدیریت احراز هویت و سشن کاربر"""

    def __init__(self):
        self._current_user: Optional[User] = None

    def login(self, username: str, password: str) -> bool:
        """
        لاگین ساده (فعلاً هاردکد)
        بعداً می‌تونیم به دیتابیس یا فایل امن وصلش کنیم
        """
        # فعلاً برای تست:
        valid_users = {
            "admin": {"password": "admin123", "role": "admin"},
            "user":  {"password": "user123",  "role": "user"},
            "guest": {"password": "guest123", "role": "guest"},
        }

        user_data = valid_users.get(username)
        if user_data and user_data["password"] == password:
            self._current_user = User(username=username, role=user_data["role"])
            return True
        return False

    def logout(self):
        self._current_user = None

    @property
    def is_authenticated(self) -> bool:
        return self._current_user is not None

    @property
    def current_user(self) -> Optional[User]:
        return self._current_user

    def has_permission(self, required_role: str) -> bool:
        """بعداً برای سطح دسترسی استفاده می‌شه"""
        if not self.is_authenticated:
            return False
        # فعلاً ساده
        return True

# یک نمونه سراسری
auth_manager = AuthManager()