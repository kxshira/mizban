# ui/main_window.py

from PySide6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget
from PySide6.QtCore import Qt

from core.auth import auth_manager
from core.theme_manager import theme_manager, Theme

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        if not auth_manager.is_authenticated:
            raise PermissionError("Unauthorized access: Please log in first.")

        self.setWindowTitle("Mizban")
        self.resize(1000, 650)

        self.setup_ui()
        self.apply_theme()

        theme_manager.theme_changed.connect(self.apply_theme)

    def setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout(central)
        layout.setAlignment(Qt.AlignCenter)

        user = auth_manager.current_user

        self.welcome_label = QLabel(f"Welcome, {user.username}")
        self.welcome_label.setAlignment(Qt.AlignCenter)
        self.welcome_label.setStyleSheet("font-size: 24px; font-weight: bold;")

        self.role_label = QLabel(f"Role: {user.role}")
        self.role_label.setAlignment(Qt.AlignCenter)
        self.role_label.setStyleSheet("font-size: 16px; margin-top: 10px;")

        layout.addWidget(self.welcome_label)
        layout.addWidget(self.role_label)

    def apply_theme(self):
        colors = theme_manager.colors

        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {colors['background']};
            }}
            QLabel {{
                color: {colors['text_primary']};
            }}
        """)