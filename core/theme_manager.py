# core/theme_manager.py

from enum import Enum
from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QColor

class Theme(Enum):
    LIGHT = "light"
    DARK = "dark"

class ThemeManager(QObject):
    """مدیریت تم روشن و تاریک برنامه"""

    theme_changed = Signal(Theme)  # وقتی تم عوض شد، این سیگنال ارسال می‌شه

    def __init__(self):
        super().__init__()
        self._current_theme = Theme.LIGHT  # تم پیش‌فرض

        # رنگ‌های تم روشن
        self.light_colors = {
            "background": "#F8F5F0",          # پس‌زمینه اصلی
            "card_background": "#F8F5F0",     # پس‌زمینه کارت لاگین
            "input_background": "#F8F5F0",
            "input_border": "#A8C5A0",        # سبز ملایم
            "input_text": "#2D2D2D",
            "input_placeholder": "#8A8A8A",
            "button_background": "#8FBC8F",   # سبز دکمه‌ی Login
            "button_text": "#FFFFFF",
            "button_hover": "#7AAB7A",
            "text_primary": "#2D2D2D",
            "text_secondary": "#6B6B6B",
            "accent": "#8FBC8F",
            "close_button": "#A0A0A0",
        }

        # رنگ‌های تم تاریک
        self.dark_colors = {
            "background": "#1A1F2E",
            "card_background": "#1A1F2E",
            "input_background": "#1A1F2E",
            "input_border": "#C9B896",        # بژ ملایم
            "input_text": "#E8E0D5",
            "input_placeholder": "#9A9A9A",
            "button_background": "#C9B896",
            "button_text": "#1A1F2E",
            "button_hover": "#B8A785",
            "text_primary": "#E8E0D5",
            "text_secondary": "#A0A0A0",
            "accent": "#C9B896",
            "close_button": "#A0A0A0",
        }

    @property
    def current_theme(self) -> Theme:
        return self._current_theme

    @property
    def colors(self) -> dict:
        """رنگ‌های تم فعلی رو برمی‌گردونه"""
        if self._current_theme == Theme.LIGHT:
            return self.light_colors
        return self.dark_colors

    def toggle_theme(self):
        """تم رو بین روشن و تاریک جابه‌جا می‌کنه"""
        if self._current_theme == Theme.LIGHT:
            self._current_theme = Theme.DARK
        else:
            self._current_theme = Theme.LIGHT

        self.theme_changed.emit(self._current_theme)

    def set_theme(self, theme: Theme):
        """تم رو به صورت مستقیم تنظیم می‌کنه"""
        if theme != self._current_theme:
            self._current_theme = theme
            self.theme_changed.emit(self._current_theme)

    def get_color(self, key: str) -> str:
        """یک رنگ خاص از تم فعلی رو برمی‌گردونه"""
        return self.colors.get(key, "#000000")

# نمونه سراسری
theme_manager = ThemeManager()