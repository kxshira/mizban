# main.py

import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt

from ui.login_window import LoginWindow
from ui.main_window import MainWindow
from core.theme_manager import theme_manager

def main():
    # برای نمایش بهتر در مانیتورهای با رزولوشن بالا
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )

    app = QApplication(sys.argv)
    app.setApplicationName("Mizban")
    app.setApplicationVersion("1.0.0")

    # نگه داشتن رفرنس پنجره اصلی
    main_window = None

    def on_login_successful():
        nonlocal main_window
        main_window = MainWindow()
        main_window.show()

    # اول پنجره لاگین رو نشون بده
    login_window = LoginWindow()
    login_window.login_successful.connect(on_login_successful)
    login_window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()