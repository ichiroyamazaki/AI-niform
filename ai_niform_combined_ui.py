import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFrame, QSizePolicy, QPushButton, QComboBox, QLineEdit
from PyQt5.QtCore import Qt, QTimer, QDateTime
from PyQt5.QtGui import QFont, QPixmap
import subprocess
import threading

# Configurable guard names
guard_names = [
    "Arvin Jay De Guzman",
    "John Jason Domingo",
    "John Patrick Dulap",
    "Ichiro Yamazaki"
]

class GuardUI(QWidget):
    def __init__(self, users_window):
        super().__init__()
        self.setWindowTitle("AI-niform Guard UI")
        self.setMinimumSize(1100, 650)
        self.setStyleSheet("background: white;")
        self.selected_guard = None
        self.power_status = False
        self.users_window = users_window
        self.manual_verification_active = False
        self.manual_user_info = None
        self.manual_check_in_time = None
        self.init_ui()

    def init_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.header = QLabel("Turnstile is Closed")
        self.header.setAlignment(Qt.AlignCenter)
        self.header.setFixedHeight(80)
        self.header.setStyleSheet("background-color: #F4A940; color: #111; font-size: 44px; font-weight: bold; letter-spacing: 1px;")
        self.main_layout.addWidget(self.header)
        self.central_widget = QWidget()
        self.central_layout = QHBoxLayout(self.central_widget)
        self.central_layout.setContentsMargins(0, 0, 0, 0)
        self.central_layout.setSpacing(0)
        self.main_layout.addWidget(self.central_widget, stretch=1)
        self.footer = QFrame()
        self.footer.setStyleSheet("background-color: #FFF45C;")
        self.footer.setFixedHeight(50)
        self.footer_layout = QHBoxLayout(self.footer)
        self.footer_layout.setContentsMargins(20, 0, 20, 0)
        self.footer_layout.setSpacing(0)
        self.date_label = QLabel()
        self.date_label.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        self.date_label.setStyleSheet("color: #111;")
        self.time_label = QLabel()
        self.time_label.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        self.time_label.setStyleSheet("color: #111;")
        self.footer_layout.addWidget(self.date_label, alignment=Qt.AlignLeft)
        self.footer_layout.addStretch(1)
        self.footer_layout.addWidget(self.time_label, alignment=Qt.AlignRight)
        self.main_layout.addWidget(self.footer)
        self.update_datetime()
        timer = QTimer(self)
        timer.timeout.connect(self.update_datetime)
        timer.start(1000)
        self.show_guard_selection()

    def clear_central_layout(self):
        while self.central_layout.count():
            item = self.central_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def show_guard_selection(self):
        self.selected_guard = None
        self.clear_central_layout()
        # Hide Users UI if open
        if self.users_window:
            self.users_window.hide()
        center_widget = QWidget()
        center_widget.setStyleSheet("background: white;")
        center_vlayout = QVBoxLayout(center_widget)
        center_vlayout.setAlignment(Qt.AlignCenter)
        center_vlayout.setContentsMargins(0, 0, 0, 0)
        center_vlayout.setSpacing(20)
        logo_label = QLabel("LOGO")
        logo_label.setAlignment(Qt.AlignCenter)
        logo_label.setFont(QFont("Arial", 32, QFont.Weight.Bold))
        logo_label.setStyleSheet("color: #3A7EDB; letter-spacing: 2px;")
        center_vlayout.addWidget(logo_label)
        appname_label = QLabel("AI-niform")
        appname_label.setAlignment(Qt.AlignCenter)
        appname_label.setFont(QFont("Arial", 48, QFont.Weight.Bold))
        appname_label.setStyleSheet("color: #3A7EDB; letter-spacing: 1px;")
        center_vlayout.addWidget(appname_label)
        center_vlayout.addStretch(1)
        center_vlayout.insertStretch(0, 1)
        self.central_layout.addWidget(center_widget, stretch=4)
        right_panel = QFrame()
        right_panel.setStyleSheet("background-color: #3576B0;")
        right_panel.setFixedWidth(320)
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(30, 30, 30, 30)
        right_layout.setSpacing(25)
        guard_title = QLabel("Guard in-charge")
        guard_title.setStyleSheet("color: white; font-size: 28px; font-weight: bold;")
        guard_title.setFont(QFont("Arial", 22, QFont.Weight.Bold))
        guard_title.setAlignment(Qt.AlignCenter)
        right_layout.addWidget(guard_title)
        right_layout.addSpacing(20)
        for name in guard_names:
            guard_btn = QPushButton(name)
            guard_btn.setCursor(Qt.PointingHandCursor)
            guard_btn.setStyleSheet(
                "background-color: #D3D35B; color: #fff; font-size: 20px; font-weight: bold; "
                "border-radius: 24px; padding: 16px 0; margin-bottom: 0px;"
            )
            guard_btn.setFont(QFont("Arial", 16, QFont.Weight.Bold))
            guard_btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            guard_btn.clicked.connect(lambda checked, n=name: self.show_awaiting_screen(n))
            right_layout.addWidget(guard_btn)
            right_layout.addSpacing(10)
        right_layout.addStretch(1)
        self.central_layout.addWidget(right_panel, stretch=3)

    def show_awaiting_screen(self, guard_name):
        self.selected_guard = guard_name
        if self.users_window:
            self.users_window.guard_name = guard_name  # Set the guard name in STIMonitor
        self.clear_central_layout()
        center_widget = QWidget()
        center_widget.setStyleSheet("background: white;")
        center_vlayout = QVBoxLayout(center_widget)
        center_vlayout.setAlignment(Qt.AlignCenter)
        center_vlayout.setContentsMargins(0, 0, 0, 0)
        center_vlayout.setSpacing(20)
        logo_label = QLabel()
        logo_label.setFixedSize(180, 180)
        logo_label.setStyleSheet("")
        center_vlayout.addWidget(logo_label)
        appname_hlayout = QHBoxLayout()
        ai_label = QLabel("AI")
        ai_label.setFont(QFont("Arial", 80, QFont.Weight.Bold))
        ai_label.setStyleSheet("color: #56A8F5;")
        niform_label = QLabel("-niform")
        niform_label.setFont(QFont("Arial", 80, QFont.Weight.Bold))
        niform_label.setStyleSheet("color: #0A1A2F;")
        appname_hlayout.addWidget(ai_label)
        appname_hlayout.addWidget(niform_label)
        appname_hlayout.setAlignment(Qt.AlignCenter)
        center_vlayout.addLayout(appname_hlayout)
        center_vlayout.addStretch(1)
        center_vlayout.insertStretch(0, 1)
        self.central_layout.addWidget(center_widget, stretch=4)
        right_panel = QFrame()
        right_panel.setStyleSheet("background-color: #3576B0;")
        right_panel.setFixedWidth(320)
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(30, 30, 30, 30)
        right_layout.setSpacing(25)
        awaiting_label = QLabel("Awaiting ID\ncard scan.")
        awaiting_label.setStyleSheet("color: white; font-size: 32px; font-weight: bold;")
        awaiting_label.setFont(QFont("Arial", 26, QFont.Weight.Bold))
        awaiting_label.setAlignment(Qt.AlignCenter)
        right_layout.addWidget(awaiting_label)
        right_layout.addSpacing(20)
        self.power_label = QLabel()
        self.power_label.setFont(QFont("Arial", 14, QFont.Weight.Normal))
        self.power_label.setAlignment(Qt.AlignCenter)
        right_layout.addWidget(self.power_label)
        self.update_power_label()
        right_layout.addSpacing(10)
        turn_on_btn = QPushButton("Turn on")
        turn_on_btn.setCursor(Qt.PointingHandCursor)
        turn_on_btn.setStyleSheet(
            "background-color: #5FC16E; color: white; font-size: 22px; font-weight: bold; "
            "border-radius: 18px; padding: 12px 0; margin-bottom: 0px;"
        )
        turn_on_btn.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        turn_on_btn.clicked.connect(self.turn_on_power)
        right_layout.addWidget(turn_on_btn)
        turn_off_btn = QPushButton("Turn off")
        turn_off_btn.setCursor(Qt.PointingHandCursor)
        turn_off_btn.setStyleSheet(
            "background-color: #A97B5B; color: white; font-size: 22px; font-weight: bold; "
            "border-radius: 18px; padding: 12px 0; margin-bottom: 0px;"
        )
        turn_off_btn.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        turn_off_btn.clicked.connect(self.turn_off_power)
        right_layout.addWidget(turn_off_btn)
        change_guard_btn = QPushButton("Change Guard")
        change_guard_btn.setCursor(Qt.PointingHandCursor)
        change_guard_btn.setStyleSheet(
            "background-color: #D3D35B; color: #3576B0; font-size: 22px; font-weight: bold; "
            "border-radius: 18px; padding: 12px 0; margin-bottom: 0px;"
        )
        change_guard_btn.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        change_guard_btn.clicked.connect(self.show_guard_selection)
        right_layout.addWidget(change_guard_btn)
        right_layout.addStretch(1)
        self.central_layout.addWidget(right_panel, stretch=3)

    def update_datetime(self):
        now = QDateTime.currentDateTime()
        date_str = now.toString("MMMM d, yyyy")
        time_str = now.toString("hh:mm:ss ap").lower()
        self.date_label.setText(date_str)
        self.time_label.setText(time_str)

    def update_power_label(self):
        if self.power_status:
            self.power_label.setText("Power Status: On")
        else:
            self.power_label.setText("Power Status: Off")
        self.power_label.setStyleSheet("color: white; font-size: 18px; font-weight: bold;")

    def turn_on_power(self):
        self.power_status = True
        self.update_power_label()
        if self.users_window:
            self.users_window.show()

    def turn_off_power(self):
        self.power_status = False
        self.update_power_label()
        if self.users_window:
            self.users_window.force_reset()
            self.users_window.hide()

    def show_manual_verification(self, user_info=None, check_in_time=None):
        self.manual_verification_active = True
        self.manual_user_info = user_info
        self.manual_check_in_time = check_in_time
        self.clear_central_layout()
        # Main layout: left (Approve/Deny), right (user info)
        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        # Left: Approve/Deny
        left_widget = QWidget()
        left_widget.setStyleSheet('background: white;')
        left_layout = QVBoxLayout(left_widget)
        left_layout.setAlignment(Qt.AlignCenter)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(32)
        approve_btn = QPushButton('Approve')
        approve_btn.setFont(QFont('Arial', 44, QFont.Bold))
        approve_btn.setStyleSheet('background-color: #4CAF50; color: white; border-radius: 24px; padding: 36px 0; min-width: 500px;')
        approve_btn.setFixedHeight(120)
        approve_btn.clicked.connect(self.approve_manual_verification)
        left_layout.addWidget(approve_btn)
        deny_btn = QPushButton('Deny')
        deny_btn.setFont(QFont('Arial', 44, QFont.Bold))
        deny_btn.setStyleSheet('background-color: #e65c1c; color: white; border-radius: 24px; padding: 36px 0; min-width: 500px;')
        deny_btn.setFixedHeight(120)
        deny_btn.clicked.connect(self.deny_manual_verification)
        left_layout.addWidget(deny_btn)
        left_layout.addSpacing(10)
        manual_label = QLabel('Manual Verification is required.')
        manual_label.setFont(QFont('Arial', 28, QFont.Bold))
        manual_label.setAlignment(Qt.AlignCenter)
        manual_label.setStyleSheet('color: #111; margin-top: 30px;')
        left_layout.addWidget(manual_label)
        left_layout.addStretch(1)
        main_layout.addWidget(left_widget, 3)
        # Right: User info
        right_panel = QFrame()
        right_panel.setStyleSheet('background-color: #3576B0;')
        right_panel.setFixedWidth(340)
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(30, 30, 30, 30)
        right_layout.setSpacing(18)
        if user_info:
            # Photo
            photo_label = QLabel()
            photo_path = '/Users/ichiroyamazaki/Documents/AIniform/ux-users/image/placeholder.jpg'
            pixmap = QPixmap(photo_path)
            if not pixmap.isNull():
                scaled = pixmap.scaled(120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                photo_label.setPixmap(scaled)
                photo_label.setFixedSize(120, 120)
                photo_label.setStyleSheet('border: 6px solid #222; background: #fff; margin-bottom: 10px;')
            else:
                photo_label.setText('\n\n[Image not found]')
                photo_label.setStyleSheet('color: #888; font-size: 18px; font-style: italic; border: 6px solid #222; background: #fff;')
            right_layout.addWidget(photo_label, alignment=Qt.AlignCenter)
            # Name
            name_label = QLabel(user_info.get('name', ''))
            name_label.setFont(QFont('Arial', 28, QFont.Bold))
            name_label.setStyleSheet('color: #fff;')
            name_label.setAlignment(Qt.AlignCenter)
            right_layout.addWidget(name_label)
            # Role
            role_label = QLabel(f"({user_info.get('role', '')})")
            role_label.setFont(QFont('Arial', 20, QFont.Bold))
            role_label.setStyleSheet('color: #b8e0ff;')
            role_label.setAlignment(Qt.AlignCenter)
            right_layout.addWidget(role_label)
            # Check-in label
            checkin_label = QLabel('Time Check In:')
            checkin_label.setFont(QFont('Arial', 18, QFont.Bold))
            checkin_label.setStyleSheet('color: #fff; margin-top: 30px;')
            checkin_label.setAlignment(Qt.AlignCenter)
            right_layout.addWidget(checkin_label)
            # Check-in time
            time_label = QLabel(check_in_time if check_in_time else '')
            time_label.setFont(QFont('Arial', 20, QFont.Bold))
            time_label.setStyleSheet('color: #fff;')
            time_label.setAlignment(Qt.AlignCenter)
            right_layout.addWidget(time_label)
        right_layout.addStretch(1)
        main_layout.addWidget(right_panel, 2)
        self.central_layout.addWidget(main_widget, stretch=1)
        self.header.setText("Turnstile is Closed")
        self.header.setStyleSheet("background-color: #F4A940; color: #111; font-size: 44px; font-weight: bold; letter-spacing: 1px;")

    def approve_manual_verification(self):
        self.manual_verification_active = False
        if self.users_window:
            self.users_window.show_manual_verification_result(True)
        self.show_approved_confirmation_screen()

    def show_approved_confirmation_screen(self):
        self.clear_central_layout()
        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        # Center: Message
        center_widget = QWidget()
        center_layout = QVBoxLayout(center_widget)
        center_layout.setAlignment(Qt.AlignCenter)
        center_layout.setContentsMargins(0, 0, 0, 0)
        center_layout.setSpacing(0)
        # Add vertical stretch to center the message
        center_layout.addStretch(2)
        message = QLabel("User Identity Verified.")
        message.setFont(QFont('Arial', 48, QFont.Bold))
        message.setAlignment(Qt.AlignCenter)
        message.setStyleSheet('color: #222;')
        center_layout.addWidget(message)
        center_layout.addStretch(1)
        # Guard in-charge label at the bottom left
        guard_label = QLabel()
        guard_name = self.selected_guard if self.selected_guard else ''
        guard_label.setText(f"<b>Guard in-charge:</b> Mr. {guard_name}")
        guard_label.setFont(QFont('Arial', 24, QFont.Bold))
        guard_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        guard_label.setStyleSheet('color: #111; margin-top: 40px; margin-left: 20px;')
        center_layout.addWidget(guard_label, alignment=Qt.AlignLeft)
        main_layout.addWidget(center_widget, 3)
        # Right: User info
        right_panel = QFrame()
        right_panel.setStyleSheet('background-color: #3576B0;')
        right_panel.setFixedWidth(340)
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(30, 30, 30, 30)
        right_layout.setSpacing(18)
        user_info = self.manual_user_info
        check_in_time = self.manual_check_in_time
        if user_info:
            # Photo
            photo_label = QLabel()
            photo_path = '/Users/ichiroyamazaki/Documents/AIniform/ux-users/image/placeholder.jpg'
            pixmap = QPixmap(photo_path)
            if not pixmap.isNull():
                scaled = pixmap.scaled(120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                photo_label.setPixmap(scaled)
                photo_label.setFixedSize(120, 120)
                photo_label.setStyleSheet('border: 6px solid #222; background: #fff; margin-bottom: 10px;')
            else:
                photo_label.setText('\n\n[Image not found]')
                photo_label.setStyleSheet('color: #888; font-size: 18px; font-style: italic; border: 6px solid #222; background: #fff;')
            right_layout.addWidget(photo_label, alignment=Qt.AlignCenter)
            # Name
            name_label = QLabel(user_info.get('name', ''))
            name_label.setFont(QFont('Arial', 28, QFont.Bold))
            name_label.setStyleSheet('color: #fff;')
            name_label.setAlignment(Qt.AlignCenter)
            right_layout.addWidget(name_label)
            # Role
            role_label = QLabel(f"({user_info.get('role', '')})")
            role_label.setFont(QFont('Arial', 20, QFont.Bold))
            role_label.setStyleSheet('color: #b8e0ff;')
            role_label.setAlignment(Qt.AlignCenter)
            right_layout.addWidget(role_label)
            # Check-in label
            checkin_label = QLabel('Time Check In:')
            checkin_label.setFont(QFont('Arial', 18, QFont.Bold))
            checkin_label.setStyleSheet('color: #fff; margin-top: 30px;')
            checkin_label.setAlignment(Qt.AlignCenter)
            right_layout.addWidget(checkin_label)
            # Check-in time
            time_label = QLabel(check_in_time if check_in_time else '')
            time_label.setFont(QFont('Arial', 20, QFont.Bold))
            time_label.setStyleSheet('color: #fff;')
            time_label.setAlignment(Qt.AlignCenter)
            right_layout.addWidget(time_label)
        right_layout.addStretch(1)
        main_layout.addWidget(right_panel, 2)
        self.central_layout.addWidget(main_widget, stretch=1)
        self.header.setText("Turnstile is Open")
        self.header.setStyleSheet("background-color: #C8E6C9; color: #111; font-size: 44px; font-weight: bold; letter-spacing: 1px;")
        # After 5 seconds, return to Awaiting/Turn On/Turn Off screen and set header to closed
        def reset_to_closed():
            self.show_awaiting_screen(self.selected_guard)
            self.header.setText("Turnstile is Closed")
            self.header.setStyleSheet("background-color: #F4A940; color: #111; font-size: 44px; font-weight: bold; letter-spacing: 1px;")
        QTimer.singleShot(5000, reset_to_closed)

    def deny_manual_verification(self):
        self.manual_verification_active = False
        if self.users_window:
            self.users_window.show_manual_verification_result(False)
        self.show_denied_wait_screen()

    def show_denied_wait_screen(self):
        self.clear_central_layout()
        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)
        # Center: Please wait message
        center_layout = QVBoxLayout()
        center_layout.setAlignment(Qt.AlignCenter)
        self.header.setText("Turnstile is Closed")
        self.header.setStyleSheet("background-color: #ffb74d; color: #111; font-size: 44px; font-weight: bold; letter-spacing: 1px;")
        wait_label = QLabel("Please wait...")
        wait_label.setFont(QFont('Arial', 38, QFont.Bold))
        wait_label.setAlignment(Qt.AlignCenter)
        center_layout.addWidget(wait_label)
        main_layout.addLayout(center_layout, 3)
        # Right: User info and denial reason
        right_layout = QVBoxLayout()
        right_layout.setAlignment(Qt.AlignCenter)
        user_info = self.manual_user_info
        if user_info:
            photo_label = QLabel()
            photo_path = '/Users/ichiroyamazaki/Documents/AIniform/ux-users/image/placeholder.jpg'
            pixmap = QPixmap(photo_path)
            if not pixmap.isNull():
                scaled = pixmap.scaled(120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                photo_label.setPixmap(scaled)
                photo_label.setStyleSheet('border: 4px solid #111; background: #fff;')
            else:
                photo_label.setText('\n\n[Image not found]')
                photo_label.setStyleSheet('color: #888; font-size: 18px; font-style: italic; border: 4px solid #111; background: #fff;')
            right_layout.addWidget(photo_label, alignment=Qt.AlignCenter)
            name_label = QLabel(user_info.get('name', ''))
            name_label.setFont(QFont('Arial', 24, QFont.Bold))
            name_label.setStyleSheet('color: #fff;')
            name_label.setAlignment(Qt.AlignCenter)
            right_layout.addWidget(name_label)
            role_label = QLabel(f"({user_info.get('role', '')})")
            role_label.setFont(QFont('Arial', 18, QFont.Bold))
            role_label.setStyleSheet('color: #b8e0ff;')
            role_label.setAlignment(Qt.AlignCenter)
            denial_label = QLabel("Different / Incomplete\nUniform Found.")
            denial_label.setFont(QFont('Arial', 18, QFont.Bold))
            denial_label.setStyleSheet('color: #fff; margin-top: 40px;')
            denial_label.setAlignment(Qt.AlignCenter)
            right_layout.addWidget(denial_label)
        main_layout.addLayout(right_layout, 2)
        self.central_layout.addWidget(main_widget, stretch=1)
        # After 2 seconds, show the report screen
        QTimer.singleShot(2000, self.show_denied_report_screen)

    def show_denied_report_screen(self):
        self.clear_central_layout()
        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        # Center: Report message
        center_widget = QWidget()
        center_layout = QVBoxLayout(center_widget)
        center_layout.setAlignment(Qt.AlignCenter)
        center_layout.setContentsMargins(0, 0, 0, 0)
        center_layout.setSpacing(0)
        center_layout.addStretch(2)
        report_label = QLabel('Report has been generated.')
        report_label.setFont(QFont('Arial', 38, QFont.Bold))
        report_label.setAlignment(Qt.AlignCenter)
        report_label.setStyleSheet('color: #111; font-weight: bold;')
        center_layout.addWidget(report_label)
        user_info = self.manual_user_info
        # Only show parent/guardian subtext for students
        if user_info and user_info.get('role', '').lower() == 'student':
            parent_label = QLabel('Parents/Guardian has been also notified.')
            parent_label.setFont(QFont('Arial', 20))
            parent_label.setAlignment(Qt.AlignCenter)
            parent_label.setStyleSheet('color: #111;')
            center_layout.addWidget(parent_label)
        center_layout.addStretch(1)
        # Guard in-charge label at the bottom left
        guard_label = QLabel()
        guard_name = self.selected_guard if self.selected_guard else ''
        guard_label.setText(f"<b>Guard in-charge:</b> Mr. {guard_name}")
        guard_label.setFont(QFont('Arial', 22, QFont.Bold))
        guard_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        guard_label.setStyleSheet('color: #111; margin-top: 40px; margin-left: 20px;')
        center_layout.addWidget(guard_label, alignment=Qt.AlignLeft)
        main_layout.addWidget(center_widget, 3)
        # Right: User info
        right_panel = QFrame()
        right_panel.setStyleSheet('background-color: #3576B0;')
        right_panel.setFixedWidth(340)
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(30, 30, 30, 30)
        right_layout.setSpacing(18)
        check_in_time = self.manual_check_in_time
        if user_info:
            # Photo
            photo_label = QLabel()
            photo_path = '/Users/ichiroyamazaki/Documents/AIniform/ux-users/image/placeholder.jpg'
            pixmap = QPixmap(photo_path)
            if not pixmap.isNull():
                scaled = pixmap.scaled(120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                photo_label.setPixmap(scaled)
                photo_label.setFixedSize(120, 120)
                photo_label.setStyleSheet('border: 6px solid #222; background: #fff; margin-bottom: 10px;')
            else:
                photo_label.setText('\n\n[Image not found]')
                photo_label.setStyleSheet('color: #888; font-size: 18px; font-style: italic; border: 6px solid #222; background: #fff;')
            right_layout.addWidget(photo_label, alignment=Qt.AlignCenter)
            # Name
            name_label = QLabel(user_info.get('name', ''))
            name_label.setFont(QFont('Arial', 28, QFont.Bold))
            name_label.setStyleSheet('color: #fff;')
            name_label.setAlignment(Qt.AlignCenter)
            right_layout.addWidget(name_label)
            # Role
            role_label = QLabel(f"({user_info.get('role', '')})")
            role_label.setFont(QFont('Arial', 20, QFont.Bold))
            role_label.setStyleSheet('color: #b8e0ff;')
            role_label.setAlignment(Qt.AlignCenter)
            right_layout.addWidget(role_label)
            # Check-in label
            checkin_label = QLabel('Time Check In:')
            checkin_label.setFont(QFont('Arial', 18, QFont.Bold))
            checkin_label.setStyleSheet('color: #fff; margin-top: 30px;')
            checkin_label.setAlignment(Qt.AlignCenter)
            right_layout.addWidget(checkin_label)
            # Check-in time
            time_label = QLabel(check_in_time if check_in_time else '')
            time_label.setFont(QFont('Arial', 20, QFont.Bold))
            time_label.setStyleSheet('color: #fff;')
            time_label.setAlignment(Qt.AlignCenter)
            right_layout.addWidget(time_label)
        right_layout.addStretch(1)
        main_layout.addWidget(right_panel, 2)
        self.central_layout.addWidget(main_widget, stretch=1)
        self.header.setText("Turnstile is Open")
        self.header.setStyleSheet("background-color: #C8E6C9; color: #111; font-size: 44px; font-weight: bold; letter-spacing: 1px;")
        # After 3 seconds, return to Awaiting/Turn On/Turn Off screen and set header to closed
        def reset_to_closed():
            self.show_awaiting_screen(self.selected_guard)
            self.header.setText("Turnstile is Closed")
            self.header.setStyleSheet("background-color: #F4A940; color: #111; font-size: 44px; font-weight: bold; letter-spacing: 1px;")
        QTimer.singleShot(3000, reset_to_closed)

    def show_awaiting_screen_after_confirmation(self):
        self.power_status = True
        # Do NOT hide the main window
        self.show_awaiting_screen(self.selected_guard)
        self.update_power_label()
        self.header.setText("Turnstile is Closed")
        self.header.setStyleSheet("background-color: #F4A940; color: #111; font-size: 44px; font-weight: bold; letter-spacing: 1px;")

    def showEvent(self, event):
        super().showEvent(event)
        self.raise_()
        self.activateWindow()

    def show_invalid_id_screen(self):
        self.clear_central_layout()
        # Main layout: left (logo), right (error message)
        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        # Left: Logo and AI-niform text
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setAlignment(Qt.AlignCenter)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(0)
        logo_label = QLabel()
        logo_path = '/Users/ichiroyamazaki/Documents/AIniform/ux-users/image/logo.png'
        logo_pixmap = QPixmap(logo_path)
        if not logo_pixmap.isNull():
            scaled = logo_pixmap.scaled(160, 160, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo_label.setPixmap(scaled)
        else:
            logo_label.setText('[Logo]')
            logo_label.setStyleSheet('color: #888; font-size: 18px; font-style: italic;')
        logo_label.setAlignment(Qt.AlignCenter)
        left_layout.addWidget(logo_label)
        # AI-niform text
        ainiform_label = QLabel()
        ainiform_label.setText('<span style="color:#56A8F5; font-size:72px; font-weight:bold;">AI</span><span style="color:#111; font-size:72px; font-weight:bold;">-niform</span>')
        ainiform_label.setAlignment(Qt.AlignCenter)
        left_layout.addWidget(ainiform_label)
        left_layout.addStretch(1)
        main_layout.addWidget(left_widget, 3)
        # Right: Error message
        right_panel = QFrame()
        right_panel.setStyleSheet('background-color: #3576B0;')
        right_panel.setFixedWidth(340)
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(30, 30, 30, 30)
        right_layout.setSpacing(0)
        error_label = QLabel('Unknown /\nInvalid ID has\nbeen scanned.')
        error_label.setFont(QFont('Arial', 28, QFont.Bold))
        error_label.setStyleSheet('color: #fff;')
        error_label.setAlignment(Qt.AlignCenter)
        right_layout.addStretch(2)
        right_layout.addWidget(error_label)
        right_layout.addStretch(3)
        main_layout.addWidget(right_panel, 2)
        self.central_layout.addWidget(main_widget, stretch=1)
        self.header.setText('Turnstile is Closed')
        self.header.setStyleSheet('background-color: #F4A940; color: #111; font-size: 44px; font-weight: bold; letter-spacing: 1px;')
        # After 3 seconds, return to the Turn On/Turn Off splash screen
        QTimer.singleShot(3000, lambda: self.show_awaiting_screen(self.selected_guard))

    def show_scanning_id_screen(self):
        self.clear_central_layout()
        # Main layout: left (logo), right (scanning message)
        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        # Left: Logo and AI-niform text
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setAlignment(Qt.AlignCenter)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(0)
        logo_label = QLabel()
        logo_path = '/Users/ichiroyamazaki/Documents/AIniform/ux-users/image/logo.png'
        logo_pixmap = QPixmap(logo_path)
        if not logo_pixmap.isNull():
            scaled = logo_pixmap.scaled(160, 160, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo_label.setPixmap(scaled)
        else:
            logo_label.setText('[Logo]')
            logo_label.setStyleSheet('color: #888; font-size: 18px; font-style: italic;')
        logo_label.setAlignment(Qt.AlignCenter)
        left_layout.addWidget(logo_label)
        # AI-niform text
        ainiform_label = QLabel()
        ainiform_label.setText('<span style="color:#56A8F5; font-size:72px; font-weight:bold;">AI</span><span style="color:#111; font-size:72px; font-weight:bold;">-niform</span>')
        ainiform_label.setAlignment(Qt.AlignCenter)
        left_layout.addWidget(ainiform_label)
        left_layout.addStretch(1)
        main_layout.addWidget(left_widget, 3)
        # Right: Scanning message
        right_panel = QFrame()
        right_panel.setStyleSheet('background-color: #3576B0;')
        right_panel.setFixedWidth(340)
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(30, 30, 30, 30)
        right_layout.setSpacing(0)
        scan_label = QLabel('Scanning ID\ncard,\nplease wait...')
        scan_label.setFont(QFont('Arial', 28, QFont.Bold))
        scan_label.setStyleSheet('color: #fff;')
        scan_label.setAlignment(Qt.AlignCenter)
        right_layout.addStretch(2)
        right_layout.addWidget(scan_label)
        right_layout.addStretch(3)
        main_layout.addWidget(right_panel, 2)
        self.central_layout.addWidget(main_widget, stretch=1)
        self.header.setText('Turnstile is Closed')
        self.header.setStyleSheet('background-color: #F4A940; color: #111; font-size: 44px; font-weight: bold; letter-spacing: 1px;')

    def show_logo_user_info_screen(self, user_info=None, check_in_time=None):
        self.clear_central_layout()
        # Main layout: left (logo), right (user info)
        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        # Left: Logo and AI-niform text
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setAlignment(Qt.AlignCenter)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(0)
        logo_label = QLabel()
        logo_path = '/Users/ichiroyamazaki/Documents/AIniform/ux-users/image/logo.png'
        logo_pixmap = QPixmap(logo_path)
        if not logo_pixmap.isNull():
            scaled = logo_pixmap.scaled(160, 160, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo_label.setPixmap(scaled)
        else:
            logo_label.setText('[Logo]')
            logo_label.setStyleSheet('color: #888; font-size: 18px; font-style: italic;')
        logo_label.setAlignment(Qt.AlignCenter)
        left_layout.addWidget(logo_label)
        # AI-niform text
        ainiform_label = QLabel()
        ainiform_label.setText('<span style="color:#56A8F5; font-size:72px; font-weight:bold;">AI</span><span style="color:#111; font-size:72px; font-weight:bold;">-niform</span>')
        ainiform_label.setAlignment(Qt.AlignCenter)
        left_layout.addWidget(ainiform_label)
        left_layout.addStretch(1)
        main_layout.addWidget(left_widget, 3)
        # Right: User info
        right_panel = QFrame()
        right_panel.setStyleSheet('background-color: #3576B0;')
        right_panel.setFixedWidth(340)
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(30, 30, 30, 30)
        right_layout.setSpacing(18)
        if user_info:
            # Photo
            photo_label = QLabel()
            photo_path = '/Users/ichiroyamazaki/Documents/AIniform/ux-users/image/placeholder.jpg'
            pixmap = QPixmap(photo_path)
            if not pixmap.isNull():
                scaled = pixmap.scaled(120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                photo_label.setPixmap(scaled)
                photo_label.setFixedSize(120, 120)
                photo_label.setStyleSheet('border: 6px solid #222; background: #fff; margin-bottom: 10px;')
            else:
                photo_label.setText('\n\n[Image not found]')
                photo_label.setStyleSheet('color: #888; font-size: 18px; font-style: italic; border: 6px solid #222; background: #fff;')
            right_layout.addWidget(photo_label, alignment=Qt.AlignCenter)
            # Name
            name_label = QLabel(user_info.get('name', ''))
            name_label.setFont(QFont('Arial', 28, QFont.Bold))
            name_label.setStyleSheet('color: #fff;')
            name_label.setAlignment(Qt.AlignCenter)
            right_layout.addWidget(name_label)
            # Role
            role_label = QLabel(f"({user_info.get('role', '')})")
            role_label.setFont(QFont('Arial', 20, QFont.Bold))
            role_label.setStyleSheet('color: #b8e0ff;')
            role_label.setAlignment(Qt.AlignCenter)
            right_layout.addWidget(role_label)
            # Check-in label
            checkin_label = QLabel('Time Check In:')
            checkin_label.setFont(QFont('Arial', 18, QFont.Bold))
            checkin_label.setStyleSheet('color: #fff; margin-top: 30px;')
            checkin_label.setAlignment(Qt.AlignCenter)
            right_layout.addWidget(checkin_label)
            # Check-in time
            time_label = QLabel(check_in_time if check_in_time else '')
            time_label.setFont(QFont('Arial', 20, QFont.Bold))
            time_label.setStyleSheet('color: #fff;')
            time_label.setAlignment(Qt.AlignCenter)
            right_layout.addWidget(time_label)
        right_layout.addStretch(1)
        main_layout.addWidget(right_panel, 2)
        self.central_layout.addWidget(main_widget, stretch=1)
        self.header.setText('Turnstile is Closed')
        self.header.setStyleSheet('background-color: #F4A940; color: #111; font-size: 44px; font-weight: bold; letter-spacing: 1px;')

    def show_manual_verification_wait_screen(self, user_info=None, check_in_time=None, reason=None):
        self.clear_central_layout()
        # Main layout: left (please wait), right (user info)
        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        # Center: Please wait message
        center_widget = QWidget()
        center_layout = QVBoxLayout(center_widget)
        center_layout.setAlignment(Qt.AlignCenter)
        center_layout.setContentsMargins(0, 0, 0, 0)
        center_layout.setSpacing(0)
        center_layout.addStretch(2)
        wait_label = QLabel('Please wait...')
        wait_label.setFont(QFont('Arial', 38, QFont.Bold))
        wait_label.setAlignment(Qt.AlignCenter)
        wait_label.setStyleSheet('color: #111;')
        center_layout.addWidget(wait_label)
        center_layout.addStretch(3)
        main_layout.addWidget(center_widget, 3)
        # Right: User info
        right_panel = QFrame()
        right_panel.setStyleSheet('background-color: #3576B0;')
        right_panel.setFixedWidth(340)
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(30, 30, 30, 30)
        right_layout.setSpacing(18)
        if user_info:
            # Photo
            photo_label = QLabel()
            photo_path = '/Users/ichiroyamazaki/Documents/AIniform/ux-users/image/placeholder.jpg'
            pixmap = QPixmap(photo_path)
            if not pixmap.isNull():
                scaled = pixmap.scaled(120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                photo_label.setPixmap(scaled)
                photo_label.setFixedSize(120, 120)
                photo_label.setStyleSheet('border: 6px solid #222; background: #fff; margin-bottom: 10px;')
            else:
                photo_label.setText('\n\n[Image not found]')
                photo_label.setStyleSheet('color: #888; font-size: 18px; font-style: italic; border: 6px solid #222; background: #fff;')
            right_layout.addWidget(photo_label, alignment=Qt.AlignCenter)
            # Name
            name_label = QLabel(user_info.get('name', ''))
            name_label.setFont(QFont('Arial', 28, QFont.Bold))
            name_label.setStyleSheet('color: #fff;')
            name_label.setAlignment(Qt.AlignCenter)
            right_layout.addWidget(name_label)
            # Role
            role_label = QLabel(f"({user_info.get('role', '')})")
            role_label.setFont(QFont('Arial', 20, QFont.Bold))
            role_label.setStyleSheet('color: #b8e0ff;')
            role_label.setAlignment(Qt.AlignCenter)
            right_layout.addWidget(role_label)
            # Reason (if any)
            if reason:
                reason_label = QLabel(reason)
                reason_label.setFont(QFont('Arial', 18, QFont.Bold))
                reason_label.setStyleSheet('color: #fff; margin-top: 40px;')
                reason_label.setAlignment(Qt.AlignCenter)
                right_layout.addWidget(reason_label)
            # Check-in label
            checkin_label = QLabel('Time Check In:')
            checkin_label.setFont(QFont('Arial', 16, QFont.Bold))
            checkin_label.setStyleSheet('color: #fff; margin-top: 20px;')
            checkin_label.setAlignment(Qt.AlignCenter)
            right_layout.addWidget(checkin_label)
            # Check-in time
            time_label = QLabel(check_in_time if check_in_time else '')
            time_label.setFont(QFont('Arial', 18, QFont.Bold))
            time_label.setStyleSheet('color: #b8e0ff;')
            time_label.setAlignment(Qt.AlignCenter)
            right_layout.addWidget(time_label)
        right_layout.addStretch(1)
        main_layout.addWidget(right_panel, 2)
        self.central_layout.addWidget(main_widget, stretch=1)
        self.header.setText('Turnstile is Closed')
        self.header.setStyleSheet('background-color: #F4A940; color: #111; font-size: 44px; font-weight: bold; letter-spacing: 1px;')

    def show_special_pass_close_screen(self, user_info=None, check_in_time=None):
        self.clear_central_layout()
        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        # Center: Close the Turnstile button
        center_widget = QWidget()
        center_layout = QVBoxLayout(center_widget)
        center_layout.setAlignment(Qt.AlignCenter)
        center_layout.setContentsMargins(0, 0, 0, 0)
        center_layout.setSpacing(0)
        center_layout.addStretch(2)
        close_btn = QPushButton('Close the Turnstile')
        close_btn.setFont(QFont('Arial', 32, QFont.Bold))
        close_btn.setStyleSheet('background-color: #F4A940; color: #fff; border-radius: 18px; padding: 32px 0; min-width: 500px;')
        close_btn.setFixedHeight(90)
        close_btn.clicked.connect(lambda: self.show_awaiting_screen(self.selected_guard))
        center_layout.addWidget(close_btn)
        center_layout.addStretch(3)
        # Guard in-charge label at the bottom left
        guard_label = QLabel()
        guard_name = self.selected_guard if self.selected_guard else ''
        guard_label.setText(f"<b>Guard in-charge:</b> Mr. {guard_name}")
        guard_label.setFont(QFont('Arial', 20, QFont.Bold))
        guard_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        guard_label.setStyleSheet('color: #111; margin-top: 40px; margin-left: 20px;')
        center_layout.addWidget(guard_label, alignment=Qt.AlignLeft)
        main_layout.addWidget(center_widget, 3)
        # Right: Special Pass info
        right_panel = QFrame()
        right_panel.setStyleSheet('background-color: #3576B0;')
        right_panel.setFixedWidth(340)
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(30, 30, 30, 30)
        right_layout.setSpacing(18)
        if user_info:
            # Photo (placeholder for special pass)
            photo_label = QLabel()
            photo_path = '/Users/ichiroyamazaki/Documents/AIniform/ux-users/image/placeholder.jpg'
            pixmap = QPixmap(photo_path)
            if not pixmap.isNull():
                scaled = pixmap.scaled(120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                photo_label.setPixmap(scaled)
                photo_label.setFixedSize(120, 120)
                photo_label.setStyleSheet('border: 6px solid #222; background: #fff; margin-bottom: 10px;')
            else:
                photo_label.setText('\n\n[Image not found]')
                photo_label.setStyleSheet('color: #888; font-size: 18px; font-style: italic; border: 6px solid #222; background: #fff;')
            right_layout.addWidget(photo_label, alignment=Qt.AlignCenter)
            # Special Pass label
            sp_label = QLabel('Special Pass')
            sp_label.setFont(QFont('Arial', 24, QFont.Bold))
            sp_label.setStyleSheet('color: #fff;')
            sp_label.setAlignment(Qt.AlignCenter)
            right_layout.addWidget(sp_label)
            # Ref number
            ref_label = QLabel(f"Ref. {user_info.get('id', '')}")
            ref_label.setFont(QFont('Arial', 16, QFont.Bold))
            ref_label.setStyleSheet('color: #b8e0ff;')
            ref_label.setAlignment(Qt.AlignCenter)
            right_layout.addWidget(ref_label)
            # Check-in label
            checkin_label = QLabel('Time Check In:')
            checkin_label.setFont(QFont('Arial', 16, QFont.Bold))
            checkin_label.setStyleSheet('color: #fff; margin-top: 20px;')
            checkin_label.setAlignment(Qt.AlignCenter)
            right_layout.addWidget(checkin_label)
            # Check-in time
            time_label = QLabel(check_in_time if check_in_time else '')
            time_label.setFont(QFont('Arial', 18, QFont.Bold))
            time_label.setStyleSheet('color: #b8e0ff;')
            time_label.setAlignment(Qt.AlignCenter)
            right_layout.addWidget(time_label)
        right_layout.addStretch(1)
        main_layout.addWidget(right_panel, 2)
        self.central_layout.addWidget(main_widget, stretch=1)
        self.header.setText('Turnstile is Open')
        self.header.setStyleSheet('background-color: #C8E6C9; color: #111; font-size: 44px; font-weight: bold; letter-spacing: 1px;')

class DummyTapWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Dummy ID Tap')
        self.setGeometry(1200, 200, 300, 400)
        layout = QVBoxLayout()
        layout.setSpacing(10)
        check_mode_label = QLabel('Mode:')
        self.check_mode_combo = QComboBox()
        self.check_mode_combo.addItems(['Check In', 'Check Out'])
        check_mode_row = QHBoxLayout()
        check_mode_row.addWidget(check_mode_label)
        check_mode_row.addWidget(self.check_mode_combo)
        layout.addLayout(check_mode_row)
        name_label = QLabel('Name:')
        self.name_input = QLineEdit()
        layout.addWidget(name_label)
        layout.addWidget(self.name_input)
        id_label = QLabel('Student ID Number:')
        self.id_input = QLineEdit()
        layout.addWidget(id_label)
        layout.addWidget(self.id_input)
        course_label = QLabel('Course:')
        self.course_label = course_label
        self.course_combo = QComboBox()
        self.course_combo.addItems(['BSIT / BSCS / BSCpE', 'BSHM', 'BSTM'])
        layout.addWidget(course_label)
        layout.addWidget(self.course_combo)
        role_label = QLabel('Role:')
        self.role_combo = QComboBox()
        self.role_combo.addItems(['Student', 'Teacher', 'Staff'])
        self.role_combo.currentTextChanged.connect(self.update_course_visibility)
        layout.addWidget(role_label)
        layout.addWidget(self.role_combo)
        self.update_course_visibility(self.role_combo.currentText())
        btn = QPushButton('Simulate ID Tap')
        btn.setFont(QFont('Arial', 14, QFont.Bold))
        btn.setStyleSheet('background-color: #3b7bbf; color: white; padding: 10px; border-radius: 8px;')
        btn.clicked.connect(self.simulate_tap)
        layout.addWidget(btn)
        invalid_btn = QPushButton('Invalid ID')
        invalid_btn.setFont(QFont('Arial', 14, QFont.Bold))
        invalid_btn.setStyleSheet('background-color: #d9534f; color: white; padding: 10px; border-radius: 8px;')
        invalid_btn.clicked.connect(self.simulate_invalid)
        layout.addWidget(invalid_btn)
        special_btn = QPushButton('Special Pass Mode')
        special_btn.setFont(QFont('Arial', 14, QFont.Bold))
        special_btn.setStyleSheet('background-color: #ff9800; color: white; padding: 10px; border-radius: 8px;')
        special_btn.clicked.connect(self.show_special_pass_form)
        layout.addWidget(special_btn)
        self.setLayout(layout)

    def update_course_visibility(self, value):
        if value == 'Student':
            self.course_label.setVisible(True)
            self.course_combo.setVisible(True)
            self.course_combo.setEnabled(True)
        else:
            self.course_label.setVisible(False)
            self.course_combo.setVisible(False)
            self.course_combo.setEnabled(False)

    def simulate_tap(self, event=None):
        name = self.name_input.text()
        student_id = self.id_input.text()
        role = self.role_combo.currentText()
        course = self.course_combo.currentText() if role == 'Student' else ''
        check_mode = self.check_mode_combo.currentText()
        display_name = name
        if role == 'Student' and student_id:
            display_name = f"{name}"
        user_info = {
            'name': display_name,
            'id': student_id,
            'role': role,
            'course': course,
            'mode': check_mode
        }
        check_in_time = QDateTime.currentDateTime().toString('hh:mm:ss ap')
        check_in_date = QDateTime.currentDateTime().toString('MMMM d, yyyy')
        print(f"Mode: {check_mode}, Name: {name}, ID: {student_id}, Role: {role}, Course: {course}, Date: {check_in_date}, Check-in Time: {check_in_time}")
        self.main_window.user_info = user_info
        self.main_window.check_in_time = check_in_time
        self.main_window.show_wait_message(user_info)

    def simulate_invalid(self):
        self.main_window.show_invalid_id()
        if hasattr(self.main_window, 'guard_window') and self.main_window.guard_window:
            self.main_window.guard_window.show_invalid_id_screen()

    def show_special_pass_form(self):
        self.special_form = QWidget()
        self.special_form.setWindowTitle('Special Pass Entry')
        self.special_form.setGeometry(1250, 250, 350, 220)
        layout = QVBoxLayout()
        layout.setSpacing(10)
        ref_label = QLabel('Reference Number:')
        self.special_pass_combo = QComboBox()
        self.special_pass_combo.addItems([str(i) for i in range(1, 101)])
        layout.addWidget(ref_label)
        layout.addWidget(self.special_pass_combo)
        active_label = QLabel('Active Card:')
        self.active_combo = QComboBox()
        self.active_combo.addItems(['Yes', 'No'])
        layout.addWidget(active_label)
        layout.addWidget(self.active_combo)
        submit_btn = QPushButton('Simulate Special Pass Tap')
        submit_btn.setFont(QFont('Arial', 14, QFont.Bold))
        submit_btn.setStyleSheet('background-color: #3b7bbf; color: white; padding: 10px; border-radius: 8px;')
        submit_btn.clicked.connect(self.simulate_special_pass)
        layout.addWidget(submit_btn)
        self.special_form.setLayout(layout)
        self.special_form.show()

    def simulate_special_pass(self):
        if self.active_combo.currentText() == 'No':
            self.special_form.close()
            self.main_window.show_special_pass_deactivated_error()
            return
        special_pass_number = self.special_pass_combo.currentText()
        check_mode = self.check_mode_combo.currentText()
        user_info = {
            'name': '',
            'id': special_pass_number,
            'role': 'Special Pass',
            'mode': check_mode
        }
        self.special_form.close()
        self.main_window.show_special_pass_wait_then_verified(user_info)

class STIMonitor(QWidget):
    def __init__(self, guard_window=None):
        super().__init__()
        self.setWindowTitle('AI-niform Main Screen')
        self.setGeometry(100, 100, 1000, 600)
        self.setStyleSheet("background-color: #f6f6f6;")
        self.user_info = {'name': 'Yamazaki, Ichiro P.', 'role': 'Student', 'mode': 'Check In'}
        self.check_in_time = QDateTime.currentDateTime().toString('hh:mm:ss ap')
        self.secret_buffer = ''
        self.dummy_window = None
        self.countdown_value = 3
        self.countdown_timer = None
        self.scanning_timer = None
        self.guard_window = guard_window
        self.guard_name = None  # Add guard_name property
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        self.header_label = QLabel('The Machine is Ready for Operation')
        self.header_label.setAlignment(Qt.AlignCenter)
        self.header_label.setFont(QFont('Arial', 38, QFont.Bold))
        self.header_label.setStyleSheet("background-color: #cbe7fa; color: #222; padding: 36px 0; min-height: 70px;")
        main_layout.addWidget(self.header_label)
        center_frame = QFrame()
        center_layout = QHBoxLayout()
        center_layout.setContentsMargins(0, 0, 0, 0)
        center_layout.setSpacing(0)
        left_frame = QFrame()
        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(0)
        self.group_photo_label = QLabel()
        img_path = '/Users/ichiroyamazaki/Documents/AIniform/ux-users/image/welcome1.jpeg'
        self.group_photo_pixmap = QPixmap(img_path)
        if not self.group_photo_pixmap.isNull():
            scaled = self.group_photo_pixmap.scaled(400, 180, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.group_photo_label.setPixmap(scaled)
        else:
            self.group_photo_label.setText('\n\n[Image not found]')
            self.group_photo_label.setStyleSheet("color: #888; font-size: 18px; font-style: italic;")
        self.group_photo_label.setAlignment(Qt.AlignCenter)
        self.group_photo_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        left_layout.addWidget(self.group_photo_label)
        left_frame.setLayout(left_layout)
        left_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        center_layout.addWidget(left_frame, 2)
        right_frame = QFrame()
        right_frame.setStyleSheet("background-color: #3b7bbf;")
        right_layout = QVBoxLayout(right_frame)
        right_layout.setAlignment(Qt.AlignCenter)
        right_layout.setContentsMargins(30, 30, 30, 30)
        right_layout.setSpacing(25)
        self.right_frame = right_frame
        self.right_layout = right_layout
        self.instruction = QLabel('Please tap your ID to the Card Reader.')
        self.instruction.setFont(QFont('Arial', 22, QFont.Bold))
        self.instruction.setStyleSheet("color: #fff; padding: 40px;")
        self.instruction.setAlignment(Qt.AlignCenter)
        self.instruction.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.right_layout.addWidget(self.instruction)
        right_frame.setLayout(right_layout)
        right_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        center_layout.addWidget(right_frame, 1)
        center_frame.setLayout(center_layout)
        main_layout.addWidget(center_frame)
        bottom_bar = QFrame()
        bottom_bar.setStyleSheet("background-color: #ffe066; min-height: 32px; padding: 4px 0;")
        bottom_layout = QHBoxLayout()
        bottom_layout.setContentsMargins(20, 0, 20, 0)
        self.date_label = QLabel()
        self.date_label.setFont(QFont('Arial', 14, QFont.Bold))
        self.date_label.setStyleSheet("color: #222;")
        self.date_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        bottom_layout.addWidget(self.date_label)
        self.version_label = QLabel('Version 0.0.1')
        self.version_label.setFont(QFont('Arial', 12, QFont.Bold))
        self.version_label.setStyleSheet("color: #888;")
        self.version_label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        bottom_layout.addWidget(self.version_label, 1)
        self.time_label = QLabel()
        self.time_label.setFont(QFont('Arial', 14, QFont.Bold))
        self.time_label.setStyleSheet("color: #222;")
        self.time_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        bottom_layout.addWidget(self.time_label)
        bottom_bar.setLayout(bottom_layout)
        main_layout.addWidget(bottom_bar)
        self.setLayout(main_layout)
        timer = QTimer(self)
        timer.timeout.connect(self.update_datetime)
        timer.start(1000)
        self.update_datetime()

    def update_datetime(self):
        now = QDateTime.currentDateTime()
        self.date_label.setText(now.toString('MMMM d, yyyy'))
        self.time_label.setText(now.toString('hh:mm:ss ap'))

    def keyPressEvent(self, event):
        char = event.text()
        if char:
            self.secret_buffer += char
            if len(self.secret_buffer) > 6:
                self.secret_buffer = self.secret_buffer[-6:]
            if self.secret_buffer.lower() == 'secret':
                if self.dummy_window is None:
                    self.dummy_window = DummyTapWindow(self)
                self.dummy_window.show()
                self.secret_buffer = ''
        super().keyPressEvent(event)

    def show_wait_message(self, user_info=None):
        self.user_info = user_info
        img_path = '/Users/ichiroyamazaki/Documents/AIniform/ux-users/image/instructions1.jpg'
        self.group_photo_pixmap = QPixmap(img_path)
        if not self.group_photo_pixmap.isNull():
            scaled = self.group_photo_pixmap.scaled(400, 180, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.group_photo_label.setPixmap(scaled)
            self.group_photo_label.setStyleSheet('background-color: #000;')
        else:
            self.group_photo_label.setText('\n\n[Image not found]')
            self.group_photo_label.setStyleSheet('color: #888; font-size: 18px; font-style: italic;')
        self.instruction.setText('Please wait...')
        self.instruction.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        if hasattr(self, 'guard_window') and self.guard_window:
            guard_name = self.guard_window.selected_guard
            self.guard_window.show_scanning_id_screen()
            QTimer.singleShot(800, lambda: self.guard_window.show_awaiting_screen(guard_name))
        QTimer.singleShot(800, self.show_user_info)

    def show_user_info(self):
        if self.user_info:
            mode = self.user_info.get('mode', 'Check In')
            check_in_date = QDateTime.currentDateTime().toString('MMMM d, yyyy')
            print(f"Guard: {self.guard_name} | Mode: {mode}, Name: {self.user_info.get('name', '')}, ID: {self.user_info.get('id', '')}, Role: {self.user_info.get('role', '')}, Date: {check_in_date}, Time: {QDateTime.currentDateTime().toString('hh:mm:ss ap')}")
            if hasattr(self, 'guard_window') and self.guard_window:
                self.guard_window.show_logo_user_info_screen(self.user_info, getattr(self, 'check_in_time', None))
            if mode == 'Check Out':
                for i in reversed(range(self.right_layout.count())):
                    widget = self.right_layout.itemAt(i).widget()
                    if widget:
                        widget.setParent(None)
                wait_label = QLabel('Please wait...')
                wait_label.setFont(QFont('Arial', 22, QFont.Bold))
                wait_label.setStyleSheet('color: #fff; padding: 40px;')
                wait_label.setAlignment(Qt.AlignCenter)
                wait_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                self.right_layout.addWidget(wait_label)
                self.check_out_time = QDateTime.currentDateTime().toString('hh:mm:ss ap')
                QTimer.singleShot(800, self.show_verified_screen)
            else:
                for i in reversed(range(self.right_layout.count())):
                    widget = self.right_layout.itemAt(i).widget()
                    if widget:
                        widget.setParent(None)
                name_label = QLabel(self.user_info['name'])
                name_label.setFont(QFont('Arial', 26, QFont.Bold))
                name_label.setStyleSheet('color: #fff;')
                name_label.setAlignment(Qt.AlignCenter)
                name_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                self.right_layout.addWidget(name_label)
                role_label = QLabel(f"({self.user_info['role']})")
                role_label.setFont(QFont('Arial', 18, QFont.Bold))
                role_label.setStyleSheet('color: #b8e0ff;')
                role_label.setAlignment(Qt.AlignCenter)
                role_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                self.right_layout.addWidget(role_label)
                spacer = QLabel()
                spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                self.right_layout.addWidget(spacer)
                checkin_label = QLabel('Time Check In:')
                checkin_label.setFont(QFont('Arial', 16, QFont.Bold))
                checkin_label.setStyleSheet('color: #222; margin-top: 20px;')
                checkin_label.setAlignment(Qt.AlignCenter)
                checkin_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                self.right_layout.addWidget(checkin_label)
                self.check_in_time = QDateTime.currentDateTime().toString('hh:mm:ss ap')
                time_label = QLabel(self.check_in_time)
                time_label.setFont(QFont('Arial', 18, QFont.Bold))
                time_label.setStyleSheet('color: #b8e0ff;')
                time_label.setAlignment(Qt.AlignCenter)
                time_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                self.right_layout.addWidget(checkin_label)
                self.right_layout.addWidget(time_label)
                # Start countdown after showing user info
                self.start_countdown()
        else:
            self.reset_instruction()

    def start_countdown(self):
        self.countdown_value = 3
        self.header_label.setText(f'Getting ready in {self.countdown_value} second(s)...')
        self.header_label.setStyleSheet("background-color: #3b7bbf; color: #fff; padding: 36px 0; min-height: 70px;")
        if self.countdown_timer:
            self.countdown_timer.stop()
        self.countdown_timer = QTimer()
        self.countdown_timer.timeout.connect(self.update_countdown)
        self.countdown_timer.start(1000)

    def update_countdown(self):
        self.countdown_value -= 1
        if self.countdown_value > 0:
            self.header_label.setText(f'Getting ready in {self.countdown_value} second(s)...')
        else:
            self.countdown_timer.stop()
            self.show_scanning_in_progress()

    def show_scanning_in_progress(self):
        self.header_label.setText('Scanning is in progress... Please do not move.')
        self.header_label.setStyleSheet("background-color: #cbe7fa; color: #222; padding: 36px 0; min-height: 70px;")
        img_path = '/Users/ichiroyamazaki/Documents/AIniform/ux-users/image/instructions1.jpg'
        self.group_photo_pixmap = QPixmap(img_path)
        if not self.group_photo_pixmap.isNull():
            label_size = self.group_photo_label.size()
            scaled = self.group_photo_pixmap.scaled(label_size, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
            self.group_photo_label.setPixmap(scaled)
            self.group_photo_label.setStyleSheet('background-color: #000;')
        else:
            self.group_photo_label.setText('\n\n[Image not found]')
            self.group_photo_label.setStyleSheet('color: #888; font-size: 18px; font-style: italic;')
        # After scanning, go directly to camera detection
        if self.scanning_timer:
            self.scanning_timer.stop()
        self.scanning_timer = QTimer()
        self.scanning_timer.setSingleShot(True)
        self.scanning_timer.timeout.connect(self.run_camera_detection)
        self.scanning_timer.start(2000)

    def show_scanning_complete_screen(self):
        print("show_scanning_complete_screen called")
        # Clear right panel
        for i in reversed(range(self.right_layout.count())):
            widget = self.right_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        # Set header
        self.header_label.setText('Please wait for the result.')
        self.header_label.setStyleSheet("background-color: #cbe7fa; color: #222; padding: 36px 0; min-height: 70px;")
        # Show scanok.jpg in the left panel
        img_path = '/Users/ichiroyamazaki/Documents/AIniform/ux-users/image/scanok.jpg'
        self.group_photo_pixmap = QPixmap(img_path)
        if not self.group_photo_pixmap.isNull():
            label_size = self.group_photo_label.size()
            scaled = self.group_photo_pixmap.scaled(label_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.group_photo_label.setPixmap(scaled)
            self.group_photo_label.setStyleSheet('background-color: #000;')
        else:
            self.group_photo_label.setText('\n\n[Image not found]')
            self.group_photo_label.setStyleSheet('color: #888; font-size: 18px; font-style: italic;')
        # Show user info on the right
        if self.user_info:
            name_label = QLabel(self.user_info.get('name', ''))
            name_label.setFont(QFont('Arial', 26, QFont.Bold))
            name_label.setStyleSheet('color: #fff;')
            name_label.setAlignment(Qt.AlignCenter)
            name_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.right_layout.addWidget(name_label)
            role_label = QLabel(f"({self.user_info.get('role', '')})")
            role_label.setFont(QFont('Arial', 18, QFont.Bold))
            role_label.setStyleSheet('color: #b8e0ff;')
            role_label.setAlignment(Qt.AlignCenter)
            role_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.right_layout.addWidget(role_label)
            spacer = QLabel()
            spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.right_layout.addWidget(spacer)
            checkin_label = QLabel('Time Check In:')
            checkin_label.setFont(QFont('Arial', 16, QFont.Bold))
            checkin_label.setStyleSheet('color: #fff; margin-top: 20px;')
            checkin_label.setAlignment(Qt.AlignCenter)
            time_label = QLabel(self.check_in_time if self.check_in_time else '')
            time_label.setFont(QFont('Arial', 18, QFont.Bold))
            time_label.setStyleSheet('color: #b8e0ff;')
            time_label.setAlignment(Qt.AlignCenter)
            self.right_layout.addWidget(checkin_label)
            self.right_layout.addWidget(time_label)
        else:
            spacer = QLabel()
            spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.right_layout.addWidget(spacer)
        # After 1.5 seconds, show the correct result screen
        if hasattr(self, 'last_scan_success') and self.last_scan_success:
            QTimer.singleShot(1500, self.show_verified_screen)
        else:
            QTimer.singleShot(1500, self.show_manual_verification_needed)

    def run_camera_detection(self):
        # Run test ict.py in a thread to avoid blocking UI
        def detection_thread():
            try:
                process = subprocess.Popen(['python3', 'test ict.py', '1'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1, universal_newlines=True)
                detected_objects = set()
                while True:
                    line = process.stdout.readline()
                    if not line and process.poll() is not None:
                        break
                    if line:
                        print(f"Script output: {line.strip()}")
                        if 'DETECTED:' in line:
                            obj = line.split('DETECTED:')[1].strip()
                            detected_objects.add(obj)
                        elif ' : yes' in line:
                            obj = line.split(' : yes')[0].strip()
                            detected_objects.add(obj)
                remaining_output, stderr = process.communicate()
                if remaining_output:
                    print(f"Remaining output: {remaining_output}")
                    for line in remaining_output.split('\n'):
                        if 'DETECTED:' in line:
                            obj = line.split('DETECTED:')[1].strip()
                            detected_objects.add(obj)
                        elif ' : yes' in line:
                            obj = line.split(' : yes')[0].strip()
                            detected_objects.add(obj)
                if stderr:
                    print(f"Script errors: {stderr}")
                valid_detections = any(obj in ['ict-gray-polo', 'ict-pants', 'ict-skirt'] for obj in detected_objects)
                # Store the result and always show the scanning complete screen
                self.last_scan_success = valid_detections
                QTimer.singleShot(0, self.show_scanning_complete_screen)
            except Exception as e:
                print(f"Error running ICT detection: {str(e)}")
                self.last_scan_success = False
                QTimer.singleShot(0, self.show_scanning_complete_screen)
        threading.Thread(target=detection_thread, daemon=True).start()

    def show_manual_verification_needed(self):
        self.header_label.setText('Unable to Verify your Identity')
        self.header_label.setStyleSheet("background-color: #ffb74d; color: #222; padding: 36px 0; min-height: 70px;")
        img_path = '/Users/ichiroyamazaki/Documents/AIniform/ux-users/image/welcome1.jpeg'
        self.group_photo_pixmap = QPixmap(img_path)
        if not self.group_photo_pixmap.isNull():
            label_size = self.group_photo_label.size()
            scaled = self.group_photo_pixmap.scaled(label_size, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
            self.group_photo_label.setPixmap(scaled)
            self.group_photo_label.setStyleSheet("background-color: #000;")
        else:
            self.group_photo_label.setText('\n\n[Image not found]')
            self.group_photo_label.setStyleSheet("color: #888; font-size: 18px; font-style: italic; border: 4px solid #111; background: #fff;")
        for i in reversed(range(self.right_layout.count())):
            widget = self.right_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        manual_label = QLabel('Please wait\nfor the\nManual Verification.')
        manual_label.setFont(QFont('Arial', 32, QFont.Bold))
        manual_label.setStyleSheet("color: #fff; padding: 40px;")
        manual_label.setAlignment(Qt.AlignCenter)
        manual_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.right_layout.addWidget(manual_label)
        # Show the wait screen on the guard monitor
        self.show_manual_verification_wait_on_guard(reason='Different / Incomplete\nUniform Found.')
        # Trigger Guard UI manual verification window with user info
        if self.guard_window:
            self.guard_window.show_manual_verification(self.user_info, self.check_in_time)

    def show_verified_screen(self):
        self.header_label.setText('User Identity Verified. Thank You!')
        self.header_label.setStyleSheet("background-color: #C8E6C9; color: #222; padding: 36px 0; min-height: 70px;")
        img_path = '/Users/ichiroyamazaki/Documents/AIniform/ux-users/image/placeholder.jpg'
        pixmap = QPixmap(img_path)
        for i in reversed(range(self.right_layout.count())):
            widget = self.right_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        if pixmap and not pixmap.isNull():
            label_size = self.group_photo_label.size()
            scaled = pixmap.scaled(label_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.group_photo_label.setPixmap(scaled)
            self.group_photo_label.setStyleSheet("border: 6px solid #111; background: #fff;")
        else:
            self.group_photo_label.setText('\n\n[Image not found]')
            self.group_photo_label.setStyleSheet("color: #888; font-size: 18px; font-style: italic; border: 6px solid #111; background: #fff;")
        role = self.user_info.get('role', '') if self.user_info else ''
        if role == 'Special Pass':
            sp_label = QLabel('Special Pass')
            sp_label.setFont(QFont('Arial', 28, QFont.Bold))
            sp_label.setStyleSheet('color: #fff;')
            sp_label.setAlignment(Qt.AlignCenter)
            ref_label = QLabel(f"Ref. {self.user_info.get('id', '')}")
            ref_label.setFont(QFont('Arial', 18, QFont.Bold))
            ref_label.setStyleSheet('color: #b8e0ff;')
            ref_label.setAlignment(Qt.AlignCenter)
            spacer = QLabel()
            spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.right_layout.addWidget(sp_label)
            self.right_layout.addWidget(ref_label)
            self.right_layout.addWidget(spacer)
        elif role == 'Student':
            name_label = QLabel(self.user_info.get('name', ''))
            name_label.setFont(QFont('Arial', 28, QFont.Bold))
            name_label.setStyleSheet('color: #fff;')
            name_label.setAlignment(Qt.AlignCenter)
            id_label = QLabel(f"Student ID: {self.user_info.get('id', '')}")
            id_label.setFont(QFont('Arial', 18, QFont.Bold))
            id_label.setStyleSheet('color: #b8e0ff;')
            id_label.setAlignment(Qt.AlignCenter)
            spacer = QLabel()
            spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.right_layout.addWidget(name_label)
            self.right_layout.addWidget(id_label)
            self.right_layout.addWidget(spacer)
        else:
            name_label = QLabel(self.user_info.get('name', ''))
            name_label.setFont(QFont('Arial', 28, QFont.Bold))
            name_label.setStyleSheet('color: #fff;')
            name_label.setAlignment(Qt.AlignCenter)
            role_label = QLabel(f"({self.user_info.get('role', '')})")
            role_label.setFont(QFont('Arial', 20, QFont.Bold))
            role_label.setStyleSheet('color: #b8e0ff;')
            role_label.setAlignment(Qt.AlignCenter)
            spacer = QLabel()
            spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.right_layout.addWidget(name_label)
            self.right_layout.addWidget(role_label)
            self.right_layout.addWidget(spacer)
        mode = self.user_info.get('mode', 'Check In') if self.user_info else 'Check In'
        check_in_date = QDateTime.currentDateTime().toString('MMMM d, yyyy')
        # Add print statement for regular user verification
        if role != 'Special Pass':  # Don't print again for special pass as it's already printed
            print(f"Guard: {self.guard_name} | Mode: {mode}, Name: {self.user_info.get('name', '')}, ID: {self.user_info.get('id', '')}, Role: {self.user_info.get('role', '')}, Date: {check_in_date}, Time: {self.check_in_time}")
        if mode == 'Check Out':
            checkout_label = QLabel('Time Check Out:')
            checkout_label.setFont(QFont('Arial', 16, QFont.Bold))
            checkout_label.setStyleSheet('color: #fff; margin-top: 20px;')
            checkout_label.setAlignment(Qt.AlignCenter)
            self.check_out_time = QDateTime.currentDateTime().toString('hh:mm:ss ap')
            time_label = QLabel(self.check_out_time)
            time_label.setFont(QFont('Arial', 18, QFont.Bold))
            time_label.setStyleSheet('color: #b8e0ff;')
            time_label.setAlignment(Qt.AlignCenter)
            self.right_layout.addWidget(checkout_label)
            self.right_layout.addWidget(time_label)
            # Add print statement for check out
            print(f"Guard: {self.guard_name} | Mode: {mode}, Name: {self.user_info.get('name', '')}, ID: {self.user_info.get('id', '')}, Role: {self.user_info.get('role', '')}, Date: {check_in_date}, Time: {self.check_out_time}")
        else:
            checkin_label = QLabel('Time Check In:')
            checkin_label.setFont(QFont('Arial', 16, QFont.Bold))
            checkin_label.setStyleSheet('color: #fff; margin-top: 20px;')
            checkin_label.setAlignment(Qt.AlignCenter)
            time_label = QLabel(self.check_in_time)
            time_label.setFont(QFont('Arial', 18, QFont.Bold))
            time_label.setStyleSheet('color: #b8e0ff;')
            time_label.setAlignment(Qt.AlignCenter)
            self.right_layout.addWidget(checkin_label)
            self.right_layout.addWidget(time_label)
        QTimer.singleShot(5000, self.reset_instruction)

    def show_invalid_id(self):
        for i in reversed(range(self.right_layout.count())):
            widget = self.right_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        self.instruction = QLabel('Please wait...')
        self.instruction.setFont(QFont('Arial', 22, QFont.Bold))
        self.instruction.setStyleSheet("color: #fff; padding: 40px;")
        self.instruction.setAlignment(Qt.AlignCenter)
        self.instruction.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.right_layout.addWidget(self.instruction)
        if hasattr(self, 'guard_window') and self.guard_window:
            guard_name = self.guard_window.selected_guard
            self.guard_window.show_scanning_id_screen()
            QTimer.singleShot(800, lambda: self.guard_window.show_awaiting_screen(guard_name))
        QTimer.singleShot(800, self.show_invalid_message)

    def show_invalid_message(self):
        for i in reversed(range(self.right_layout.count())):
            widget = self.right_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        invalid_label = QLabel('Unknown / Invalid ID has been scanned.')
        invalid_label.setFont(QFont('Arial', 22, QFont.Bold))
        invalid_label.setStyleSheet('color: #fff; padding: 40px;')
        invalid_label.setAlignment(Qt.AlignCenter)
        invalid_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.right_layout.addWidget(invalid_label)
        QTimer.singleShot(3000, self.reset_instruction)

    def show_special_pass_wait_then_verified(self, user_info):
        self.user_info = user_info
        self.check_in_time = QDateTime.currentDateTime().toString('hh:mm:ss ap')
        for i in reversed(range(self.right_layout.count())):
            widget = self.right_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        wait_label = QLabel('Please wait...')
        wait_label.setFont(QFont('Arial', 22, QFont.Bold))
        wait_label.setStyleSheet("color: #fff; padding: 40px;")
        wait_label.setAlignment(Qt.AlignCenter)
        wait_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.right_layout.addWidget(wait_label)
        if hasattr(self, 'guard_window') and self.guard_window:
            guard_name = self.guard_window.selected_guard
            self.guard_window.show_scanning_id_screen()
            QTimer.singleShot(800, lambda: self.guard_window.show_awaiting_screen(guard_name))
        QTimer.singleShot(800, lambda: self.show_special_pass_verified(user_info))

    def show_special_pass_verified(self, user_info):
        self.user_info = user_info
        self.check_in_time = QDateTime.currentDateTime().toString('hh:mm:ss ap')
        check_in_date = QDateTime.currentDateTime().toString('MMMM d, yyyy')
        mode = self.user_info.get('mode', 'Check In')
        # Update print statement to include guard name
        print(f"Guard: {self.guard_name} | Mode: {mode}, Special Pass Ref: {self.user_info['id']}, Date: {check_in_date}, Time: {self.check_in_time}")
        self.header_label.setText('User Identity Verified. Thank You!')
        self.header_label.setStyleSheet("background-color: #C8E6C9; color: #222; padding: 36px 0; min-height: 70px;")
        photo_path = '/Users/ichiroyamazaki/Documents/AIniform/ux-users/image/placeholder.jpg'
        pixmap = QPixmap(photo_path)
        for i in reversed(range(self.right_layout.count())):
            widget = self.right_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        if pixmap and not pixmap.isNull():
            label_size = self.group_photo_label.size()
            scaled = pixmap.scaled(label_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.group_photo_label.setPixmap(scaled)
            self.group_photo_label.setStyleSheet("border: 6px solid #111; background: #fff;")
        else:
            self.group_photo_label.setText('\n\n[Image not found]')
            self.group_photo_label.setStyleSheet("color: #888; font-size: 18px; font-style: italic; border: 6px solid #111; background: #fff;")
        sp_label = QLabel('Special Pass')
        sp_label.setFont(QFont('Arial', 28, QFont.Bold))
        sp_label.setStyleSheet('color: #fff;')
        sp_label.setAlignment(Qt.AlignCenter)
        ref_label = QLabel(f"Ref. {self.user_info['id']}")
        ref_label.setFont(QFont('Arial', 18, QFont.Bold))
        ref_label.setStyleSheet('color: #b8e0ff;')
        ref_label.setAlignment(Qt.AlignCenter)
        spacer = QLabel()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.right_layout.addWidget(sp_label)
        self.right_layout.addWidget(ref_label)
        self.right_layout.addWidget(spacer)
        mode = self.user_info.get('mode', 'Check In')
        if mode == 'Check Out':
            checkout_label = QLabel('Time Check Out:')
            checkout_label.setFont(QFont('Arial', 16, QFont.Bold))
            checkout_label.setStyleSheet('color: #fff; margin-top: 20px;')
            checkout_label.setAlignment(Qt.AlignCenter)
            self.check_out_time = QDateTime.currentDateTime().toString('hh:mm:ss ap')
            time_label = QLabel(self.check_out_time)
            time_label.setFont(QFont('Arial', 18, QFont.Bold))
            time_label.setStyleSheet('color: #b8e0ff;')
            time_label.setAlignment(Qt.AlignCenter)
            self.right_layout.addWidget(checkout_label)
            self.right_layout.addWidget(time_label)
        else:
            checkin_label = QLabel('Time Check In:')
            checkin_label.setFont(QFont('Arial', 16, QFont.Bold))
            checkin_label.setStyleSheet('color: #fff; margin-top: 20px;')
            checkin_label.setAlignment(Qt.AlignCenter)
            time_label = QLabel(self.check_in_time)
            time_label.setFont(QFont('Arial', 18, QFont.Bold))
            time_label.setStyleSheet('color: #b8e0ff;')
            time_label.setAlignment(Qt.AlignCenter)
            self.right_layout.addWidget(checkin_label)
            self.right_layout.addWidget(time_label)
        QTimer.singleShot(5000, self.reset_instruction)

    def show_special_pass_deactivated_error(self):
        self.header_label.setText('The Machine is Ready for Operation')
        self.header_label.setStyleSheet("background-color: #cbe7fa; color: #222; padding: 36px 0; min-height: 70px;")
        img_path = '/Users/ichiroyamazaki/Documents/AIniform/ux-users/image/welcome1.jpeg'
        self.group_photo_pixmap = QPixmap(img_path)
        if not self.group_photo_pixmap.isNull():
            label_size = self.group_photo_label.size()
            scaled = self.group_photo_pixmap.scaled(label_size, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
            self.group_photo_label.setPixmap(scaled)
            self.group_photo_label.setStyleSheet("background-color: #000;")
        else:
            self.group_photo_label.setText('\n\n[Image not found]')
            self.group_photo_label.setStyleSheet("color: #888; font-size: 18px; font-style: italic;")
        for i in reversed(range(self.right_layout.count())):
            widget = self.right_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        wait_label = QLabel('Please wait...')
        wait_label.setFont(QFont('Arial', 22, QFont.Bold))
        wait_label.setStyleSheet("color: #fff; padding: 40px;")
        wait_label.setAlignment(Qt.AlignCenter)
        wait_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.right_layout.addWidget(wait_label)
        if hasattr(self, 'guard_window') and self.guard_window:
            guard_name = self.guard_window.selected_guard
            self.guard_window.show_scanning_id_screen()
            QTimer.singleShot(800, lambda: self.guard_window.show_awaiting_screen(guard_name))
        QTimer.singleShot(800, self.show_special_pass_deactivated_error_message)

    def show_special_pass_deactivated_error_message(self):
        self.header_label.setText('Special Pass Deactivated')
        self.header_label.setStyleSheet("background-color: #f44336; color: #fff; padding: 36px 0; min-height: 70px;")
        img_path = '/Users/ichiroyamazaki/Documents/AIniform/ux-users/image/welcome1.jpeg'
        self.group_photo_pixmap = QPixmap(img_path)
        if not self.group_photo_pixmap.isNull():
            label_size = self.group_photo_label.size()
            scaled = self.group_photo_pixmap.scaled(label_size, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
            self.group_photo_label.setPixmap(scaled)
            self.group_photo_label.setStyleSheet("background-color: #000;")
        else:
            self.group_photo_label.setText('\n\n[Image not found]')
            self.group_photo_label.setStyleSheet("color: #888; font-size: 18px; font-style: italic;")
        for i in reversed(range(self.right_layout.count())):
            widget = self.right_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        error_label = QLabel('This special pass is currently deactivated, please fill-up first to activate')
        error_label.setFont(QFont('Arial', 22, QFont.Bold))
        error_label.setStyleSheet("color: #fff; padding: 40px;")
        error_label.setAlignment(Qt.AlignCenter)
        error_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.right_layout.addWidget(error_label)
        QTimer.singleShot(4000, self.reset_instruction)

    def reset_instruction(self):
        for i in reversed(range(self.right_layout.count())):
            widget = self.right_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        img_path = '/Users/ichiroyamazaki/Documents/AIniform/ux-users/image/welcome1.jpeg'
        self.group_photo_pixmap = QPixmap(img_path)
        if not self.group_photo_pixmap.isNull():
            label_size = self.group_photo_label.size()
            scaled = self.group_photo_pixmap.scaled(label_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.group_photo_label.setPixmap(scaled)
            self.group_photo_label.setStyleSheet("background-color: #000;")
        else:
            self.group_photo_label.setText('\n\n[Image not found]')
            self.group_photo_label.setStyleSheet("color: #888; font-size: 18px; font-style: italic;")
        
        # Clear and reset the right panel
        for i in reversed(range(self.right_layout.count())):
            widget = self.right_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        
        # Add back the default instruction
        self.instruction = QLabel('Please tap your ID to the Card Reader.')
        self.instruction.setFont(QFont('Arial', 22, QFont.Bold))
        self.instruction.setStyleSheet("color: #fff; padding: 40px;")
        self.instruction.setAlignment(Qt.AlignCenter)
        self.instruction.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.right_layout.addWidget(self.instruction)
        self.header_label.setText('The Machine is Ready for Operation')
        self.header_label.setStyleSheet("background-color: #cbe7fa; color: #222; padding: 36px 0; min-height: 70px;")
        self.user_info = None
        self.check_in_time = None

    def show_manual_verification_result(self, approved):
        if approved:
            self.show_verified_screen()
        else:
            self.header_label.setText('Different / Incomplete Uniform Found.')
            self.header_label.setStyleSheet("background-color: #ffb74d; color: #222; padding: 36px 0; min-height: 70px;")
            img_path = '/Users/ichiroyamazaki/Documents/AIniform/ux-users/image/welcome1.jpeg'
            self.group_photo_pixmap = QPixmap(img_path)
            if not self.group_photo_pixmap.isNull():
                label_size = self.group_photo_label.size()
                scaled = self.group_photo_pixmap.scaled(label_size, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
                self.group_photo_label.setPixmap(scaled)
                self.group_photo_label.setStyleSheet("background-color: #000;")
            else:
                self.group_photo_label.setText('\n\n[Image not found]')
                self.group_photo_label.setStyleSheet("color: #888; font-size: 18px; font-style: italic; border: 4px solid #111; background: #fff;")
            for i in reversed(range(self.right_layout.count())):
                widget = self.right_layout.itemAt(i).widget()
                if widget:
                    widget.setParent(None)
            report_layout = QVBoxLayout()
            name_label = QLabel(self.user_info['name']) if self.user_info else QLabel('')
            name_label.setFont(QFont('Arial', 28, QFont.Bold))
            name_label.setStyleSheet('color: #fff;')
            name_label.setAlignment(Qt.AlignCenter)
            role_label = QLabel(f"({self.user_info['role']})") if self.user_info else QLabel('')
            role_label.setFont(QFont('Arial', 20, QFont.Bold))
            role_label.setStyleSheet('color: #b8e0ff;')
            role_label.setAlignment(Qt.AlignCenter)
            report_label = QLabel('Report has been generated.')
            report_label.setFont(QFont('Arial', 18, QFont.Bold))
            report_label.setStyleSheet('color: #fff; margin-top: 20px;')
            report_label.setAlignment(Qt.AlignCenter)
            # Only show parent/guardian subtext for students
            parent_label = None
            if self.user_info and self.user_info.get('role', '').lower() == 'student':
                parent_label = QLabel('Parents/Guardian has been also notified.')
                parent_label.setFont(QFont('Arial', 14))
                parent_label.setStyleSheet('color: #fff;')
                parent_label.setAlignment(Qt.AlignCenter)
            checkin_label = QLabel('Time Check In:')
            checkin_label.setFont(QFont('Arial', 16, QFont.Bold))
            checkin_label.setStyleSheet('color: #fff; margin-top: 20px;')
            checkin_label.setAlignment(Qt.AlignCenter)
            time_label = QLabel(self.check_in_time if self.check_in_time else '')
            time_label.setFont(QFont('Arial', 18, QFont.Bold))
            time_label.setStyleSheet('color: #b8e0ff;')
            time_label.setAlignment(Qt.AlignCenter)
            # Add to right_layout
            self.right_layout.addWidget(name_label)
            self.right_layout.addWidget(role_label)
            self.right_layout.addWidget(report_label)
            if parent_label:
                self.right_layout.addWidget(parent_label)
            self.right_layout.addWidget(checkin_label)
            self.right_layout.addWidget(time_label)
            # Optionally, auto-reset after a delay
            QTimer.singleShot(5000, self.reset_instruction)

    def force_reset(self):
        # Stop any active timers
        if self.countdown_timer:
            self.countdown_timer.stop()
        if self.scanning_timer:
            self.scanning_timer.stop()
        
        # Reset all state variables
        self.user_info = None
        self.check_in_time = None
        self.secret_buffer = ''
        self.countdown_value = 3
        
        # Reset the UI
        self.header_label.setText('The Machine is Ready for Operation')
        self.header_label.setStyleSheet("background-color: #cbe7fa; color: #222; padding: 36px 0; min-height: 70px;")
        
        # Reset the image
        img_path = '/Users/ichiroyamazaki/Documents/AIniform/ux-users/image/welcome1.jpeg'
        self.group_photo_pixmap = QPixmap(img_path)
        if not self.group_photo_pixmap.isNull():
            label_size = self.group_photo_label.size()
            scaled = self.group_photo_pixmap.scaled(label_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.group_photo_label.setPixmap(scaled)
            self.group_photo_label.setStyleSheet("background-color: #000;")
        else:
            self.group_photo_label.setText('\n\n[Image not found]')
            self.group_photo_label.setStyleSheet("color: #888; font-size: 18px; font-style: italic;")
        
        # Clear and reset the right panel
        for i in reversed(range(self.right_layout.count())):
            widget = self.right_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        
        # Add back the default instruction
        self.instruction = QLabel('Please tap your ID to the Card Reader.')
        self.instruction.setFont(QFont('Arial', 22, QFont.Bold))
        self.instruction.setStyleSheet("color: #fff; padding: 40px;")
        self.instruction.setAlignment(Qt.AlignCenter)
        self.instruction.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.right_layout.addWidget(self.instruction)

    def show_logo_user_info_on_guard(self):
        if hasattr(self, 'guard_window') and self.guard_window:
            self.guard_window.show_logo_user_info_screen(self.user_info, getattr(self, 'check_in_time', None))

    def show_manual_verification_wait_on_guard(self, reason=None):
        if hasattr(self, 'guard_window') and self.guard_window:
            self.guard_window.show_manual_verification_wait_screen(self.user_info, getattr(self, 'check_in_time', None), reason)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    guard_window = GuardUI(None)  # Temporary None, will set below
    users_window = STIMonitor(guard_window)
    guard_window.users_window = users_window  # Set the reference
    guard_window.show()
    sys.exit(app.exec_()) 
