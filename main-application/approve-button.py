"""
Approve/Deny main screen UI

This module builds a PyQt5 window that visually matches the provided design:
- Left content panel with a red status header and large Approve/Deny buttons
- Right information panel with STI Balagtas logo, circular user avatar, labels
- Bottom bar with live time, date, and a Logout button

Images expected (relative to this file):
- image-elements/STI Balagtas Logo.png
- image-elements/Generic User Image.jpg
"""

import os
import sys
from datetime import datetime

from PyQt5.QtCore import Qt, QTimer, QSize
from PyQt5.QtGui import QFont, QPixmap, QPainter, QPainterPath, QColor, QGuiApplication
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QFrame,
    QSizePolicy,
)


def resource_path(*relative_parts: str) -> str:
    """Return absolute path for resources next to this script.

    Works both for normal execution and when packaged.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, *relative_parts)


class MainWindow(QMainWindow):
    """Main application window mirroring the provided layout."""

    # Brand and palette colors (approximations based on the screenshot)
    COLOR_RED_HEADER = "#E65673"
    COLOR_APPROVE = "#41BB45"
    COLOR_DENY = "#EA6928"
    COLOR_RIGHT_PANEL = "#177DB3"
    COLOR_BOTTOM_LEFT = "#0E6EAD"
    COLOR_BOTTOM_CENTER = "#0B2437"
    COLOR_BOTTOM_RIGHT = "#E8BFAE"

    WINDOW_WIDTH = 1280
    WINDOW_HEIGHT = 720

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Approve / Deny")
        # Lock window to 1366x768 as requested
        self.setFixedSize(QSize(1366, 768))

        # Capture check-in time at launch and keep it fixed
        self.launch_time = datetime.now()
        self.checkin_time_str = self._format_time(self.launch_time)

        # Build the main layout structure
        central = QWidget(self)
        self.setCentralWidget(central)
        main_vbox = QVBoxLayout(central)
        main_vbox.setContentsMargins(0, 0, 0, 0)
        main_vbox.setSpacing(0)

        content_hbox = QHBoxLayout()
        content_hbox.setContentsMargins(0, 0, 0, 0)
        content_hbox.setSpacing(0)
        main_vbox.addLayout(content_hbox, 1)

        # Left content panel
        left_panel = self._build_left_panel()
        # Align right panel boundary with bottom logout block by using 5:2 ratio
        content_hbox.addWidget(left_panel, 5)

        # Right info panel
        right_panel = self._build_right_panel()
        content_hbox.addWidget(right_panel, 2)

        # Bottom bar spanning the whole width
        bottom_bar = self._build_bottom_bar()
        main_vbox.addWidget(bottom_bar, 0)

        # Live clock timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._update_time_and_date)
        self.timer.start(1000)
        self._update_time_and_date()

        # Ensure window opens on the primary (first) display
        self._move_to_primary_screen()

    # ------------------- Builders -------------------
    def _build_left_panel(self) -> QWidget:
        container = QFrame()
        container.setStyleSheet("background-color: white;")

        vbox = QVBoxLayout(container)
        # Remove outer margins so the red header forms a full-width block
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.setSpacing(18)

        # Status header
        self.status_header = QFrame()
        self.status_header.setStyleSheet(f"background-color: {self.COLOR_RED_HEADER};")
        header_layout = QHBoxLayout(self.status_header)
        header_layout.setContentsMargins(24, 12, 24, 12)
        header_label = QLabel("Turnstile is Closed")
        header_label.setAlignment(Qt.AlignCenter)
        header_label.setStyleSheet("color: white;")
        header_label.setFont(QFont("Arial", 36, QFont.Bold))
        header_layout.addWidget(header_label)
        vbox.addWidget(self.status_header, 0)

        # Content area below header with inner margins for buttons
        content_area = QFrame()
        content_layout = QVBoxLayout(content_area)
        content_layout.setContentsMargins(24, 24, 24, 24)
        content_layout.setSpacing(18)

        # Spacer-like stretch to center buttons vertically
        content_layout.addStretch(1)

        # Approve button
        self.approve_button = QPushButton("Approve")
        self.approve_button.setCursor(Qt.PointingHandCursor)
        self.approve_button.setMinimumHeight(140)
        self.approve_button.setFont(QFont("Arial", 36, QFont.Black))
        self.approve_button.setStyleSheet(
            f"""
            QPushButton {{
                background-color: {self.COLOR_APPROVE};
                color: white;
                border: none;
                border-radius: 8px;
            }}
            QPushButton:pressed {{
                background-color: #36a23a;
            }}
            """
        )
        self.approve_button.clicked.connect(self._handle_approve)
        content_layout.addWidget(self.approve_button, 0)

        # Deny button
        self.deny_button = QPushButton("Deny")
        self.deny_button.setCursor(Qt.PointingHandCursor)
        self.deny_button.setMinimumHeight(120)
        self.deny_button.setFont(QFont("Arial", 32, QFont.Black))
        self.deny_button.setStyleSheet(
            f"""
            QPushButton {{
                background-color: {self.COLOR_DENY};
                color: white;
                border: none;
                border-radius: 8px;
            }}
            QPushButton:pressed {{
                background-color: #cf581e;
            }}
            """
        )
        self.deny_button.clicked.connect(self._handle_deny)
        content_layout.addWidget(self.deny_button, 0)

        content_layout.addStretch(2)
        vbox.addWidget(content_area, 1)
        return container

    def _build_right_panel(self) -> QWidget:
        container = QFrame()
        container.setStyleSheet(f"background-color: {self.COLOR_RIGHT_PANEL};")
        container.setMinimumWidth(360)

        vbox = QVBoxLayout(container)
        vbox.setContentsMargins(24, 24, 24, 24)
        vbox.setSpacing(18)

        # STI Logo
        logo_path = resource_path("image-elements", "STI Balagtas Logo.png")
        logo_label = QLabel()
        logo_label.setAlignment(Qt.AlignCenter)
        if os.path.exists(logo_path):
            pix = QPixmap(logo_path)
            # Constrain to a reasonable height while keeping aspect ratio
            logo_label.setPixmap(pix.scaledToHeight(72, Qt.SmoothTransformation))
        vbox.addWidget(logo_label, 0, Qt.AlignTop)

        # User avatar (squircle)
        avatar_path = resource_path("image-elements", "Generic User Image.jpg")
        avatar_label = QLabel()
        avatar_label.setAlignment(Qt.AlignCenter)
        avatar_label.setFixedSize(220, 220)
        avatar_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        # Squircle (rounded-rect) avatar instead of circle
        avatar_pixmap = self._build_squircle_avatar(avatar_path, avatar_label.size())
        if avatar_pixmap is not None:
            avatar_label.setPixmap(avatar_pixmap)
        vbox.addWidget(avatar_label, 0, Qt.AlignHCenter)

        # ID card title and role
        id_title = QLabel("Test ID Card")
        id_title.setAlignment(Qt.AlignCenter)
        id_title.setStyleSheet("color: white;")
        id_title.setFont(QFont("Arial", 24, QFont.Black))
        vbox.addWidget(id_title)

        role_label = QLabel("(Test User Role)")
        role_label.setAlignment(Qt.AlignCenter)
        role_label.setStyleSheet("color: white;")
        role_label.setFont(QFont("Arial", 16))
        vbox.addWidget(role_label)

        # Time Check-in
        self.checkin_label = QLabel("")
        self.checkin_label.setAlignment(Qt.AlignCenter)
        self.checkin_label.setStyleSheet("color: white;")
        self.checkin_label.setFont(QFont("Arial", 14, QFont.Medium))
        self.checkin_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.checkin_label.setText(f"Time Check-in: {self.checkin_time_str}")
        vbox.addWidget(self.checkin_label, 0, Qt.AlignHCenter)

        vbox.addStretch(1)

        # Guard in-charge
        guard_title = QLabel("Guard in-charge:")
        guard_title.setAlignment(Qt.AlignLeft)
        guard_title.setStyleSheet("color: white;")
        guard_title.setFont(QFont("Arial", 24, QFont.Black))
        vbox.addWidget(guard_title)

        guard_name = QLabel("John Jason Domingo")
        guard_name.setAlignment(Qt.AlignLeft)
        guard_name.setStyleSheet("color: white;")
        guard_name.setFont(QFont("Arial", 18))
        vbox.addWidget(guard_name)

        return container

    def _build_bottom_bar(self) -> QWidget:
        container = QFrame()
        container.setFixedHeight(96)
        hbox = QHBoxLayout(container)
        hbox.setContentsMargins(0, 0, 0, 0)
        hbox.setSpacing(0)

        # Left time area
        left = QFrame()
        left.setStyleSheet(f"background-color: {self.COLOR_BOTTOM_LEFT};")
        left_layout = QHBoxLayout(left)
        left_layout.setContentsMargins(24, 8, 24, 8)
        self.time_label = QLabel("")
        self.time_label.setStyleSheet("color: white;")
        self.time_label.setFont(QFont("Arial", 34, QFont.Black))
        # Center the time within its block
        left_layout.addWidget(self.time_label, 0, Qt.AlignCenter)
        hbox.addWidget(left, 2)

        # Center date area
        center = QFrame()
        center.setStyleSheet(f"background-color: {self.COLOR_BOTTOM_CENTER};")
        center_layout = QHBoxLayout(center)
        center_layout.setContentsMargins(24, 8, 24, 8)
        self.date_label = QLabel("")
        self.date_label.setStyleSheet("color: white;")
        self.date_label.setFont(QFont("Arial", 28, QFont.Black))
        center_layout.addWidget(self.date_label, 0, Qt.AlignCenter)
        hbox.addWidget(center, 3)

        # Right logout area
        right = QFrame()
        right.setStyleSheet(f"background-color: {self.COLOR_BOTTOM_RIGHT};")
        right_layout = QHBoxLayout(right)
        right_layout.setContentsMargins(24, 8, 24, 8)
        logout_btn = QPushButton("Log out")
        logout_btn.setCursor(Qt.PointingHandCursor)
        logout_btn.setStyleSheet(
            """
            QPushButton {
                background-color: transparent;
                color: white;
                border: none;
            }
            QPushButton:pressed {
                color: #f7f3f1;
            }
            """
        )
        logout_btn.setFont(QFont("Arial", 28, QFont.Black))
        logout_btn.clicked.connect(self.close)
        right_layout.addWidget(logout_btn, 0, Qt.AlignCenter)
        hbox.addWidget(right, 2)

        return container

    # ------------------- Helpers -------------------
    def _build_squircle_avatar(self, image_path: str, target_size: QSize) -> QPixmap:
        """Return a squircle-clipped avatar pixmap.

        Uses a rounded rectangle clip with a large radius to approximate a
        squircle look similar to modern OS avatar placeholders.
        """
        if not os.path.exists(image_path):
            return None
        raw = QPixmap(image_path)
        if raw.isNull():
            return None

        width = target_size.width()
        height = target_size.height()
        scaled = raw.scaled(width, height, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)

        result = QPixmap(width, height)
        result.fill(Qt.transparent)

        painter = QPainter(result)
        painter.setRenderHint(QPainter.Antialiasing, True)
        clip_path = QPainterPath()
        radius = int(min(width, height) * 0.22)  # tuned for a squircle feel
        clip_path.addRoundedRect(0, 0, width, height, radius, radius)
        painter.setClipPath(clip_path)
        # Center the scaled pixmap
        x = (width - scaled.width()) // 2
        y = (height - scaled.height()) // 2
        painter.drawPixmap(x, y, scaled)
        painter.end()
        return result

    def _build_circular_avatar(self, image_path: str, target_size: QSize) -> QPixmap:
        if not os.path.exists(image_path):
            return None
        raw = QPixmap(image_path)
        if raw.isNull():
            return None

        diameter = min(target_size.width(), target_size.height())
        scaled = raw.scaled(diameter, diameter, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)

        result = QPixmap(diameter, diameter)
        result.fill(Qt.transparent)

        painter = QPainter(result)
        painter.setRenderHint(QPainter.Antialiasing, True)
        clip_path = QPainterPath()
        clip_path.addEllipse(0, 0, diameter, diameter)
        painter.setClipPath(clip_path)
        painter.drawPixmap(0, 0, scaled)
        painter.end()
        return result

    def _update_time_and_date(self) -> None:
        now = datetime.now()
        time_str = self._format_time(now)
        date_str = now.strftime("%B %-d, %Y") if sys.platform != "win32" else now.strftime("%B %#d, %Y")
        self.time_label.setText(time_str)
        self.date_label.setText(date_str)

    def _format_time(self, dt: datetime) -> str:
        """Return time formatted as e.g. '12:34:56 pm' with leading zero removed."""
        return dt.strftime("%I:%M:%S %p").lstrip("0").replace("AM", "am").replace("PM", "pm")

    def _move_to_primary_screen(self) -> None:
        """Position the window on the first/primary display, centered."""
        screen = QGuiApplication.primaryScreen()
        if screen is None:
            screens = QGuiApplication.screens()
            screen = screens[0] if screens else None
        if screen is None:
            return
        geo = screen.availableGeometry()
        x = geo.x() + (geo.width() - self.width()) // 2
        y = geo.y() + (geo.height() - self.height()) // 2
        self.move(x, y)

    # ------------------- Actions -------------------
    def _handle_approve(self) -> None:
        print("Approve Button Clicked", flush=True)
        app = QApplication.instance()
        if app is not None:
            app.quit()

    def _handle_deny(self) -> None:
        print("Deny Button Clicked", flush=True)
        app = QApplication.instance()
        if app is not None:
            app.quit()

    def _set_status_header(self, open_state: bool) -> None:
        if open_state:
            self.status_header.setStyleSheet("background-color: #2ECC71;")
            # Replace text by recreating child label to ensure consistent centering/contrast
            self._replace_header_text("Turnstile is Open")
        else:
            self.status_header.setStyleSheet(f"background-color: {self.COLOR_RED_HEADER};")
            self._replace_header_text("Turnstile is Closed")

    def _replace_header_text(self, text: str) -> None:
        # Clear existing children and add a new centered label
        for child in self.status_header.findChildren(QWidget):
            child.setParent(None)
        layout = QHBoxLayout(self.status_header)
        layout.setContentsMargins(24, 12, 24, 12)
        label = QLabel(text)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("color: white;")
        label.setFont(QFont("Arial", 36, QFont.Bold))
        layout.addWidget(label)


def main() -> None:
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()


