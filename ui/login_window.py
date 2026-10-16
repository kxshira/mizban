# ui/login_window.py

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QComboBox, QFrame, QGraphicsDropShadowEffect
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap, QColor

from core.theme_manager import theme_manager, Theme
from core.auth import auth_manager
from ui.widgets.toggle_switch import ToggleSwitch
from ui.widgets.floating_line_edit import FloatingLineEdit

class LoginWindow(QWidget):
    login_successful = Signal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mizban - Login")
        self.setFixedSize(420, 580)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.setup_ui()
        self.apply_theme()
        self.connect_signals()
        self.center_window()

    def center_window(self):
        screen = self.screen().availableGeometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Main card
        self.card = QFrame()
        self.card.setObjectName("loginCard")
        self.card.setFixedSize(380, 540)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setXOffset(0)
        shadow.setYOffset(8)
        shadow.setColor(QColor(0, 0, 0, 80))
        self.card.setGraphicsEffect(shadow)

        card_layout = QVBoxLayout(self.card)
        card_layout.setContentsMargins(40, 28, 40, 25)
        card_layout.setSpacing(0)

        # Close button
        close_layout = QHBoxLayout()
        close_layout.addStretch()
        self.close_btn = QPushButton("×")
        self.close_btn.setObjectName("closeButton")
        self.close_btn.setFixedSize(28, 28)
        self.close_btn.setCursor(Qt.PointingHandCursor)
        close_layout.addWidget(self.close_btn)
        card_layout.addLayout(close_layout)

        card_layout.addSpacing(8)

        # Logo / Avatar
        self.avatar_label = QLabel()
        self.avatar_label.setFixedSize(140, 140)
        self.avatar_label.setAlignment(Qt.AlignCenter)
        self.avatar_label.setObjectName("avatar")

        pixmap = QPixmap("assets/icons/logo.png")
        if not pixmap.isNull():
            self.avatar_label.setPixmap(
                pixmap.scaled(140, 140, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            )
        else:
            self.avatar_label.setText("Logo")
            self.avatar_label.setStyleSheet("font-size: 18px;")

        avatar_container = QHBoxLayout()
        avatar_container.addStretch()
        avatar_container.addWidget(self.avatar_label)
        avatar_container.addStretch()
        card_layout.addLayout(avatar_container)

        card_layout.addSpacing(26)

        # Username field (Floating Label)
        self.username_input = FloatingLineEdit("username")
        self.username_input.connect_focus_events()
        card_layout.addWidget(self.username_input)

        card_layout.addSpacing(10)

        # Password field (Floating Label)
        self.password_input = FloatingLineEdit("password")
        self.password_input.setEchoMode(self.password_input.input.EchoMode.Password)
        self.password_input.connect_focus_events()
        card_layout.addWidget(self.password_input)

        card_layout.addSpacing(20)

        # Login button
        self.login_btn = QPushButton("Login")
        self.login_btn.setObjectName("loginButton")
        self.login_btn.setFixedHeight(42)
        self.login_btn.setCursor(Qt.PointingHandCursor)
        card_layout.addWidget(self.login_btn)

        card_layout.addSpacing(16)

        # Language selector (placeholder for future i18n)
        lang_layout = QHBoxLayout()
        lang_layout.addStretch()
        self.lang_combo = QComboBox()
        self.lang_combo.addItems(["english", "persian"])
        self.lang_combo.setObjectName("langCombo")
        self.lang_combo.setFixedWidth(100)
        self.lang_combo.setFixedHeight(28)
        lang_layout.addWidget(self.lang_combo)
        lang_layout.addStretch()
        card_layout.addLayout(lang_layout)

        card_layout.addSpacing(12)

        # Theme toggle switch
        theme_layout = QHBoxLayout()
        theme_layout.addStretch()
        self.theme_toggle = ToggleSwitch()
        theme_layout.addWidget(self.theme_toggle)
        theme_layout.addStretch()
        card_layout.addLayout(theme_layout)

        card_layout.addStretch()

        # Version label
        self.version_label = QLabel("build 1.0.0 free")
        self.version_label.setObjectName("versionLabel")
        self.version_label.setAlignment(Qt.AlignLeft)
        card_layout.addWidget(self.version_label)

        main_layout.addWidget(self.card, alignment=Qt.AlignCenter)

    def connect_signals(self):
        self.close_btn.clicked.connect(self.close)
        self.login_btn.clicked.connect(self.handle_login)
        self.theme_toggle.stateChanged.connect(self.on_theme_toggled)

        # Enter key support
        self.username_input.input.returnPressed.connect(self.handle_login)
        self.password_input.input.returnPressed.connect(self.handle_login)

        theme_manager.theme_changed.connect(self.apply_theme)

    def on_theme_toggled(self, checked: bool):
        if checked:
            theme_manager.set_theme(Theme.DARK)
        else:
            theme_manager.set_theme(Theme.LIGHT)

    def apply_theme(self):
        colors = theme_manager.colors
        is_dark = theme_manager.current_theme == Theme.DARK

        # Sync toggle state
        self.theme_toggle.blockSignals(True)
        self.theme_toggle.setChecked(is_dark)
        self.theme_toggle.blockSignals(False)

        # Update toggle colors
        if is_dark:
            self.theme_toggle.set_colors("#3A4558", "#C9B896", "#FFFFFF", "#2D2D2D")
        else:
            self.theme_toggle.set_colors("#C5D5C0", "#8FBC8F", "#FFFFFF", "#5A5A5A")

        # Apply style to floating inputs
        self.username_input.apply_style(colors)
        self.password_input.apply_style(colors)

        self.setStyleSheet(f"""
            QWidget {{
                background: transparent;
            }}

            #loginCard {{
                background-color: {colors['card_background']};
                border-radius: 18px;
            }}

            #closeButton {{
                background: transparent;
                color: {colors['close_button']};
                font-size: 20px;
                font-weight: bold;
                border: none;
            }}
            #closeButton:hover {{
                color: #E74C3C;
            }}

            #avatar {{
                background-color: {colors['input_background']};
                border-radius: 16px;
                border: 2px solid {colors['input_border']};
            }}

            #loginButton {{
                background-color: {colors['button_background']};
                color: {colors['button_text']};
                border: none;
                border-radius: 21px;
                font-size: 15px;
                font-weight: 600;
            }}
            #loginButton:hover {{
                background-color: {colors['button_hover']};
            }}
            #loginButton:pressed {{
                background-color: {colors['button_background']};
            }}

            #langCombo {{
                background-color: transparent;
                color: {colors['text_secondary']};
                border: 1px solid {colors['input_border']};
                border-radius: 8px;
                padding: 2px 8px;
                font-size: 12px;
            }}
            #langCombo::drop-down {{
                border: none;
            }}

            #versionLabel {{
                color: {colors['text_secondary']};
                font-size: 11px;
            }}
        """)

    def handle_login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text()

        if not username or not password:
            self.username_input.setFocus()
            return

        if auth_manager.login(username, password):
            self.login_successful.emit()
            self.close()
        else:
            self.password_input.clear()
            self.password_input.setFocus()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and hasattr(self, '_drag_pos'):
            self.move(event.globalPosition().toPoint() - self._drag_pos)
            event.accept()