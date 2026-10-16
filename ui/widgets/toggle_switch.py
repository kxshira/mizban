# ui/widgets/toggle_switch.py

from PySide6.QtWidgets import QCheckBox
from PySide6.QtCore import Qt, QPropertyAnimation, QRectF, Property, QEasingCurve, QPointF
from PySide6.QtGui import QPainter, QColor, QPen, QPainterPath

class ToggleSwitch(QCheckBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(46, 26)
        self.setCursor(Qt.PointingHandCursor)

        self._handle_position = 0.0  # 0.0 = left (light), 1.0 = right (dark)

        self.animation = QPropertyAnimation(self, b"handle_position", self)
        self.animation.setEasingCurve(QEasingCurve.InOutCubic)
        self.animation.setDuration(200)

        self.stateChanged.connect(self.start_animation)

        # Default colors
        self.track_color_off = QColor("#C5D5C0")   # light mode track
        self.track_color_on = QColor("#3A4558")    # dark mode track
        self.handle_color = QColor("#FFFFFF")
        self.icon_color = QColor("#5A5A5A")

    def start_animation(self, checked: bool):
        self.animation.stop()
        self.animation.setStartValue(self._handle_position)
        self.animation.setEndValue(1.0 if checked else 0.0)
        self.animation.start()

    def hitButton(self, pos):
        return self.contentsRect().contains(pos)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # ---------- Track ----------
        track_rect = QRectF(0, 0, self.width(), self.height())

        # Smooth track color transition
        r = int(self.track_color_off.red()   + (self.track_color_on.red()   - self.track_color_off.red())   * self._handle_position)
        g = int(self.track_color_off.green() + (self.track_color_on.green() - self.track_color_off.green()) * self._handle_position)
        b = int(self.track_color_off.blue()  + (self.track_color_on.blue()  - self.track_color_off.blue())  * self._handle_position)
        track_color = QColor(r, g, b)

        painter.setPen(Qt.NoPen)
        painter.setBrush(track_color)
        painter.drawRoundedRect(track_rect, 13, 13)

        # ---------- Handle ----------
        handle_radius = 10
        margin = 3
        x = margin + self._handle_position * (self.width() - 2 * margin - handle_radius * 2)
        y = (self.height() - handle_radius * 2) / 2
        handle_rect = QRectF(x, y, handle_radius * 2, handle_radius * 2)

        painter.setBrush(self.handle_color)
        painter.drawEllipse(handle_rect)

        # ---------- Icon (Sun / Moon) ----------
        painter.setPen(QPen(self.icon_color, 1.4))
        painter.setBrush(Qt.NoBrush)

        cx = handle_rect.center().x()
        cy = handle_rect.center().y()

        if self._handle_position < 0.5:
            # Draw Sun
            self.draw_sun(painter, cx, cy, 5.5)
        else:
            # Draw Moon
            self.draw_moon(painter, cx, cy, 5.5)

    def draw_sun(self, painter: QPainter, cx: float, cy: float, radius: float):
        # Circle
        painter.drawEllipse(QPointF(cx, cy), radius * 0.55, radius * 0.55)

        # Rays
        for i in range(8):
            angle = i * 45
            from math import cos, sin, radians
            rad = radians(angle)
            inner = radius * 0.7
            outer = radius * 1.15
            x1 = cx + cos(rad) * inner
            y1 = cy + sin(rad) * inner
            x2 = cx + cos(rad) * outer
            y2 = cy + sin(rad) * outer
            painter.drawLine(QPointF(x1, y1), QPointF(x2, y2))

    def draw_moon(self, painter: QPainter, cx: float, cy: float, radius: float):
        # Crescent moon using two circles
        path = QPainterPath()
        path.addEllipse(QPointF(cx, cy), radius * 0.7, radius * 0.7)

        # Cut out
        cut = QPainterPath()
        cut.addEllipse(QPointF(cx + radius * 0.35, cy - radius * 0.15), radius * 0.6, radius * 0.6)
        path = path.subtracted(cut)

        painter.setBrush(self.icon_color)
        painter.setPen(Qt.NoPen)
        painter.drawPath(path)

    def get_handle_position(self):
        return self._handle_position

    def set_handle_position(self, pos: float):
        self._handle_position = pos
        self.update()

    handle_position = Property(float, get_handle_position, set_handle_position)

    def set_colors(self, track_off: str, track_on: str, handle: str = "#FFFFFF", icon: str = "#5A5A5A"):
        self.track_color_off = QColor(track_off)
        self.track_color_on = QColor(track_on)
        self.handle_color = QColor(handle)
        self.icon_color = QColor(icon)
        self.update()