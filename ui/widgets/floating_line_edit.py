# ui/widgets/floating_line_edit.py

from PySide6.QtWidgets import QWidget, QLineEdit, QLabel
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property, QPoint
from PySide6.QtGui import QFont

class FloatingLineEdit(QWidget):
    def __init__(self, placeholder: str = "", parent=None):
        super().__init__(parent)

        self._placeholder = placeholder
        self._is_focused = False
        self._has_text = False
        self._label_font_size = 13.0

        self.setFixedHeight(48)
        self.setup_ui()
        self.setup_animations()
        self.connect_focus_events()

    def setup_ui(self):
        # Input field
        self.input = QLineEdit(self)
        self.input.setObjectName("floatingInput")
        self.input.setGeometry(0, 6, 300, 42)  # Will be resized in resizeEvent
        self.input.setAlignment(Qt.AlignCenter)
        self.input.setPlaceholderText("")

        # Floating label
        self.label = QLabel(self._placeholder, self)
        self.label.setObjectName("floatingLabel")
        self.label.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.label.setAlignment(Qt.AlignCenter)

        font = QFont()
        font.setPointSizeF(self._label_font_size)
        self.label.setFont(font)

        # Initial position (centered inside the input)
        self._update_label_geometry(floating=False)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Keep input full width
        self.input.setGeometry(0, 6, self.width(), 42)
        self._update_label_geometry(self._is_focused or self._has_text)

    def setup_animations(self):
        self.anim_pos = QPropertyAnimation(self.label, b"pos")
        self.anim_pos.setDuration(150)
        self.anim_pos.setEasingCurve(QEasingCurve.InOutCubic)

        self.anim_font = QPropertyAnimation(self, b"label_font_size")
        self.anim_font.setDuration(150)
        self.anim_font.setEasingCurve(QEasingCurve.InOutCubic)

    def get_label_font_size(self):
        return self._label_font_size

    def set_label_font_size(self, size: float):
        self._label_font_size = size
        font = self.label.font()
        font.setPointSizeF(size)
        self.label.setFont(font)
        self.label.adjustSize()

    label_font_size = Property(float, get_label_font_size, set_label_font_size)

    def connect_focus_events(self):
        self.input.focusInEvent = self._on_focus_in
        self.input.focusOutEvent = self._on_focus_out
        self.input.textChanged.connect(self._on_text_changed)

    def _on_focus_in(self, event):
        QLineEdit.focusInEvent(self.input, event)
        self._is_focused = True
        self._update_label_state()

    def _on_focus_out(self, event):
        QLineEdit.focusOutEvent(self.input, event)
        self._is_focused = False
        self._update_label_state()

    def _on_text_changed(self, text: str):
        self._has_text = bool(text.strip())
        self._update_label_state()

    def _update_label_geometry(self, floating: bool):
        self.label.adjustSize()
        label_w = self.label.width()
        label_h = self.label.height()

        if floating:
            # Centered above the input
            x = (self.width() - label_w) // 2
            y = 0
        else:
            # Centered inside the input
            x = (self.width() - label_w) // 2
            y = 6 + (42 - label_h) // 2

        self.label.move(x, y)

    def _update_label_state(self):
        should_float = self._is_focused or self._has_text

        self.anim_pos.stop()
        self.anim_font.stop()

        self.label.adjustSize()
        label_w = self.label.width()
        label_h = self.label.height()

        if should_float:
            end_pos = QPoint((self.width() - label_w) // 2, 0)
            end_size = 11.0
        else:
            end_pos = QPoint((self.width() - label_w) // 2, 6 + (42 - label_h) // 2)
            end_size = 13.0

        self.anim_pos.setStartValue(self.label.pos())
        self.anim_pos.setEndValue(end_pos)

        self.anim_font.setStartValue(self._label_font_size)
        self.anim_font.setEndValue(end_size)

        self.anim_pos.start()
        self.anim_font.start()

    def text(self) -> str:
        return self.input.text()

    def setText(self, text: str):
        self.input.setText(text)
        self._has_text = bool(text.strip())
        self._update_label_state()

    def clear(self):
        self.input.clear()
        self._has_text = False
        self._update_label_state()

    def setEchoMode(self, mode):
        self.input.setEchoMode(mode)

    def setFocus(self):
        self.input.setFocus()

    def apply_style(self, colors: dict):
        self.setStyleSheet(f"""
            #floatingInput {{
                background-color: {colors['input_background']};
                color: {colors['input_text']};
                border: 1.5px solid {colors['input_border']};
                border-radius: 21px;
                padding: 0 16px;
                font-size: 14px;
                selection-background-color: {colors['accent']};
            }}
            #floatingInput:focus {{
                border: 1.5px solid {colors['accent']};
            }}
            #floatingLabel {{
                color: {colors['input_placeholder']};
                background-color: {colors['card_background']};
                padding: 0 6px;
            }}
        """)