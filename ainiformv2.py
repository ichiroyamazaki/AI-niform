import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QComboBox, QStackedLayout
from PyQt5.QtCore import Qt, QTimer, QDateTime, pyqtSignal
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtMultimedia import QCamera, QCameraImageCapture, QCameraInfo, QCameraViewfinderSettings
from PyQt5.QtMultimediaWidgets import QCameraViewfinder

class IDScanApp(QWidget):
    def __init__(self):
        super().__init__()
        self.camera = None
        self.viewfinder = None
        self.secret_buffer = ''
        self.dummy_tap_window = None
        self.user_info = None
        self.check_in_time = None
        self.initUI()
        self.start_camera()

    def initUI(self):
        self.setWindowTitle('ID Scan')
        self.setGeometry(100, 100, 1024, 768) # Same size as main app for consistency

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Top Bar
        top_bar = QWidget()
        top_bar.setFixedHeight(80)
        top_bar.setStyleSheet("background-color: #ADD8E6;") # Light blue
        top_bar_layout = QHBoxLayout()
        top_bar_layout.setContentsMargins(0, 0, 0, 0)
        self.top_bar_label = QLabel("Please tap your ID to the Card Reader.") # Make instance variable
        self.top_bar_label.setAlignment(Qt.AlignCenter)
        self.top_bar_label.setFont(QFont("Arial", 24, QFont.Bold))
        self.top_bar_label.setStyleSheet("color: black;")
        top_bar_layout.addWidget(self.top_bar_label)
        top_bar.setLayout(top_bar_layout)
        main_layout.addWidget(top_bar)

        # Main Content Area
        content_area = QWidget()
        content_area.setStyleSheet("background-color: white;")
        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        # Left side of content area (Date and Time)
        left_content = QWidget()
        left_content.setStyleSheet("background-color: #007BFF;") # Blue
        left_content.setFixedWidth(300) # Fixed width for the blue section
        left_content_layout = QVBoxLayout()
        left_content_layout.setAlignment(Qt.AlignCenter)
        
        self.date_label_scan = QLabel(QDateTime.currentDateTime().toString("MMMM d, yyyy")) # Make instance variable
        self.date_label_scan.setFont(QFont("Arial", 30, QFont.Bold))
        self.date_label_scan.setStyleSheet("color: white;")
        self.date_label_scan.setAlignment(Qt.AlignCenter)
        left_content_layout.addWidget(self.date_label_scan)

        self.time_label_scan = QLabel(QDateTime.currentDateTime().toString("hh:mm:ss ap")) # Make instance variable
        self.time_label_scan.setFont(QFont("Arial", 30, QFont.Bold))
        self.time_label_scan.setStyleSheet("color: white;")
        self.time_label_scan.setAlignment(Qt.AlignCenter)
        left_content_layout.addWidget(self.time_label_scan)

        left_content.setLayout(left_content_layout)
        content_layout.addWidget(left_content, 1) # Less stretch to the left side

        # Right side of content area (Camera feed / Dynamic Content)
        right_content = QWidget()
        right_content.setStyleSheet("background-color: black;") # Default black background
        self.right_content_layout_stacked = QStackedLayout() # Use QStackedLayout
        self.right_content_layout_stacked.setContentsMargins(0,0,0,0)
        self.right_content_layout_stacked.setSpacing(0)

        # Camera Viewfinder Widget
        camera_widget = QWidget()
        camera_layout = QVBoxLayout(camera_widget)
        camera_layout.setContentsMargins(0,0,0,0)
        camera_layout.setSpacing(0)
        self.viewfinder = QCameraViewfinder(self)
        camera_layout.addWidget(self.viewfinder)
        self.right_content_layout_stacked.addWidget(camera_widget)

        # Placeholder/Message Widget
        message_widget = QWidget()
        message_layout = QVBoxLayout(message_widget)
        message_layout.setAlignment(Qt.AlignCenter)
        self.dynamic_message_label = QLabel("Dynamic Message")
        self.dynamic_message_label.setFont(QFont("Arial", 28, QFont.Bold))
        self.dynamic_message_label.setStyleSheet("color: white;")
        self.dynamic_message_label.setAlignment(Qt.AlignCenter)
        message_layout.addWidget(self.dynamic_message_label)
        self.right_content_layout_stacked.addWidget(message_widget)

        right_content.setLayout(self.right_content_layout_stacked)
        content_layout.addWidget(right_content, 2) # More stretch to the right side for the image

        content_area.setLayout(content_layout)
        main_layout.addWidget(content_area, 1) # Allow content area to expand

        # Bottom Bar
        bottom_bar = QWidget()
        bottom_bar.setFixedHeight(80)
        bottom_bar.setStyleSheet("background-color: #DAA520;") # Goldenrod color
        bottom_bar_layout = QHBoxLayout()
        bottom_bar_layout.setContentsMargins(0, 0, 0, 0)
        bottom_bar_label = QLabel("Welcome to STI College Balagtas!")
        bottom_bar_label.setAlignment(Qt.AlignCenter)
        bottom_bar_label.setFont(QFont("Arial", 24, QFont.Bold))
        bottom_bar_label.setStyleSheet("color: white;")
        bottom_bar_layout.addWidget(bottom_bar_label)

        bottom_bar.setLayout(bottom_bar_layout)
        main_layout.addWidget(bottom_bar)

        self.setLayout(main_layout)
        
        # Update time every second
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time_date_scan)
        self.timer.start(1000)
    
    def start_camera(self):
        available_cameras = QCameraInfo.availableCameras()
        if not available_cameras:
            print("No cameras found!")
            return
        
        self.camera = QCamera(available_cameras[0]) # Use the first available camera
        self.camera.setViewfinder(self.viewfinder)
        
        # Set resolution for 360p (480x360 for 4:3 aspect ratio) using QCameraViewfinderSettings
        viewfinder_settings = QCameraViewfinderSettings()
        viewfinder_settings.setResolution(480, 360)
        self.camera.setViewfinderSettings(viewfinder_settings)
        
        self.camera.start()
        self.right_content_layout_stacked.setCurrentIndex(0) # Show camera view

    def closeEvent(self, event):
        if self.camera and self.camera.status() == QCamera.ActiveStatus:
            self.camera.stop()
        super().closeEvent(event)

    def update_time_date_scan(self):
        self.time_label_scan.setText(QDateTime.currentDateTime().toString("hh:mm:ss ap"))
        self.date_label_scan.setText(QDateTime.currentDateTime().toString("MMMM d, yyyy"))
    
    def keyPressEvent(self, event):
        if event.text():
            self.secret_buffer += event.text().lower()
            if len(self.secret_buffer) > 6:
                self.secret_buffer = self.secret_buffer[-6:]
            if self.secret_buffer == 'secret':
                if self.dummy_tap_window is None:
                    self.dummy_tap_window = DummyTapWindow(self)
                self.dummy_tap_window.show()
                self.secret_buffer = ''
        super().keyPressEvent(event)

    # Methods for DummyTapWindow interactions (placeholder implementations)
    def show_wait_message(self, user_info=None):
        self.user_info = user_info
        self.top_bar_label.setText("Processing ID... Please wait.")
        self.dynamic_message_label.setText("Please wait...")
        self.right_content_layout_stacked.setCurrentIndex(1) # Show message view
        QTimer.singleShot(2000, self.reset_to_camera_view)

    def show_invalid_id(self):
        self.top_bar_label.setText("Unknown / Invalid ID Scanned.")
        self.dynamic_message_label.setText("Unknown /\nInvalid ID\nhas been scanned.")
        self.right_content_layout_stacked.setCurrentIndex(1) # Show message view
        QTimer.singleShot(3000, self.reset_to_camera_view)

    def show_special_pass_deactivated_error(self):
        self.top_bar_label.setText("Special Pass Deactivated.")
        self.dynamic_message_label.setText("Special Pass\nis deactivated.")
        self.right_content_layout_stacked.setCurrentIndex(1) # Show message view
        QTimer.singleShot(4000, self.reset_to_camera_view)

    def show_special_pass_wait_then_verified(self, user_info):
        self.user_info = user_info
        self.check_in_time = QDateTime.currentDateTime().toString("hh:mm:ss ap")
        self.top_bar_label.setText("Verifying Special Pass... Please wait.")
        self.dynamic_message_label.setText("Verifying Special Pass...")
        self.right_content_layout_stacked.setCurrentIndex(1) # Show message view
        QTimer.singleShot(2000, self.show_special_pass_verified)

    def show_special_pass_verified(self):
        self.top_bar_label.setText("Special Pass Verified. Thank You!")
        if self.user_info:
            self.dynamic_message_label.setText(f"Special Pass\nRef: {self.user_info.get('id', '')}\nVerified!")
        else:
            self.dynamic_message_label.setText("Special Pass Verified!")
        self.right_content_layout_stacked.setCurrentIndex(1) # Show message view
        QTimer.singleShot(3000, self.reset_to_camera_view)

    def reset_to_camera_view(self):
        self.top_bar_label.setText("Please tap your ID to the Card Reader.")
        self.right_content_layout_stacked.setCurrentIndex(0) # Show camera view


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
        self.close()

    def simulate_invalid(self):
        self.main_window.show_invalid_id()
        self.close()

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
            self.close()
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
        self.close()

class DummyIDApp(QWidget):
    guard_selected = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('AI-niform Dummy ID for Guards')
        self.setGeometry(100, 100, 400, 600) # Adjusted size based on the image
        self.setStyleSheet("background-color: white; border-radius: 10px;") # White background with rounded corners

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 30, 30, 30) # Add some padding
        main_layout.setSpacing(20)

        # Title Label
        title_label = QLabel("AI-niform Dummy ID for Guards")
        title_label.setFont(QFont("Arial", 20, QFont.Bold))
        title_label.setStyleSheet("color: black;")
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        # Names
        names = [
            "Arvin Jay De Guzman",
            "John Jason Domingo",
            "John Patrick Dulap",
            "Ichiro Yamazaki"
        ]

        for name in names:
            button = QPushButton(name)
            button.setFont(QFont("Arial", 18, QFont.Bold))
            button.setStyleSheet(
                "QPushButton { background-color: #FFA500; color: white; border-radius: 10px; padding: 15px; }"
                "QPushButton:pressed { background-color: #FF8C00; }"
            )
            button.setFixedHeight(70)
            button.clicked.connect(lambda _, n=name: self.select_guard(n)) # Connect to new slot
            main_layout.addWidget(button)

        # Close Button
        close_button = QPushButton('Close')
        close_button.setFont(QFont("Arial", 18, QFont.Bold))
        close_button.setStyleSheet(
            "QPushButton { background-color: #FF4500; color: white; border-radius: 10px; padding: 15px; }"
            "QPushButton:pressed { background-color: #CC3700; }"
        )
        close_button.setFixedHeight(70)
        close_button.clicked.connect(self.close) # Connect to close the window
        main_layout.addWidget(close_button)

        self.setLayout(main_layout)

    def select_guard(self, name):
        self.guard_selected.emit(name)
        self.close() # Close the dummy ID app after selection

class AIniformApp(QWidget):
    def __init__(self):
        super().__init__()
        self.secret_sequence = "guard"
        self.typed_sequence = ""
        self.current_guard_name = None # To store the name of the logged-in guard
        self.dummy_id_app = DummyIDApp() # Instantiate the dummy ID app HERE
        self.dummy_id_app.guard_selected.connect(self.handle_guard_selection) # Connect signal HERE
        self.active_id_scan_app = None # To store the currently open IDScanApp instance
        self.initUI()

    def initUI(self):
        self.setWindowTitle('AI-niform Turnstile')
        self.setGeometry(100, 100, 1024, 768) # Adjust window size for better resemblance

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Top Bar
        top_bar = QWidget()
        top_bar.setFixedHeight(80)
        top_bar.setStyleSheet("background-color: #FFA500;") # Orange
        top_bar_layout = QHBoxLayout()
        top_bar_layout.setContentsMargins(0, 0, 0, 0)
        top_bar_label = QLabel("Turnstile is Closed")
        top_bar_label.setAlignment(Qt.AlignCenter)
        top_bar_label.setFont(QFont("Arial", 24, QFont.Bold))
        top_bar_label.setStyleSheet("color: black;")
        top_bar_layout.addWidget(top_bar_label)
        top_bar.setLayout(top_bar_layout)
        main_layout.addWidget(top_bar)

        # Main Content Area
        content_area = QWidget()
        content_area.setStyleSheet("background-color: white;")
        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        # Left side of content area (Logo and AI-niform text)
        left_content = QWidget()
        left_content_layout = QVBoxLayout()
        left_content_layout.setAlignment(Qt.AlignCenter)
        # Placeholder for image - you would load your actual image here
        logo_label = QLabel()
        # For now, let's put a text placeholder until we have the image file
        logo_text_label = QLabel("AI-niform")
        logo_text_label.setFont(QFont("Arial", 60, QFont.Bold))
        # To make "AI-" blue and "niform" black, we would need to use rich text (HTML) or separate QLabels
        # For simplicity, let's make it all dark blue for now
        # Will adjust this later if the user provides the image or asks for specific styling.
        logo_text_label.setText('<span style=\'color: #007BFF;\'>AI-</span><span style=\'color: #1A2B3C;\'>niform</span>')
        logo_label.setAlignment(Qt.AlignCenter)
        left_content_layout.addWidget(logo_label)
        left_content_layout.addWidget(logo_text_label)
        left_content.setLayout(left_content_layout)
        content_layout.addWidget(left_content, 2) # Give more stretch to the left side

        # Right side of content area (Tap ID text)
        right_content = QWidget()
        right_content.setFixedWidth(300) # Fixed width as seen in the image
        right_content.setStyleSheet("background-color: #007BFF;") # Blue
        right_content_layout = QVBoxLayout()
        right_content_layout.setAlignment(Qt.AlignCenter)
        self.tap_id_label = QLabel("Please tap\nyour ID to\nthe Card\nReader.") # Make it an instance variable
        self.tap_id_label.setAlignment(Qt.AlignCenter)
        self.tap_id_label.setFont(QFont("Arial", 20, QFont.Bold))
        self.tap_id_label.setStyleSheet("color: white;")
        right_content_layout.addWidget(self.tap_id_label)

        self.guard_in_charge_label = QLabel("") # New label for guard in charge
        self.guard_in_charge_label.setAlignment(Qt.AlignCenter)
        self.guard_in_charge_label.setFont(QFont("Arial", 14, QFont.Bold))
        self.guard_in_charge_label.setStyleSheet("color: white;")
        right_content_layout.addWidget(self.guard_in_charge_label)
        self.guard_in_charge_label.hide() # Initially hidden

        right_content.setLayout(right_content_layout)
        content_layout.addWidget(right_content, 1) # Less stretch to the right side

        content_area.setLayout(content_layout)
        main_layout.addWidget(content_area, 1) # Allow content area to expand

        # Bottom Bar
        bottom_bar = QWidget()
        bottom_bar.setFixedHeight(60)
        bottom_bar_layout = QHBoxLayout()
        bottom_bar_layout.setContentsMargins(0, 0, 0, 0)
        bottom_bar_layout.setSpacing(0)

        # Time
        self.time_label = QLabel(QDateTime.currentDateTime().toString("hh:mm:ss ap"))
        self.time_label.setStyleSheet("background-color: #007BFF; color: white; padding-left: 20px;") # Blue
        self.time_label.setFont(QFont("Arial", 16, QFont.Bold))
        self.time_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        bottom_bar_layout.addWidget(self.time_label)

        # Date
        self.date_label = QLabel(QDateTime.currentDateTime().toString("MMMM d, yyyy"))
        self.date_label.setStyleSheet("background-color: #1A2B3C; color: white;") # Dark blue
        self.date_label.setFont(QFont("Arial", 16, QFont.Bold))
        self.date_label.setAlignment(Qt.AlignCenter)
        bottom_bar_layout.addWidget(self.date_label)

        # Quit/Log out Button
        self.action_button = QPushButton('Quit') # Rename and make it an instance variable
        self.action_button.setStyleSheet("background-color: #FFA500; color: white; font-size: 18px; font-weight: bold; border: none;") # Orange
        self.action_button.setFixedSize(120, 60) # Fixed size as seen in the image
        self.action_button.clicked.connect(QApplication.instance().quit) # Default to quitting
        bottom_bar_layout.addWidget(self.action_button)

        # New Guard Login Button (Removed)
        # self.guard_login_button = QPushButton('Guard Login')
        # self.guard_login_button.setStyleSheet("background-color: #D3D35B; color: white; font-size: 18px; font-weight: bold; border: none;")
        # self.guard_login_button.setFixedSize(150, 60)
        # self.guard_login_button.clicked.connect(self.dummy_id_app.show) # Show DummyIDApp
        # bottom_bar_layout.addWidget(self.guard_login_button)
        
        bottom_bar.setLayout(bottom_bar_layout)
        main_layout.addWidget(bottom_bar)

        self.setLayout(main_layout)

        # Update time every second
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time_date)
        self.timer.start(1000)

    def update_time_date(self):
        self.time_label.setText(QDateTime.currentDateTime().toString("hh:mm:ss ap"))
        self.date_label.setText(QDateTime.currentDateTime().toString("MMMM d, yyyy"))
    
    def keyPressEvent(self, event):
        if event.text():
            self.typed_sequence += event.text().lower()
            if len(self.typed_sequence) > len(self.secret_sequence):
                self.typed_sequence = self.typed_sequence[-len(self.secret_sequence):]
            if self.typed_sequence == self.secret_sequence:
                self.dummy_id_app.show()
                self.typed_sequence = "" # Reset typed sequence after showing
        super().keyPressEvent(event)

    def handle_guard_selection(self, guard_name):
        self.current_guard_name = guard_name
        # Update main app UI
        self.tap_id_label.setText("Awaiting ID\ncard scan.")
        self.guard_in_charge_label.setText(f"Guard in-charge:\n{guard_name}")
        self.guard_in_charge_label.show()
        self.action_button.setText('Log out')
        self.action_button.clicked.disconnect() # Disconnect previous connection
        self.action_button.clicked.connect(self.logout_guard) # Connect to logout function

        # Create and show the IDScanApp as a separate window
        if self.active_id_scan_app:
            self.active_id_scan_app.close() # Close existing one if any
            self.active_id_scan_app = None # Clear reference
        self.active_id_scan_app = IDScanApp()
        self.active_id_scan_app.show()

    def logout_guard(self):
        self.current_guard_name = None
        if self.active_id_scan_app and self.active_id_scan_app.isVisible():
            self.active_id_scan_app.close() # Close the ID scan app if it's visible
            self.active_id_scan_app = None # Clear reference
        
        # Revert main app UI to initial state
        self.tap_id_label.setText("Please tap\nyour ID to\nthe Card\nReader.")
        self.guard_in_charge_label.hide()
        self.action_button.setText('Quit')
        self.action_button.clicked.disconnect() # Disconnect logout connection
        self.action_button.clicked.connect(QApplication.instance().quit) # Reconnect to quit

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = AIniformApp()
    ex.show()
    sys.exit(app.exec_())
