import sys
import os
import subprocess
import signal
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QFrame, QGridLayout, QPushButton, QDialog)
from PyQt5.QtCore import QTimer, Qt, QSize
from PyQt5.QtGui import QPixmap, QFont, QPainter, QColor, QPen, QBrush, QPainterPath
from PyQt5.QtSvg import QSvgWidget

class DeveloperModeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Developer Mode")
        self.setFixedSize(800, 600)
        self.setStyleSheet("""
            QDialog {
                background-color: #1E3A8A;
            }
        """)
        
        # Make dialog modal
        self.setModal(True)
        
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Header
        header = QLabel("Developer Mode")
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("""
            QLabel {
                background-color: #DAA520;
                color: white;
                font-family: Arial, sans-serif;
                font-size: 28px;
                font-weight: bold;
                padding: 15px;
                border-radius: 8px;
                min-height: 30px;
            }
        """)
        layout.addWidget(header)
        
        # Status Simulation Section
        status_label = QLabel("Status Simulation:")
        status_label.setStyleSheet("""
            QLabel {
                color: white;
                font-family: Arial, sans-serif;
                font-size: 18px;
                font-weight: bold;
                margin-top: 15px;
                margin-bottom: 5px;
            }
        """)
        layout.addWidget(status_label)
        
        # Invalid ID Button
        invalid_btn = QPushButton("Invalid ID")
        invalid_btn.setMinimumHeight(50)
        invalid_btn.setStyleSheet("""
            QPushButton {
                background-color: #DC3545;
                color: white;
                font-family: Arial, sans-serif;
                font-size: 18px;
                font-weight: bold;
                padding: 12px 20px;
                border-radius: 8px;
                border: none;
                text-align: center;
            }
            QPushButton:hover {
                background-color: #C82333;
            }
            QPushButton:pressed {
                background-color: #A71E2A;
            }
        """)
        invalid_btn.clicked.connect(lambda: self.simulate_status("Invalid ID"))
        layout.addWidget(invalid_btn)
        
        # Deactivated Pass Button
        deactivated_btn = QPushButton("Deactivated Pass")
        deactivated_btn.setMinimumHeight(50)
        deactivated_btn.setStyleSheet("""
            QPushButton {
                background-color: #DC3545;
                color: white;
                font-family: Arial, sans-serif;
                font-size: 18px;
                font-weight: bold;
                padding: 12px 20px;
                border-radius: 8px;
                border: none;
                text-align: center;
            }
            QPushButton:hover {
                background-color: #C82333;
            }
            QPushButton:pressed {
                background-color: #A71E2A;
            }
        """)
        deactivated_btn.clicked.connect(lambda: self.simulate_status("Deactivated Pass"))
        layout.addWidget(deactivated_btn)
        
        # Valid Special Pass Button
        valid_special_btn = QPushButton("Valid Special Pass")
        valid_special_btn.setMinimumHeight(50)
        valid_special_btn.setStyleSheet("""
            QPushButton {
                background-color: #28A745;
                color: white;
                font-family: Arial, sans-serif;
                font-size: 18px;
                font-weight: bold;
                padding: 12px 20px;
                border-radius: 8px;
                border: none;
                text-align: center;
            }
            QPushButton:hover {
                background-color: #218838;
            }
            QPushButton:pressed {
                background-color: #1E7E34;
            }
        """)
        valid_special_btn.clicked.connect(lambda: self.simulate_status("Valid Special Pass"))
        layout.addWidget(valid_special_btn)
        
        # Valid ID Button
        valid_btn = QPushButton("Valid ID")
        valid_btn.setMinimumHeight(50)
        valid_btn.setStyleSheet("""
            QPushButton {
                background-color: #28A745;
                color: white;
                font-family: Arial, sans-serif;
                font-size: 18px;
                font-weight: bold;
                padding: 12px 20px;
                border-radius: 8px;
                border: none;
                text-align: center;
            }
            QPushButton:hover {
                background-color: #218838;
            }
            QPushButton:pressed {
                background-color: #1E7E34;
            }
        """)
        valid_btn.clicked.connect(lambda: self.simulate_status("Valid Pass"))
        layout.addWidget(valid_btn)
        
        # Time Check-out Section
        checkout_label = QLabel("For Time Check-out:")
        checkout_label.setStyleSheet("""
            QLabel {
                color: white;
                font-family: Arial, sans-serif;
                font-size: 18px;
                font-weight: bold;
                margin-top: 15px;
                margin-bottom: 5px;
            }
        """)
        layout.addWidget(checkout_label)
        
        # Special Pass Button
        special_pass_btn = QPushButton("Special Pass")
        special_pass_btn.setMinimumHeight(50)
        special_pass_btn.setStyleSheet("""
            QPushButton {
                background-color: #28A745;
                color: white;
                font-family: Arial, sans-serif;
                font-size: 18px;
                font-weight: bold;
                padding: 12px 20px;
                border-radius: 8px;
                border: none;
                text-align: center;
            }
            QPushButton:hover {
                background-color: #218838;
            }
            QPushButton:pressed {
                background-color: #1E7E34;
            }
        """)
        special_pass_btn.clicked.connect(lambda: self.simulate_status("Special Pass"))
        layout.addWidget(special_pass_btn)
        
        # Student / Teacher / Staff Button
        student_teacher_staff_btn = QPushButton("Student / Teacher / Staff")
        student_teacher_staff_btn.setMinimumHeight(50)
        student_teacher_staff_btn.setStyleSheet("""
            QPushButton {
                background-color: #28A745;
                color: white;
                font-family: Arial, sans-serif;
                font-size: 18px;
                font-weight: bold;
                padding: 12px 20px;
                border-radius: 8px;
                border: none;
                text-align: center;
            }
            QPushButton:hover {
                background-color: #218838;
            }
            QPushButton:pressed {
                background-color: #1E7E34;
            }
        """)
        student_teacher_staff_btn.clicked.connect(lambda: self.simulate_status("Student / Teacher / Staff"))
        layout.addWidget(student_teacher_staff_btn)
        
        # Exit Button
        exit_btn = QPushButton("Exit Developer Mode")
        exit_btn.setMinimumHeight(50)
        exit_btn.setStyleSheet("""
            QPushButton {
                background-color: #FD7E14;
                color: white;
                font-family: Arial, sans-serif;
                font-size: 18px;
                font-weight: bold;
                padding: 12px 20px;
                border-radius: 8px;
                border: none;
                text-align: center;
                margin-top: 10px;
            }
            QPushButton:hover {
                background-color: #E55A00;
            }
            QPushButton:pressed {
                background-color: #CC5200;
            }
        """)
        exit_btn.clicked.connect(self.close)
        layout.addWidget(exit_btn)
    
    def simulate_status(self, status):
        print(f"Simulating status: {status}")
        # Get the parent window (main screen) and trigger the status display
        if self.parent():
            self.parent().show_status_message(status)
        self.close()  # Close developer dialog
    
    def manual_verification(self, action):
        print(f"Manual verification: {action}")
        # Get the parent window (main screen) and trigger the manual verification
        if self.parent():
            self.parent().show_status_message(action)
        self.close()  # Close developer dialog

class STIWelcomeScreen(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI-niform - Main Screen")
        self.setFixedSize(1920, 1080)  # Lock to 1920x1080 resolution
        
        # Position window on secondary monitor if available
        self.position_on_secondary_monitor()
        
        # Set window to fullscreen
        self.showFullScreen()
        
        # Set up the main widget
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        # Create main layout
        layout = QVBoxLayout(main_widget)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.setup_ui(layout)
        self.setup_timer()
        
        # Set window style
        self.setStyleSheet("""
            QMainWindow {
                background-color: white;
            }
        """)
        
        # Developer mode input tracking
        self.developer_input = ""
        self.developer_timeout = None
        
        # Status message tracking
        self.status_timer = None
        self.reset_timer = None
        self.original_instruction_text = "Please tap your ID\nto the Card Reader"
        
        # Scanning sequence tracking
        self.scanning_sequence_step = 0
        self.scanning_overlay = None
        self.sequence_in_progress = False
        
        # Enable key events for returning to login and card scanning
        self.setFocusPolicy(Qt.StrongFocus)
        self.setFocus()  # Set focus to receive keyboard events
        
        # Status file for communication with guard screen
        self.status_file = "main_screen_status.txt"
    
    def closeEvent(self, event):
        """Handle window close event"""
        print("closeEvent called - main screen is closing")
        # Write a status to indicate main screen is closing
        try:
            with open(self.status_file, "w") as f:
                f.write("MAIN_SCREEN_CLOSED\n")
                f.write("N/A\n")
                f.write("N/A\n")
                f.write("N/A\n")
            print("Main screen closing - status written to file")
        except Exception as e:
            print(f"Error writing close status: {e}")
        
        event.accept()
    
    def position_on_secondary_monitor(self):
        """Position the window on the secondary monitor if available"""
        try:
            # Get the application instance to access screen information
            app = QApplication.instance()
            if app:
                screens = app.screens()
                
                if len(screens) > 1:
                    # Get the secondary screen (index 1)
                    secondary_screen = screens[1]
                    secondary_geometry = secondary_screen.geometry()
                    
                    # Calculate position to center the window on the secondary screen
                    x = secondary_geometry.x() + (secondary_geometry.width() - 1920) // 2
                    y = secondary_geometry.y() + (secondary_geometry.height() - 1080) // 2
                    
                    # Set the window geometry on the secondary screen
                    self.setGeometry(x, y, 1920, 1080)
                    print(f"Main screen positioned on secondary monitor at ({x}, {y})")
                else:
                    # Only one screen available, position normally
                    self.setGeometry(0, 0, 1920, 1080)
                    print("Only one monitor detected, positioning on primary monitor")
            else:
                # Fallback positioning
                self.setGeometry(0, 0, 1920, 1080)
                print("Could not detect screens, using fallback positioning")
                
        except Exception as e:
            print(f"Error positioning on secondary monitor: {e}")
            # Fallback positioning
            self.setGeometry(0, 0, 1920, 1080)
    
    def keyPressEvent(self, event):
        """Handle key press events"""
        if event.key() == Qt.Key_Escape:
            # Return to login screen
            self.return_to_login()
        elif event.key() == Qt.Key_F1:
            # Developer mode
            self.show_developer_dialog()
        elif event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            # Handle Enter key for card processing
            if hasattr(self, 'card_buffer') and self.card_buffer:
                self.process_card()
        else:
            # Handle card scanning
            self.handle_card_input(event)
            super().keyPressEvent(event)
    
    def handle_card_input(self, event):
        """Handle card input for scanning"""
        # Collect characters for card ID
        if event.char.isalnum() or event.char in ['\r', '\n']:
            if not hasattr(self, 'card_buffer'):
                self.card_buffer = ""
            
            if event.char in ['\r', '\n']:
                # Process the card
                self.process_card()
            else:
                self.card_buffer += event.char
                print(f"Card buffer: {self.card_buffer}")  # Debug output
                
                # Update instruction to show card ID being entered
                if hasattr(self, 'instruction_label'):
                    self.instruction_label.setText(f"Card ID: {self.card_buffer}")
    
    def process_card(self):
        """Process the scanned card"""
        try:
            if hasattr(self, 'card_buffer') and self.card_buffer:
                card_id = self.card_buffer.strip()
                print(f"Processing card: {card_id}")  # Debug output
                
                # Stop any existing timers to prevent conflicts
                self.stop_all_timers()
                
                # Clear the right panel completely before processing new card
                self.clear_right_panel()
                
                # Check if it's a special pass
                if self.is_special_pass(card_id):
                    print("Special pass detected!")  # Debug output
                    self.show_special_pass_verification(card_id)
                elif self.is_valid_card(card_id):
                    print("Valid card detected")  # Debug output
                    # Handle regular student/teacher cards
                    self.show_regular_card_verification(card_id)
                else:
                    print("Invalid card detected")  # Debug output
                    # Show invalid card message
                    self.show_invalid_card_message(card_id)
                
                # Clear buffer
                self.card_buffer = ""
        except Exception as e:
            print(f"Error processing card: {e}")
            # Reset to main screen on error
            self.reset_to_main_screen()
    
    def is_valid_card(self, card_id):
        """Check if the card ID is valid (student, teacher, etc.)"""
        # Import database manager to check against database
        from database_manager import DatabaseManager
        db_manager = DatabaseManager()
        
        # Check if the card exists in the database
        person = db_manager.find_person(card_id)
        return person is not None and person['role'] in ['STUDENT', 'TEACHER']
    
    def is_special_pass(self, card_id):
        """Check if the card ID is a special pass"""
        # Import database manager to check against database
        from database_manager import DatabaseManager
        db_manager = DatabaseManager()
        
        # Check if the card exists in the database as a special pass
        person = db_manager.find_person(card_id)
        return person is not None and person['role'] == 'SPECIAL'
    
    def show_special_pass_verification(self, card_id):
        """Show special pass verification screen with check-in/check-out logic"""
        try:
            # Import database manager to check status
            from database_manager import DatabaseManager
            db_manager = DatabaseManager()
            
            # Get current check status
            check_status = db_manager.get_special_pass_check_status(card_id)
            
            # Get person data
            person = db_manager.find_person(card_id)
            
            if person:
                if check_status == "CHECKED_OUT":
                    # Need to check in
                    db_manager.record_special_pass_check(card_id, "CHECK_IN")
                    self.show_special_pass_checkin_screen(card_id, person)
                else:
                    # Need to check out
                    db_manager.record_special_pass_check(card_id, "CHECK_OUT")
                    self.show_special_pass_checkout_screen(card_id, person)
            else:
                # Person not found - show invalid card
                self.show_invalid_card_message(card_id)
        except Exception as e:
            print(f"Error in special pass verification: {e}")
            # Show invalid card message on error
            self.show_invalid_card_message(card_id)
    
    def show_special_pass_checkin_screen(self, card_id, person):
        """Show special pass check-in screen"""
        try:
            print(f"Showing special pass check-in screen for: {person['name']}")
            
            # Update top banner to show check-in status
            if hasattr(self, 'top_banner') and self.is_widget_valid(self.top_banner):
                self.top_banner.setStyleSheet("background-color: #90EE90;")  # Light green
                for child in self.top_banner.findChildren(QLabel):
                    if self.is_widget_valid(child):
                        child.setText("Turnstile is Open")
                        child.setStyleSheet("""
                            QLabel {
                                color: black;
                                font-size: 24px;
                                font-weight: bold;
                                background-color: transparent;
                            }
                        """)
            
            # Clear right panel and show check-in information
            if hasattr(self, 'right_panel') and self.is_widget_valid(self.right_panel):
                # Clear existing content using the dedicated method
                self.clear_right_panel()
                
                # Add person information
                name_label = QLabel(person['name'])
                name_label.setAlignment(Qt.AlignCenter)
                name_label.setStyleSheet("""
                    QLabel {
                        color: white;
                        font-size: 24px;
                        font-weight: bold;
                        background-color: transparent;
                    }
                """)
                self.right_panel.layout().addWidget(name_label)
                
                # Add role
                role_label = QLabel(f"({person['role']})")
                role_label.setAlignment(Qt.AlignCenter)
                role_label.setStyleSheet("""
                    QLabel {
                        color: white;
                        font-size: 18px;
                        background-color: transparent;
                    }
                """)
                self.right_panel.layout().addWidget(role_label)
                
                # Add check-in time
                from datetime import datetime
                checkin_time = datetime.now().strftime("%I:%M:%S %p")
                time_label = QLabel(f"Time Check-in: {checkin_time}")
                time_label.setAlignment(Qt.AlignLeft)
                time_label.setStyleSheet("""
                    QLabel {
                        color: white;
                        font-size: 18px;
                        background-color: transparent;
                    }
                """)
                self.right_panel.layout().addWidget(time_label)
                
                # Add date
                checkin_date = datetime.now().strftime("%B %d, %Y")
                date_label = QLabel(f"Date: {checkin_date}")
                date_label.setAlignment(Qt.AlignLeft)
                date_label.setStyleSheet("""
                    QLabel {
                        color: white;
                        font-size: 18px;
                        background-color: transparent;
                    }
                """)
                self.right_panel.layout().addWidget(date_label)
                
                # Add guard information
                guard_label = QLabel("Guard in-charge:")
                guard_label.setAlignment(Qt.AlignLeft)
                guard_label.setStyleSheet("""
                    QLabel {
                        color: white;
                        font-size: 18px;
                        background-color: transparent;
                    }
                """)
                self.right_panel.layout().addWidget(guard_label)
                
                guard_name_label = QLabel("Arvin Jay De Guzman")
                guard_name_label.setAlignment(Qt.AlignLeft)
                guard_name_label.setStyleSheet("""
                    QLabel {
                        color: white;
                        font-size: 18px;
                        background-color: transparent;
                    }
                """)
                self.right_panel.layout().addWidget(guard_name_label)
            
            # Reset after 5 seconds
            self.timer.singleShot(5000, self.reset_to_main_screen)
            
            # Force UI update
            self.update()
            self.repaint()
        except Exception as e:
            print(f"Error showing special pass check-in screen: {e}")
            # Reset to main screen on error
            self.reset_to_main_screen()
    
    def show_special_pass_checkout_screen(self, card_id, person):
        """Show special pass check-out screen"""
        try:
            print(f"Showing special pass check-out screen for: {person['name']}")
            
            # Stop the status check timer to prevent flashing
            if hasattr(self, 'status_check_timer') and self.status_check_timer:
                self.status_check_timer.stop()
            
            # Update top banner to show check-out status
            if hasattr(self, 'top_banner') and self.is_widget_valid(self.top_banner):
                self.top_banner.setStyleSheet("background-color: #FFB6C1;")  # Light pink
                for child in self.top_banner.findChildren(QLabel):
                    if self.is_widget_valid(child):
                        child.setText("Check-out Complete")
                        child.setStyleSheet("""
                            QLabel {
                                color: black;
                                font-size: 24px;
                                font-weight: bold;
                                background-color: transparent;
                            }
                        """)
            
            # Clear right panel and show check-out information
            if hasattr(self, 'right_panel') and self.is_widget_valid(self.right_panel):
                # Clear existing content using the dedicated method
                self.clear_right_panel()
                
                # Add person information
                name_label = QLabel(person['name'])
                name_label.setAlignment(Qt.AlignCenter)
                name_label.setStyleSheet("""
                    QLabel {
                        color: white;
                        font-size: 24px;
                        font-weight: bold;
                        background-color: transparent;
                    }
                """)
                self.right_panel.layout().addWidget(name_label)
                
                # Add role
                role_label = QLabel(f"({person['role']})")
                role_label.setAlignment(Qt.AlignCenter)
                role_label.setStyleSheet("""
                    QLabel {
                        color: white;
                        font-size: 18px;
                        background-color: transparent;
                    }
                """)
                self.right_panel.layout().addWidget(role_label)
                
                # Add check-out time
                from datetime import datetime
                checkout_time = datetime.now().strftime("%I:%M:%S %p")
                time_label = QLabel(f"Time Check-out: {checkout_time}")
                time_label.setAlignment(Qt.AlignLeft)
                time_label.setStyleSheet("""
                    QLabel {
                        color: white;
                        font-size: 18px;
                        background-color: transparent;
                    }
                """)
                self.right_panel.layout().addWidget(time_label)
                
                # Add date
                checkout_date = datetime.now().strftime("%B %d, %Y")
                date_label = QLabel(f"Date: {checkout_date}")
                date_label.setAlignment(Qt.AlignLeft)
                date_label.setStyleSheet("""
                    QLabel {
                        color: white;
                        font-size: 18px;
                        background-color: transparent;
                    }
                """)
                self.right_panel.layout().addWidget(date_label)
                
                # Add guard information
                guard_label = QLabel("Guard in-charge:")
                guard_label.setAlignment(Qt.AlignLeft)
                guard_label.setStyleSheet("""
                    QLabel {
                        color: white;
                        font-size: 18px;
                        background-color: transparent;
                    }
                """)
                self.right_panel.layout().addWidget(guard_label)
                
                guard_name_label = QLabel("Arvin Jay De Guzman")
                guard_name_label.setAlignment(Qt.AlignLeft)
                guard_name_label.setStyleSheet("""
                    QLabel {
                        color: white;
                        font-size: 18px;
                        background-color: transparent;
                    }
                """)
                self.right_panel.layout().addWidget(guard_name_label)
            
            # Reset after 5 seconds
            self.timer.singleShot(5000, self.reset_to_main_screen)
            
            # Force UI update
            self.update()
            self.repaint()
        except Exception as e:
            print(f"Error showing special pass check-out screen: {e}")
            # Reset to main screen on error
            self.reset_to_main_screen()
    
    def check_status_file(self):
        """Check status file for updates from guard screen"""
        try:
            if os.path.exists(self.status_file):
                with open(self.status_file, 'r') as f:
                    lines = f.readlines()
                    if len(lines) >= 4:
                        status = lines[0].strip()
                        print(f"Status file read - Status: {status}, Lines: {len(lines)}")
                        
                        if status == "TURNSTILE_OPEN":
                            special_pass = lines[1].strip()
                            time_checkin = lines[2].strip()
                            guard_name = lines[3].strip()
                            print(f"Processing TURNSTILE_OPEN: {special_pass}, {time_checkin}, {guard_name}")
                            self.show_turnstile_open_status(special_pass, time_checkin, guard_name)
                        elif status == "SPECIAL_PASS_CHECKOUT":
                            special_pass = lines[1].strip()
                            time_checkout = lines[2].strip()
                            guard_name = lines[3].strip()
                            print(f"Processing SPECIAL_PASS_CHECKOUT: {special_pass}, {time_checkout}, {guard_name}")
                            self.show_special_pass_checkout_status(special_pass, time_checkout, guard_name)
                        elif status in ("STUDENT_TEACHER_APPROVED", "STUDENT_TEACHER_INFO") and len(lines) >= 5:
                            person_name = lines[1].strip()
                            person_role = lines[2].strip()
                            time_value = lines[3].strip()
                            guard_name = lines[4].strip()
                            print(f"Processing STUDENT_TEACHER_INFO: {person_name}, {person_role}, {time_value}, {guard_name}")
                            # First show instructions overlay, then the person info
                            self.show_instructions_then_person(person_name, person_role, time_value, guard_name)
                        elif status == "TURNSTILE_CLOSED":
                            print("Processing TURNSTILE_CLOSED - calling reset_to_main_screen")
                            self.reset_to_main_screen()
                            # Clear the status file after processing to prevent re-processing
                            try:
                                with open(self.status_file, "w") as f:
                                    f.write("PROCESSED\n")
                                    f.write("N/A\n")
                                    f.write("N/A\n")
                                    f.write("N/A\n")
                                print("Status file cleared after processing TURNSTILE_CLOSED")
                            except Exception as e:
                                print(f"Error clearing status file: {e}")
                        elif status == "INVALID_ID":
                            print("Processing INVALID_ID")
                            self.show_invalid_id_message()
                        elif status == "DEACTIVATED_PASS":
                            print("Processing DEACTIVATED_PASS")
                            self.show_deactivated_pass_message()
                        elif status == "RESET_TO_DEFAULT":
                            print("Processing RESET_TO_DEFAULT - calling reset_to_main_screen")
                            self.reset_to_main_screen()
                    else:
                        print(f"Status file has insufficient lines: {len(lines)}")
            else:
                print("Status file does not exist")
                            
        except Exception as e:
            print(f"Error reading status file: {e}")
    
    def show_turnstile_open_status(self, special_pass, time_checkin, guard_name):
        """Show turnstile open status with special pass information"""
        # Stop the status check timer to prevent flashing
        if hasattr(self, 'status_check_timer') and self.status_check_timer:
            self.status_check_timer.stop()
            # Restart the timer immediately to continue monitoring for status changes
            self.status_check_timer.start(2000)
        
        # Update top banner to show turnstile open status
        if hasattr(self, 'top_banner'):
            self.top_banner.setStyleSheet("background-color: #90EE90;")  # Light green
            for child in self.top_banner.findChildren(QLabel):
                child.setText("Turnstile is Open")
                child.setWordWrap(True)
                child.setStyleSheet("""
                    QLabel {
                        color: black;
                        font-size: 36px;
                        font-weight: bold;
                        background-color: transparent;
                    }
                """)
        
        # Update instruction label
        if hasattr(self, 'instruction_label'):
            self.instruction_label.setText("Special Pass")
            self.instruction_label.setStyleSheet("""
                QLabel {
                    color: white;
                    font-size: 32px;
                    font-weight: bold;
                    background-color: transparent;
                    margin-top: 40px;
                }
            """)
        
        # Clear existing labels and add new information
        if hasattr(self, 'right_panel'):
            # Remove existing special labels
            for child in self.right_panel.findChildren(QLabel):
                if hasattr(child, 'is_special_label'):
                    child.deleteLater()
            
            # Add reference number
            ref_label = QLabel(f"Ref. {special_pass}")
            ref_label.setAlignment(Qt.AlignCenter)
            ref_label.setStyleSheet("""
                QLabel {
                    color: white;
                    font-size: 24px;
                    background-color: transparent;
                    margin-top: 10px;
                }
            """)
            ref_label.is_special_label = True
            self.right_panel.layout().addWidget(ref_label)
            
            # Add time check-in
            time_label = QLabel("Time Check-in:")
            time_label.setAlignment(Qt.AlignLeft)
            time_label.setStyleSheet("""
                QLabel {
                    color: white;
                    font-size: 18px;
                    background-color: transparent;
                    margin-top: 20px;
                }
            """)
            time_label.is_special_label = True
            self.right_panel.layout().addWidget(time_label)
            
            time_value_label = QLabel(time_checkin)
            time_value_label.setAlignment(Qt.AlignLeft)
            time_value_label.setStyleSheet("""
                QLabel {
                    color: white;
                    font-size: 18px;
                    background-color: transparent;
                }
            """)
            time_value_label.is_special_label = True
            self.right_panel.layout().addWidget(time_value_label)
            
            # Add guard name
            guard_label = QLabel("Guard in-charge:")
            guard_label.setAlignment(Qt.AlignLeft)
            guard_label.setStyleSheet("""
                QLabel {
                    color: white;
                    font-size: 18px;
                    background-color: transparent;
                    margin-top: 20px;
                }
            """)
            guard_label.is_special_label = True
            self.right_panel.layout().addWidget(guard_label)
            
            guard_name_label = QLabel(guard_name)
            guard_name_label.setAlignment(Qt.AlignLeft)
            guard_name_label.setStyleSheet("""
                QLabel {
                    color: white;
                    font-size: 18px;
                    background-color: transparent;
                }
            """)
            guard_name_label.is_special_label = True
            self.right_panel.layout().addWidget(guard_name_label)
    
    def show_special_pass_checkout_status(self, special_pass, time_checkout, guard_name):
        """Show special pass checkout status with checkout information"""
        # Stop the status check timer to prevent flashing
        if hasattr(self, 'status_check_timer') and self.status_check_timer:
            self.status_check_timer.stop()
            # Restart the timer immediately to continue monitoring for status changes
            self.status_check_timer.start(2000)
        
        # Update top banner to show turnstile open status (same as check-in)
        if hasattr(self, 'top_banner'):
            self.top_banner.setStyleSheet("background-color: #90EE90;")  # Light green
            for child in self.top_banner.findChildren(QLabel):
                child.setText("Turnstile is Open")
                child.setWordWrap(True)
                child.setStyleSheet("""
                    QLabel {
                        color: black;
                        font-size: 36px;
                        font-weight: bold;
                        background-color: transparent;
                    }
                """)
        
        # Update instruction label
        if hasattr(self, 'instruction_label'):
            self.instruction_label.setText("Special Pass")
            self.instruction_label.setStyleSheet("""
                QLabel {
                    color: white;
                    font-size: 32px;
                    font-weight: bold;
                    background-color: transparent;
                    margin-top: 40px;
                }
            """)
        
        # Clear existing labels and add new information (same layout as check-in)
        if hasattr(self, 'right_panel'):
            # Remove existing special labels
            for child in self.right_panel.findChildren(QLabel):
                if hasattr(child, 'is_special_label'):
                    child.deleteLater()
            
            # Add reference number
            ref_label = QLabel(f"Ref. {special_pass}")
            ref_label.setAlignment(Qt.AlignCenter)
            ref_label.setStyleSheet("""
                QLabel {
                    color: white;
                    font-size: 24px;
                    background-color: transparent;
                    margin-top: 10px;
                }
            """)
            ref_label.is_special_label = True
            self.right_panel.layout().addWidget(ref_label)
            
            # Add time check-out (same format as check-in)
            time_label = QLabel("Time Check-out:")
            time_label.setAlignment(Qt.AlignLeft)
            time_label.setStyleSheet("""
                QLabel {
                    color: white;
                    font-size: 18px;
                    background-color: transparent;
                    margin-top: 20px;
                }
            """)
            time_label.is_special_label = True
            self.right_panel.layout().addWidget(time_label)
            
            time_value_label = QLabel(time_checkout)
            time_value_label.setAlignment(Qt.AlignLeft)
            time_value_label.setStyleSheet("""
                QLabel {
                    color: white;
                    font-size: 18px;
                    background-color: transparent;
                }
            """)
            time_value_label.is_special_label = True
            self.right_panel.layout().addWidget(time_value_label)
            
            # Add guard name
            guard_label = QLabel("Guard in-charge:")
            guard_label.setAlignment(Qt.AlignLeft)
            guard_label.setStyleSheet("""
                QLabel {
                    color: white;
                    font-size: 18px;
                    background-color: transparent;
                    margin-top: 20px;
                }
            """)
            guard_label.is_special_label = True
            self.right_panel.layout().addWidget(guard_label)
            
            guard_name_label = QLabel(guard_name)
            guard_name_label.setAlignment(Qt.AlignLeft)
            guard_name_label.setStyleSheet("""
                QLabel {
                    color: white;
                    font-size: 18px;
                    background-color: transparent;
                }
            """)
            guard_name_label.is_special_label = True
            self.right_panel.layout().addWidget(guard_name_label)
        
        # Reset after 5 seconds
        self.timer.singleShot(5000, self.reset_to_main_screen)
        
        # Force UI update
        self.update()
        self.repaint()
    
    def show_student_teacher_info(self, person_name, person_role, time_value, guard_name):
        """Show student/teacher info on the right panel, then reset after 5s."""
        # Stop the status check timer to prevent flashing
        if hasattr(self, 'status_check_timer') and self.status_check_timer:
            self.status_check_timer.stop()
            # Restart the timer immediately to continue monitoring for status changes
            self.status_check_timer.start(2000)
        
        # Update top banner
        if hasattr(self, 'top_banner'):
            self.top_banner.setStyleSheet("background-color: #90EE90;")
            for child in self.top_banner.findChildren(QLabel):
                child.setText("Turnstile is Open")
                child.setWordWrap(True)
                child.setStyleSheet("""
                    QLabel {
                        color: black;
                        font-size: 36px;
                        font-weight: bold;
                        background-color: transparent;
                    }
                """)
        
        # Populate right panel with profile picture and info
        if hasattr(self, 'right_panel'):
            # Clear existing widgets
            for child in self.right_panel.findChildren(QLabel):
                child.deleteLater()
            
            # Add STI BALAGTAS logo at the top
            try:
                logo_path = os.path.join("image-elements", "STI Balagtas Logo.png")
                if os.path.exists(logo_path):
                    logo_icon = QLabel()
                    pixmap = QPixmap(logo_path)
                    # Scale the logo to a reasonable size
                    scaled_pixmap = pixmap.scaled(120, 90, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    logo_icon.setPixmap(scaled_pixmap)
                    logo_icon.setAlignment(Qt.AlignCenter)
                    logo_icon.setStyleSheet("background-color: transparent;")
                    self.right_panel.layout().addWidget(logo_icon)
                    
                    # Add spacing after logo
                    logo_spacer = QLabel("")
                    logo_spacer.setFixedHeight(20)
                    self.right_panel.layout().addWidget(logo_spacer)
            except Exception as e:
                print(f"Error loading STI logo: {e}")
            
            # Add profile picture
            profile_image_path = None
            if person_role == "STUDENT":
                # Try to find student image by name or use generic
                profile_image_path = os.path.join("image-students", f"{person_name.replace(' ', '_')}.jpeg")
                if not os.path.exists(profile_image_path):
                    # Try with student number if available
                    profile_image_path = os.path.join("image-students", "02000226226.jpeg")
            elif person_role == "TEACHER":
                # Try to find teacher image by name or use generic
                profile_image_path = os.path.join("image-teachers", f"{person_name.replace(' ', '_')}.jpeg")
                if not os.path.exists(profile_image_path):
                    # Try with teacher number if available
                    profile_image_path = os.path.join("image-teachers", "0095520658.jpeg")
            
            # If no specific image found, use generic
            if not profile_image_path or not os.path.exists(profile_image_path):
                profile_image_path = os.path.join("image-elements", "Generic User Image.jpg")
            
            # Load and display profile picture
            if os.path.exists(profile_image_path):
                profile_icon = QLabel()
                pixmap = QPixmap(profile_image_path)
                # Scale the profile image to a reasonable size
                scaled_pixmap = pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                
                # Create rounded corners on the image
                rounded_pixmap = QPixmap(scaled_pixmap.size())
                rounded_pixmap.fill(Qt.transparent)
                
                painter = QPainter(rounded_pixmap)
                painter.setRenderHint(QPainter.Antialiasing)
                painter.setRenderHint(QPainter.SmoothPixmapTransform)
                
                # Create circular mask
                painter.setBrush(QBrush(scaled_pixmap))
                painter.setPen(Qt.NoPen)
                painter.drawEllipse(0, 0, scaled_pixmap.width(), scaled_pixmap.height())
                painter.end()
                
                profile_icon.setPixmap(rounded_pixmap)
                profile_icon.setAlignment(Qt.AlignCenter)
                profile_icon.setStyleSheet("background-color: transparent;")
                self.right_panel.layout().addWidget(profile_icon)
            
            # Add spacing
            spacer1 = QLabel("")
            spacer1.setFixedHeight(20)
            self.right_panel.layout().addWidget(spacer1)
            
            # Add name
            name_label = QLabel(person_name)
            name_label.setAlignment(Qt.AlignCenter)
            name_label.setStyleSheet("""
                QLabel { 
                    color: white; 
                    font-size: 28px; 
                    font-weight: bold; 
                    background-color: transparent; 
                    margin: 10px;
                }
            """)
            self.right_panel.layout().addWidget(name_label)
            
            # Add role
            role_label = QLabel(f"({person_role})")
            role_label.setAlignment(Qt.AlignCenter)
            role_label.setStyleSheet("""
                QLabel { 
                    color: white; 
                    font-size: 20px; 
                    background-color: transparent; 
                    margin: 5px;
                }
            """)
            self.right_panel.layout().addWidget(role_label)
            
            # Add spacing
            spacer2 = QLabel("")
            spacer2.setFixedHeight(20)
            self.right_panel.layout().addWidget(spacer2)
            
            # Add time check-in
            time_label = QLabel(f"Time Check-in: {time_value}")
            time_label.setAlignment(Qt.AlignLeft)
            time_label.setStyleSheet("""
                QLabel { 
                    color: white; 
                    font-size: 18px; 
                    background-color: transparent; 
                    margin: 5px;
                }
            """)
            self.right_panel.layout().addWidget(time_label)
            
            # Add date
            date_label = QLabel(f"Date: {datetime.now().strftime('%B %d, %Y')}")
            date_label.setAlignment(Qt.AlignLeft)
            date_label.setStyleSheet("""
                QLabel { 
                    color: white; 
                    font-size: 18px; 
                    background-color: transparent; 
                    margin: 5px;
                }
            """)
            self.right_panel.layout().addWidget(date_label)
            
            # Add spacing
            spacer3 = QLabel("")
            spacer3.setFixedHeight(20)
            self.right_panel.layout().addWidget(spacer3)
            
            # Add guard information
            guard_label = QLabel("Guard in-charge:")
            guard_label.setAlignment(Qt.AlignLeft)
            guard_label.setStyleSheet("""
                QLabel { 
                    color: white; 
                    font-size: 18px; 
                    font-weight: bold;
                    background-color: transparent; 
                    margin: 5px;
                }
            """)
            self.right_panel.layout().addWidget(guard_label)
            
            guard_name_label = QLabel(guard_name)
            guard_name_label.setAlignment(Qt.AlignLeft)
            guard_name_label.setStyleSheet("""
                QLabel { 
                    color: white; 
                    font-size: 18px; 
                    background-color: transparent; 
                    margin: 5px;
                }
            """)
            self.right_panel.layout().addWidget(guard_name_label)
        # Stop any existing singleShot timer before starting a new one
        if hasattr(self, 'reset_timer') and self.reset_timer:
            self.reset_timer.stop()
        
        # Reset after 5 seconds
        self.reset_timer = QTimer()
        self.reset_timer.setSingleShot(True)
        self.reset_timer.timeout.connect(self.reset_to_main_screen)
        self.reset_timer.start(5000)
        print(f"Reset timer started for {person_name} - will reset in 5 seconds")
        
        self.update()
        self.repaint()

    def show_invalid_id_message(self):
        """Show invalid ID message on main screen"""
        # Update top banner to show error status
        if hasattr(self, 'top_banner'):
            self.top_banner.setStyleSheet("background-color: #FF6B6B;")  # Light red
            for child in self.top_banner.findChildren(QLabel):
                child.setText("Invalid ID Scanned")
                child.setWordWrap(True)
                child.setStyleSheet("""
                    QLabel {
                        color: white;
                        font-size: 36px;
                        font-weight: bold;
                        background-color: transparent;
                    }
                """)
        
        # Update instruction label
        if hasattr(self, 'instruction_label'):
            self.instruction_label.setText("Invalid Card")
            self.instruction_label.setStyleSheet("""
                QLabel {
                    color: white;
                    font-size: 32px;
                    font-weight: bold;
                    background-color: transparent;
                    margin-top: 40px;
                }
            """)
    
    def show_deactivated_pass_message(self):
        """Show deactivated pass message on main screen"""
        # Update top banner to show error status
        if hasattr(self, 'top_banner'):
            self.top_banner.setStyleSheet("background-color: #FF6B6B;")  # Light red
            for child in self.top_banner.findChildren(QLabel):
                child.setText("Deactivated Pass Scanned")
                child.setWordWrap(True)
                child.setStyleSheet("""
                    QLabel {
                        color: white;
                        font-size: 36px;
                        font-weight: bold;
                        background-color: transparent;
                    }
                """)
        
        # Update instruction label
        if hasattr(self, 'instruction_label'):
            self.instruction_label.setText("Deactivated Pass")
            self.instruction_label.setStyleSheet("""
                QLabel {
                    color: white;
                    font-size: 32px;
                    font-weight: bold;
                    background-color: transparent;
                }
            """)
    
    def test_special_pass(self):
        """Test method to simulate special pass verification"""
        print("Testing special pass verification...")
        self.show_special_pass_verification("9876543210")
    
    def test_invalid_card(self):
        """Test method to simulate invalid card"""
        print("Testing invalid card message...")
        self.show_invalid_card_message("INVALID123")
    
    def show_regular_card_verification(self, card_id):
        """Show regular card verification screen with check-in/check-out logic"""
        try:
            # Import database manager to check status
            from database_manager import DatabaseManager
            db_manager = DatabaseManager()
            
            # Get current check status
            check_status = db_manager.get_student_teacher_check_status(card_id)
            
            # Get person data
            person = db_manager.find_person(card_id)
            
            if person:
                if check_status == "CHECKED_OUT":
                    # Need to check in
                    db_manager.record_student_teacher_check(card_id, "CHECK_IN")
                    self.show_student_teacher_checkin_screen(card_id, person)
                else:
                    # Need to check out
                    db_manager.record_student_teacher_check(card_id, "CHECK_OUT")
                    self.show_student_teacher_checkout_screen(card_id, person)
            else:
                # Person not found - show invalid card
                self.show_invalid_card_message(card_id)
        except Exception as e:
            print(f"Error in regular card verification: {e}")
            # Show invalid card message on error
            self.show_invalid_card_message(card_id)
    
    def show_student_teacher_checkin_screen(self, card_id, person):
        """Show student/teacher check-in screen"""
        try:
            print(f"Showing check-in screen for: {person['name']}")
            
            # Update top banner to show check-in status
            if hasattr(self, 'top_banner'):
                self.top_banner.setStyleSheet("background-color: #90EE90;")  # Light green
                for child in self.top_banner.findChildren(QLabel):
                    child.setText("Turnstile is Open")
                    child.setStyleSheet("""
                        QLabel {
                            color: black;
                            font-size: 24px;
                            font-weight: bold;
                            background-color: transparent;
                        }
                    """)
            
            # Clear right panel and show check-in information
            if hasattr(self, 'right_panel'):
                # Clear existing content using the dedicated method
                self.clear_right_panel()
                
                # Add person information
                name_label = QLabel(person['name'])
                name_label.setAlignment(Qt.AlignCenter)
                name_label.setStyleSheet("""
                    QLabel {
                        color: white;
                        font-size: 24px;
                        font-weight: bold;
                        background-color: transparent;
                    }
                """)
                self.right_panel.layout().addWidget(name_label)
                
                # Add role
                role_label = QLabel(f"({person['role']})")
                role_label.setAlignment(Qt.AlignCenter)
                role_label.setStyleSheet("""
                    QLabel {
                        color: white;
                        font-size: 18px;
                        background-color: transparent;
                    }
                """)
                self.right_panel.layout().addWidget(role_label)
                
                # Add check-in time
                from datetime import datetime
                checkin_time = datetime.now().strftime("%I:%M:%S %p")
                time_label = QLabel(f"Time Check-in: {checkin_time}")
                time_label.setAlignment(Qt.AlignLeft)
                time_label.setStyleSheet("""
                    QLabel {
                        color: white;
                        font-size: 18px;
                        background-color: transparent;
                    }
                """)
                self.right_panel.layout().addWidget(time_label)
                
                # Add date
                checkin_date = datetime.now().strftime("%B %d, %Y")
                date_label = QLabel(f"Date: {checkin_date}")
                date_label.setAlignment(Qt.AlignLeft)
                date_label.setStyleSheet("""
                    QLabel {
                        color: white;
                        font-size: 18px;
                        background-color: transparent;
                    }
                """)
                self.right_panel.layout().addWidget(date_label)
                
                # Add guard information
                guard_label = QLabel("Guard in-charge:")
                guard_label.setAlignment(Qt.AlignLeft)
                guard_label.setStyleSheet("""
                    QLabel {
                        color: white;
                        font-size: 18px;
                        background-color: transparent;
                    }
                """)
                self.right_panel.layout().addWidget(guard_label)
                
                guard_name_label = QLabel("Arvin Jay De Guzman")
                guard_name_label.setAlignment(Qt.AlignLeft)
                guard_name_label.setStyleSheet("""
                    QLabel {
                        color: white;
                        font-size: 18px;
                        background-color: transparent;
                    }
                """)
                self.right_panel.layout().addWidget(guard_name_label)
            
            # Reset after 5 seconds
            self.timer.singleShot(5000, self.reset_to_main_screen)
            
            # Force UI update
            self.update()
            self.repaint()
        except Exception as e:
            print(f"Error showing check-in screen: {e}")
            # Reset to main screen on error
            self.reset_to_main_screen()
    
    def show_student_teacher_checkout_screen(self, card_id, person):
        """Show student/teacher check-out screen"""
        try:
            print(f"Showing check-out screen for: {person['name']}")
            
            # Stop the status check timer to prevent flashing
            if hasattr(self, 'status_check_timer') and self.status_check_timer:
                self.status_check_timer.stop()
            
            # Update top banner to show check-out status
            if hasattr(self, 'top_banner'):
                self.top_banner.setStyleSheet("background-color: #FFB6C1;")  # Light pink
                for child in self.top_banner.findChildren(QLabel):
                    child.setText("Check-out Complete")
                    child.setStyleSheet("""
                        QLabel {
                            color: black;
                            font-size: 24px;
                            font-weight: bold;
                            background-color: transparent;
                        }
                    """)
            
            # Clear right panel and show check-out information
            if hasattr(self, 'right_panel'):
                # Clear existing content using the dedicated method
                self.clear_right_panel()
                
                # Add person information
                name_label = QLabel(person['name'])
                name_label.setAlignment(Qt.AlignCenter)
                name_label.setStyleSheet("""
                    QLabel {
                        color: white;
                        font-size: 24px;
                        font-weight: bold;
                        background-color: transparent;
                    }
                """)
                self.right_panel.layout().addWidget(name_label)
                
                # Add role
                role_label = QLabel(f"({person['role']})")
                role_label.setAlignment(Qt.AlignCenter)
                role_label.setStyleSheet("""
                    QLabel {
                        color: white;
                        font-size: 18px;
                        background-color: transparent;
                    }
                """)
                self.right_panel.layout().addWidget(role_label)
                
                # Add check-out time
                from datetime import datetime
                checkout_time = datetime.now().strftime("%I:%M:%S %p")
                time_label = QLabel(f"Time Check-out: {checkout_time}")
                time_label.setAlignment(Qt.AlignLeft)
                time_label.setStyleSheet("""
                    QLabel {
                        color: white;
                        font-size: 18px;
                        background-color: transparent;
                    }
                """)
                self.right_panel.layout().addWidget(time_label)
                
                # Add date
                checkout_date = datetime.now().strftime("%B %d, %Y")
                date_label = QLabel(f"Date: {checkout_date}")
                date_label.setAlignment(Qt.AlignLeft)
                date_label.setStyleSheet("""
                    QLabel {
                        color: white;
                        font-size: 18px;
                        background-color: transparent;
                    }
                """)
                self.right_panel.layout().addWidget(date_label)
                
                # Add guard information
                guard_label = QLabel("Guard in-charge:")
                guard_label.setAlignment(Qt.AlignLeft)
                guard_label.setStyleSheet("""
                    QLabel {
                        color: white;
                        font-size: 18px;
                        background-color: transparent;
                    }
                """)
                self.right_panel.layout().addWidget(guard_label)
                
                guard_name_label = QLabel("Arvin Jay De Guzman")
                guard_name_label.setAlignment(Qt.AlignLeft)
                guard_name_label.setStyleSheet("""
                    QLabel {
                        color: white;
                        font-size: 18px;
                        background-color: transparent;
                    }
                """)
                self.right_panel.layout().addWidget(guard_name_label)
            
            # Reset after 5 seconds
            self.timer.singleShot(5000, self.reset_to_main_screen)
            
            # Force UI update
            self.update()
            self.repaint()
        except Exception as e:
            print(f"Error showing check-out screen: {e}")
            # Reset to main screen on error
            self.reset_to_main_screen()
    
    def show_invalid_card_message(self, card_id):
        """Show invalid card message on main screen"""
        try:
            print(f"Showing invalid card message for: {card_id}")
            
            # Update top banner to show error status
            if hasattr(self, 'top_banner'):
                print("Updating top banner for invalid card...")
                self.top_banner.setStyleSheet("background-color: #FF6B6B;")  # Light red
                for child in self.top_banner.findChildren(QLabel):
                    child.setText("Invalid ID Scanned")
                    child.setStyleSheet("""
                        QLabel {
                            color: white;
                            font-size: 36px;
                            font-weight: bold;
                            background-color: transparent;
                        }
                    """)
            else:
                print("Top banner not found!")
            
            # Update instruction label
            if hasattr(self, 'instruction_label'):
                print("Updating instruction label for invalid card...")
                self.instruction_label.setText("Invalid Card")
                self.instruction_label.setStyleSheet("""
                    QLabel {
                        color: white;
                        font-size: 32px;
                        font-weight: bold;
                        background-color: transparent;
                        margin-top: 40px;
                    }
                """)
            else:
                print("Instruction label not found!")
            
            # Reset to main screen after 3 seconds
            self.timer.singleShot(3000, self.reset_to_main_screen)
            
            # Force UI update
            self.update()
            self.repaint()
        except Exception as e:
            print(f"Error showing invalid card message: {e}")
            # Reset to main screen on error
            self.reset_to_main_screen()
    
    def reset_to_main_screen(self):
        """Reset the screen to main interface"""
        try:
            print("reset_to_main_screen called - resetting to awaiting ID scan")
            # Stop all timers first
            self.stop_all_timers()
            
            # Reset top banner
            if hasattr(self, 'top_banner') and self.is_widget_valid(self.top_banner):
                try:
                    self.top_banner.setStyleSheet("background-color: #DAA520;")  # Mustard yellow
                    for child in self.top_banner.findChildren(QLabel):
                        if self.is_widget_valid(child):
                            child.setText("Awaiting ID card scan.")
                            child.setStyleSheet("""
                                QLabel {
                                    color: white;
                                    font-size: 36px;
                                    font-weight: bold;
                                    background-color: transparent;
                                }
                            """)
                except RuntimeError:
                    print("Top banner has been deleted, skipping reset")
            
            # Reset instruction label
            if hasattr(self, 'instruction_label') and self.is_widget_valid(self.instruction_label):
                try:
                    self.instruction_label.setText("Please tap your ID\nto the Card Reader")
                    self.instruction_label.setStyleSheet("""
                        QLabel {
                            color: white;
                            font-size: 32px;
                            font-weight: bold;
                            background-color: transparent;
                            margin-top: 40px;
                        }
                    """)
                except RuntimeError:
                    print("Instruction label has been deleted, skipping reset")
            
            # Clear the right panel completely and restore default state
            if hasattr(self, 'right_panel') and self.is_widget_valid(self.right_panel):
                try:
                    # Remove ALL labels from the right panel
                    for child in self.right_panel.findChildren(QLabel):
                        if self.is_widget_valid(child):
                            child.deleteLater()
                    
                    # Force immediate cleanup
                    self.right_panel.update()
                    self.right_panel.repaint()
                    
                    # Restore the default right panel content
                    self.restore_default_right_panel()
                except RuntimeError:
                    print("Right panel has been deleted, skipping cleanup")
            
            # Clear card buffer
            if hasattr(self, 'card_buffer'):
                self.card_buffer = ""
                
            # Force UI update
            self.update()
            self.repaint()
            
            # Restart the status check timer
            if hasattr(self, 'status_check_timer'):
                self.status_check_timer.start(2000)  # Check every 2 seconds
            
        except Exception as e:
            print(f"Error resetting to main screen: {e}")
            # Try to at least reset the instruction text
            try:
                if hasattr(self, 'instruction_label') and self.is_widget_valid(self.instruction_label):
                    try:
                        self.instruction_label.setText("Please tap your ID\nto the Card Reader")
                    except RuntimeError:
                        print("Instruction label has been deleted, cannot reset")
            except Exception as e2:
                print(f"Error in fallback instruction reset: {e2}")
        

    
    def return_to_login(self):
        """Return to the login application"""
        try:
            # Get the current directory and path to ai_niform_login.py
            current_dir = os.path.dirname(os.path.abspath(__file__))
            login_path = os.path.join(current_dir, "ai_niform_login.py")
            
            # Launch the login application
            subprocess.Popen([sys.executable, login_path])
            
            # Close this application
            self.close()
            
        except Exception as e:
            print(f"Error returning to login: {e}")
            # Just close this application if there's an error
            self.close()
    
    def setup_ui(self, layout):
        # Top Banner
        top_banner = QFrame()
        top_banner.setFixedHeight(120)
        top_banner.setStyleSheet("background-color: #DAA520;")  # Mustard yellow
        
        # Main welcome label
        welcome_label = QLabel("Awaiting ID card scan.")
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_label.setWordWrap(True)
        welcome_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 36px;
                font-weight: bold;
                background-color: transparent;
            }
        """)
        
        top_layout = QVBoxLayout(top_banner)
        top_layout.addWidget(welcome_label)
        layout.addWidget(top_banner)
        
        # Store reference to top banner for later use
        self.top_banner = top_banner
        
        # Main Content Area
        main_content = QFrame()
        main_layout = QHBoxLayout(main_content)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Left Panel (White Background with Logo)
        left_panel = QFrame()
        left_panel.setStyleSheet("background-color: white;")
        left_layout = QVBoxLayout(left_panel)
        left_layout.setAlignment(Qt.AlignCenter)
        
        # Load and display STI Logo
        logo_path = os.path.join("image-elements", "STI Balagtas Logo.png")
        if os.path.exists(logo_path):
            logo_label = QLabel()
            pixmap = QPixmap(logo_path)
            # Scale the logo to a reasonable size for 1920x1080
            scaled_pixmap = pixmap.scaled(400, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo_label.setPixmap(scaled_pixmap)
            logo_label.setAlignment(Qt.AlignCenter)
            left_layout.addWidget(logo_label)
        else:
            # Fallback if logo not found
            fallback_label = QLabel("STI Balagtas Logo")
            fallback_label.setAlignment(Qt.AlignCenter)
            fallback_label.setStyleSheet("""
                QLabel {
                    font-size: 24px;
                    font-weight: bold;
                    color: #0066CC;
                    background-color: #FFD700;
                    padding: 20px;
                    border-radius: 3px;
                }
            """)
            left_layout.addWidget(fallback_label)
        
        main_layout.addWidget(left_panel)
        
        # Right Panel (Dark Blue Background)
        right_panel = QFrame()
        right_panel.setStyleSheet("background-color: #1E3A8A;")
        right_layout = QVBoxLayout(right_panel)
        right_layout.setAlignment(Qt.AlignCenter)
        
        # Load and display Generic User Image
        user_image_path = os.path.join("image-elements", "Generic User Image.jpg")
        if os.path.exists(user_image_path):
            user_icon = QLabel()
            pixmap = QPixmap(user_image_path)
            # Scale the user image to a reasonable size for 1920x1080
            scaled_pixmap = pixmap.scaled(180, 180, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            
            # Create rounded corners on the image itself
            rounded_pixmap = QPixmap(scaled_pixmap.size())
            rounded_pixmap.fill(Qt.transparent)
            
            painter = QPainter(rounded_pixmap)
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setRenderHint(QPainter.SmoothPixmapTransform)
            
            # Create rounded rectangle path
            path = QPainterPath()
            path.addRoundedRect(0, 0, scaled_pixmap.width(), scaled_pixmap.height(), 3, 3)
            painter.setClipPath(path)
            
            # Draw the image
            painter.drawPixmap(0, 0, scaled_pixmap)
            painter.end()
            
            user_icon.setPixmap(rounded_pixmap)
            user_icon.setAlignment(Qt.AlignCenter)
            user_icon.setStyleSheet("""
                QLabel {
                    background-color: transparent;
                }
            """)
        else:
            # Fallback if image not found
            user_icon = QLabel("👤")
            user_icon.setFixedSize(180, 180)
            user_icon.setStyleSheet("""
                QLabel {
                    background-color: #D3D3D3;
                    border-radius: 3px;
                    border: 2px solid white;
                    font-size: 80px;
                    color: #1E3A8A;
                }
            """)
            user_icon.setAlignment(Qt.AlignCenter)
        
        right_layout.addWidget(user_icon)
        
        # Instruction text
        self.instruction_label = QLabel("Please tap your ID\nto the Card Reader")
        self.instruction_label.setAlignment(Qt.AlignCenter)
        self.instruction_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 32px;
                font-weight: bold;
                background-color: transparent;
                margin-top: 40px;
            }
        """)
        right_layout.addWidget(self.instruction_label)
        

        
        main_layout.addWidget(right_panel)
        layout.addWidget(main_content)
        
        # Store reference to right panel for later use
        self.right_panel = right_panel
        
        # Bottom Bar
        bottom_bar = QFrame()
        bottom_bar.setFixedHeight(100)
        bottom_layout = QHBoxLayout(bottom_bar)
        bottom_layout.setSpacing(0)
        bottom_layout.setContentsMargins(0, 0, 0, 0)
        
        # Date section (Light Blue)
        date_frame = QFrame()
        date_frame.setStyleSheet("background-color: #87CEEB;")
        date_layout = QVBoxLayout(date_frame)
        
        self.date_label = QLabel()
        self.date_label.setAlignment(Qt.AlignCenter)
        self.date_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                font-weight: bold;
                background-color: transparent;
            }
        """)
        date_layout.addWidget(self.date_label)
        bottom_layout.addWidget(date_frame)
        
        # Time section (Darker Navy Blue)
        time_frame = QFrame()
        time_frame.setStyleSheet("background-color: #021C37;")
        time_layout = QVBoxLayout(time_frame)
        
        self.time_label = QLabel()
        self.time_label.setAlignment(Qt.AlignCenter)
        self.time_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                font-weight: bold;
                background-color: transparent;
            }
        """)
        time_layout.addWidget(self.time_label)
        bottom_layout.addWidget(time_frame)
        
        layout.addWidget(bottom_bar)
    
    def setup_timer(self):
        """Set up timer to update date and time"""
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)  # Update every second
        self.update_time()  # Initial update
        
        # Set up timer to check status file for updates from guard screen
        self.status_check_timer = QTimer()
        self.status_check_timer.timeout.connect(self.check_status_file)
        self.status_check_timer.start(2000)  # Check every 2 seconds
    
    def update_time(self):
        """Update the date and time display"""
        now = datetime.now()
        date_str = now.strftime("%B %d, %Y")
        time_str = now.strftime("%I:%M:%S %p")
        
        self.date_label.setText(date_str)
        self.time_label.setText(time_str)
    
    def keyPressEvent(self, event):
        """Handle key presses"""
        if event.key() == Qt.Key_Escape:
            self.showNormal()  # Exit fullscreen
        elif event.key() == Qt.Key_F11:
            if self.isFullScreen():
                self.showNormal()
            else:
                self.showFullScreen()
        else:
            # Handle developer mode input
            if event.text().isprintable():
                self.developer_input += event.text().lower()
                
                # Check if "developer" is typed
                if "developer" in self.developer_input:
                    self.show_developer_mode()
                    self.developer_input = ""
                
                # Reset input after 3 seconds of inactivity
                if self.developer_timeout:
                    self.developer_timeout.stop()
                self.developer_timeout = QTimer()
                self.developer_timeout.timeout.connect(lambda: setattr(self, 'developer_input', ''))
                self.developer_timeout.start(3000)  # 3 seconds
            
            super().keyPressEvent(event)
    
    def show_developer_mode(self):
        """Show the developer mode dialog"""
        dialog = DeveloperModeDialog(self)
        dialog.exec_()
    
    def show_status_message(self, status):
        """Show status message on the main screen for 3 seconds"""
        # Stop any existing timer
        if self.status_timer:
            self.status_timer.stop()
        
        # Update the instruction text based on status
        if status == "Invalid ID":
            self.instruction_label.setText("Invalid ID\nScanned")
            # Set up timer to revert back to original text after 3 seconds
            self.status_timer = QTimer()
            self.status_timer.timeout.connect(self.reset_instruction_text)
            self.status_timer.start(3000)  # 3 seconds
        elif status == "Deactivated Pass":
            self.instruction_label.setText("Deactivated Pass\nhas been scanned.")
            # Set up timer to revert back to original text after 3 seconds
            self.status_timer = QTimer()
            self.status_timer.timeout.connect(self.reset_instruction_text)
            self.status_timer.start(3000)  # 3 seconds
        elif status == "Valid Pass":
            # Start the scanning sequence
            self.start_scanning_sequence()
        elif status == "Valid Special Pass":
            # Show the special pass success screen directly
            self.show_special_pass_success_screen()
        elif status == "Special Pass":
            # Show the special pass check-out screen directly
            self.show_special_pass_checkout_screen()
        elif status == "Student / Teacher / Staff":
            # Show the student/teacher/staff check-out screen directly
            self.show_student_staff_checkout_screen()
        elif status == "Accept Entry":
            self.instruction_label.setText("Entry Accepted\nby Manual Verification.")
            # Set up timer to revert back to original text after 3 seconds
            self.status_timer = QTimer()
            self.status_timer.timeout.connect(self.reset_instruction_text)
            self.status_timer.start(3000)  # 3 seconds
        elif status == "Deny Entry":
            self.instruction_label.setText("Entry Denied\nby Manual Verification.")
            # Set up timer to revert back to original text after 3 seconds
            self.status_timer = QTimer()
            self.status_timer.timeout.connect(self.reset_instruction_text)
            self.status_timer.start(3000)  # 3 seconds
    
    def reset_instruction_text(self):
        """Reset instruction text back to original"""
        try:
            # Check if instruction_label still exists and is valid
            if hasattr(self, 'instruction_label') and self.is_widget_valid(self.instruction_label):
                try:
                    self.instruction_label.setText(self.original_instruction_text)
                except RuntimeError:
                    # QLabel has been deleted, skip this operation
                    print("Instruction label has been deleted, skipping reset")
                    return
            
            if hasattr(self, 'status_timer') and self.status_timer:
                self.status_timer.stop()
            
            # Also reset the top banner to "Awaiting ID card scan"
            if hasattr(self, 'top_banner') and self.is_widget_valid(self.top_banner):
                try:
                    self.top_banner.setStyleSheet("background-color: #DAA520;")  # Mustard yellow
                    for child in self.top_banner.findChildren(QLabel):
                        if self.is_widget_valid(child):
                            child.setText("Awaiting ID card scan.")
                            child.setStyleSheet("""
                                QLabel {
                                    color: white;
                                    font-size: 36px;
                                    font-weight: bold;
                                    background-color: transparent;
                                }
                            """)
                except RuntimeError:
                    # Top banner has been deleted, skip this operation
                    print("Top banner has been deleted, skipping reset")
        except Exception as e:
            print(f"Error in reset_instruction_text: {e}")
    
    def is_widget_valid(self, widget):
        """Check if a QWidget still exists and is valid"""
        try:
            if widget is None:
                return False
            # Try to access a property to see if the widget still exists
            widget.objectName()
            return True
        except RuntimeError:
            return False
    
    def clear_right_panel(self):
        """Clear all content from the right panel"""
        try:
            if hasattr(self, 'right_panel') and self.is_widget_valid(self.right_panel):
                # Remove all child widgets from the right panel
                children = self.right_panel.findChildren(QLabel)
                for child in children:
                    if self.is_widget_valid(child):
                        child.hide()  # Hide first
                        child.deleteLater()  # Then delete
                
                # Force immediate cleanup and processing
                self.right_panel.update()
                self.right_panel.repaint()
                
                # Process any pending events to ensure cleanup happens immediately
                from PyQt5.QtWidgets import QApplication
                QApplication.processEvents()
                
                print("Right panel cleared successfully")
        except Exception as e:
            print(f"Error clearing right panel: {e}")
    
    def restore_default_right_panel(self):
        """Restore the default right panel content (Awaiting ID card scan)"""
        try:
            if hasattr(self, 'right_panel') and self.is_widget_valid(self.right_panel):
                # 1) User icon (same style as initial setup)
                user_image_path = os.path.join("image-elements", "Generic User Image.jpg")
                if os.path.exists(user_image_path):
                    user_icon = QLabel()
                    pixmap = QPixmap(user_image_path)
                    # Scale the user image to a reasonable size for 1920x1080
                    scaled_pixmap = pixmap.scaled(180, 180, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    
                    # Create rounded corners on the image itself
                    rounded_pixmap = QPixmap(scaled_pixmap.size())
                    rounded_pixmap.fill(Qt.transparent)
                    
                    painter = QPainter(rounded_pixmap)
                    painter.setRenderHint(QPainter.Antialiasing)
                    painter.setRenderHint(QPainter.SmoothPixmapTransform)
                    
                    # Create rounded rectangle path
                    path = QPainterPath()
                    path.addRoundedRect(0, 0, scaled_pixmap.width(), scaled_pixmap.height(), 3, 3)
                    painter.setClipPath(path)
                    
                    # Draw the image
                    painter.drawPixmap(0, 0, scaled_pixmap)
                    painter.end()
                    
                    user_icon.setPixmap(rounded_pixmap)
                    user_icon.setAlignment(Qt.AlignCenter)
                    user_icon.setStyleSheet("""
                        QLabel {
                            background-color: transparent;
                        }
                    """)
                else:
                    # Fallback if image not found
                    user_icon = QLabel("👤")
                    user_icon.setFixedSize(180, 180)
                    user_icon.setStyleSheet("""
                        QLabel {
                            background-color: #D3D3D3;
                            border-radius: 3px;
                            border: 2px solid white;
                            font-size: 80px;
                            color: #1E3A8A;
                        }
                    """)
                    user_icon.setAlignment(Qt.AlignCenter)
                
                self.right_panel.layout().addWidget(user_icon)
                
                # 2) Large instruction text (same as initial setup)
                self.instruction_label = QLabel("Please tap your ID\nto the Card Reader")
                self.instruction_label.setAlignment(Qt.AlignCenter)
                self.instruction_label.setStyleSheet("""
                    QLabel {
                        color: white;
                        font-size: 32px;
                        font-weight: bold;
                        background-color: transparent;
                        margin-top: 40px;
                    }
                """)
                self.right_panel.layout().addWidget(self.instruction_label)
                
                print("Default right panel content restored")
        except Exception as e:
            print(f"Error restoring default right panel: {e}")
    
    def stop_all_timers(self):
        """Stop all active timers to prevent conflicts"""
        try:
            if hasattr(self, 'status_timer') and self.status_timer:
                self.status_timer.stop()
                self.status_timer = None
            if hasattr(self, 'developer_timeout') and self.developer_timeout:
                self.developer_timeout.stop()
                self.developer_timeout = None
            if hasattr(self, 'reset_timer') and self.reset_timer:
                self.reset_timer.stop()
                self.reset_timer = None
            # Note: We don't stop status_check_timer here as it should continue running
        except Exception as e:
            print(f"Error stopping timers: {e}")
    
    def start_scanning_sequence(self):
        """Start the scanning sequence for Valid Pass"""
        self.scanning_sequence_step = 1
        self.show_instructions_screen()
    
    def show_instructions_screen(self):
        """Show the instructions screen with countdown"""
        # Create overlay widget
        self.create_scanning_overlay()
        
        # Create main layout for overlay
        main_layout = QVBoxLayout(self.scanning_overlay)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Top banner - Gold/Mustard Yellow like main screen
        top_banner = QFrame()
        top_banner.setFixedHeight(120)
        top_banner.setStyleSheet("background-color: #DAA520;")
        
        countdown_label = QLabel("Getting ready in 3 second(s)...")
        countdown_label.setAlignment(Qt.AlignCenter)
        countdown_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 36px;
                font-weight: bold;
                background-color: transparent;
            }
        """)
        
        top_banner_layout = QVBoxLayout(top_banner)
        top_banner_layout.addWidget(countdown_label)
        main_layout.addWidget(top_banner)
        
        # Main content area - Split like main screen
        content_area = QFrame()
        content_layout = QHBoxLayout(content_area)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        
        # Left panel - White background with STI logo (like main screen)
        left_panel = QFrame()
        left_panel.setStyleSheet("background-color: white;")
        left_layout = QVBoxLayout(left_panel)
        left_layout.setAlignment(Qt.AlignCenter)
        
        # Load and display STI Logo (same as main screen)
        logo_path = os.path.join("image-elements", "STI Balagtas Logo.png")
        if os.path.exists(logo_path):
            logo_label = QLabel()
            pixmap = QPixmap(logo_path)
            # Scale the logo to a reasonable size for 1920x1080
            scaled_pixmap = pixmap.scaled(400, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo_label.setPixmap(scaled_pixmap)
            logo_label.setAlignment(Qt.AlignCenter)
            left_layout.addWidget(logo_label)
        else:
            # Fallback if logo not found
            fallback_label = QLabel("STI Balagtas Logo")
            fallback_label.setAlignment(Qt.AlignCenter)
            fallback_label.setStyleSheet("""
                QLabel {
                    font-size: 24px;
                    font-weight: bold;
                    color: #0066CC;
                    background-color: #FFD700;
                    padding: 20px;
                    border-radius: 3px;
                }
            """)
            left_layout.addWidget(fallback_label)
        
        content_layout.addWidget(left_panel)
        
        # Right panel - Dark blue background (like main screen)
        right_panel = QFrame()
        right_panel.setStyleSheet("background-color: #1E3A8A;")
        right_layout = QVBoxLayout(right_panel)
        right_layout.setAlignment(Qt.AlignCenter)
        
        # User icon - Load Generic User Image
        user_image_path = os.path.join("image-elements", "Generic User Image.jpg")
        if os.path.exists(user_image_path):
            user_icon = QLabel()
            pixmap = QPixmap(user_image_path)
            # Scale the user image to a reasonable size
            scaled_pixmap = pixmap.scaled(180, 180, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            
            # Create rounded corners on the image itself
            rounded_pixmap = QPixmap(scaled_pixmap.size())
            rounded_pixmap.fill(Qt.transparent)
            
            painter = QPainter(rounded_pixmap)
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setRenderHint(QPainter.SmoothPixmapTransform)
            
            # Create rounded rectangle path
            path = QPainterPath()
            path.addRoundedRect(0, 0, scaled_pixmap.width(), scaled_pixmap.height(), 3, 3)
            painter.setClipPath(path)
            
            # Draw the image
            painter.drawPixmap(0, 0, scaled_pixmap)
            painter.end()
            
            user_icon.setPixmap(rounded_pixmap)
            user_icon.setAlignment(Qt.AlignCenter)
            user_icon.setStyleSheet("""
                QLabel {
                    background-color: transparent;
                }
            """)
        else:
            # Fallback if image not found
            user_icon = QLabel("👤")
            user_icon.setFixedSize(180, 180)
            user_icon.setStyleSheet("""
                QLabel {
                    background-color: #D3D3D3;
                    border-radius: 3px;
                    border: 2px solid white;
                    font-size: 80px;
                    color: #1E3A8A;
                }
            """)
            user_icon.setAlignment(Qt.AlignCenter)
        
        right_layout.addWidget(user_icon)
        
        # ID Card info
        id_label = QLabel("Test ID Card")
        id_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                font-weight: bold;
                background-color: transparent;
                margin-top: 20px;
            }
        """)
        right_layout.addWidget(id_label, alignment=Qt.AlignCenter)
        
        role_label = QLabel("(Test User Role)")
        role_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                background-color: transparent;
            }
        """)
        right_layout.addWidget(role_label, alignment=Qt.AlignCenter)
        
        # Time check-in
        time_check_label = QLabel("Time Check-in:")
        time_check_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                background-color: transparent;
                margin-top: 40px;
            }
        """)
        right_layout.addWidget(time_check_label, alignment=Qt.AlignCenter)
        
        current_time = datetime.now().strftime("%I:%M:%S %p")
        time_value = QLabel(current_time)
        time_value.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                background-color: transparent;
            }
        """)
        right_layout.addWidget(time_value, alignment=Qt.AlignCenter)
        
        content_layout.addWidget(right_panel)
        main_layout.addWidget(content_area)
        
        # Bottom bar - Light blue and dark blue (like main screen)
        bottom_bar = QFrame()
        bottom_bar.setFixedHeight(100)
        bottom_layout = QHBoxLayout(bottom_bar)
        bottom_layout.setSpacing(0)
        bottom_layout.setContentsMargins(0, 0, 0, 0)
        
        # Date section - Light blue
        date_frame = QFrame()
        date_frame.setStyleSheet("background-color: #87CEEB;")
        date_layout = QVBoxLayout(date_frame)
        
        current_date = datetime.now().strftime("%B %d, %Y")
        date_label = QLabel(current_date)
        date_label.setAlignment(Qt.AlignCenter)
        date_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                font-weight: bold;
                background-color: transparent;
            }
        """)
        date_layout.addWidget(date_label)
        bottom_layout.addWidget(date_frame)
        
        # Time section - Dark blue
        time_frame = QFrame()
        time_frame.setStyleSheet("background-color: #021C37;")
        time_layout = QVBoxLayout(time_frame)
        
        time_display = QLabel(current_time)
        time_display.setAlignment(Qt.AlignCenter)
        time_display.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                font-weight: bold;
                background-color: transparent;
            }
        """)
        time_layout.addWidget(time_display)
        bottom_layout.addWidget(time_frame)
        
        main_layout.addWidget(bottom_bar)
        
        # Show overlay
        self.scanning_overlay.show()
        
        # Timer for next step
        self.status_timer = QTimer()
        self.status_timer.timeout.connect(self.show_instructions_image)
        self.status_timer.start(3000)  # 3 seconds
    
    def show_instructions_image(self):
        """Show the instructions image screen for 3 seconds"""
        self.scanning_sequence_step = 2
        print(f"Entering show_instructions_image - step {self.scanning_sequence_step}")
        
        # Stop any existing timer
        if hasattr(self, 'status_timer') and self.status_timer:
            self.status_timer.stop()
        
        # Clear previous content
        self.clear_overlay_content()
        
        # Create main layout for overlay
        main_layout = QVBoxLayout(self.scanning_overlay)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Top banner - Light blue like in the image
        top_banner = QFrame()
        top_banner.setFixedHeight(80)
        top_banner.setStyleSheet("background-color: #87CEEB;")
        
        progress_label = QLabel("Scanning is in progress… Please do not move.")
        progress_label.setAlignment(Qt.AlignCenter)
        progress_label.setStyleSheet("""
            QLabel {
                color: black;
                font-size: 28px;
                font-weight: bold;
                background-color: transparent;
            }
        """)
        
        top_banner_layout = QVBoxLayout(top_banner)
        top_banner_layout.addWidget(progress_label)
        main_layout.addWidget(top_banner)
        
        # Main content area - Split layout like reference
        content_area = QFrame()
        content_layout = QHBoxLayout(content_area)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        
        # Left side - Instructions image (70% width)
        left_panel = QFrame()
        left_panel.setStyleSheet("background-color: white;")
        left_layout = QVBoxLayout(left_panel)
        left_layout.setAlignment(Qt.AlignCenter)
        
        instructions_path = os.path.join("image-elements", "Instructions Scan.png")
        if os.path.exists(instructions_path):
            instructions_label = QLabel()
            pixmap = QPixmap(instructions_path)
            # Scale to fit the left panel
            scaled_pixmap = pixmap.scaled(1344, 900, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            instructions_label.setPixmap(scaled_pixmap)
            instructions_label.setAlignment(Qt.AlignCenter)
            instructions_label.setStyleSheet("background-color: transparent;")
            left_layout.addWidget(instructions_label)
        else:
            # Fallback if image not found
            fallback_label = QLabel("Instructions Scan image not found")
            fallback_label.setAlignment(Qt.AlignCenter)
            fallback_label.setStyleSheet("""
                QLabel {
                    color: red;
                    font-size: 24px;
                    font-weight: bold;
                    background-color: white;
                }
            """)
            left_layout.addWidget(fallback_label)
        
        content_layout.addWidget(left_panel, 70)  # 70% width
        
        # Right panel - User info (30% width) - Dark blue background
        right_panel = QFrame()
        right_panel.setStyleSheet("background-color: #1E3A8A;")
        right_layout = QVBoxLayout(right_panel)
        right_layout.setAlignment(Qt.AlignCenter)
        
        # User icon - Load Generic User Image with rounded corners
        user_image_path = os.path.join("image-elements", "Generic User Image.jpg")
        if os.path.exists(user_image_path):
            user_icon = QLabel()
            pixmap = QPixmap(user_image_path)
            # Scale the user image
            scaled_pixmap = pixmap.scaled(180, 180, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            
            # Create rounded corners on the image itself
            rounded_pixmap = QPixmap(scaled_pixmap.size())
            rounded_pixmap.fill(Qt.transparent)
            
            painter = QPainter(rounded_pixmap)
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setRenderHint(QPainter.SmoothPixmapTransform)
            
            # Create rounded rectangle path
            path = QPainterPath()
            path.addRoundedRect(0, 0, scaled_pixmap.width(), scaled_pixmap.height(), 3, 3)
            painter.setClipPath(path)
            
            # Draw the image
            painter.drawPixmap(0, 0, scaled_pixmap)
            painter.end()
            
            user_icon.setPixmap(rounded_pixmap)
            user_icon.setAlignment(Qt.AlignCenter)
            user_icon.setStyleSheet("""
                QLabel {
                    background-color: transparent;
                }
            """)
        else:
            # Fallback if image not found
            user_icon = QLabel("👤")
            user_icon.setFixedSize(180, 180)
            user_icon.setStyleSheet("""
                QLabel {
                    background-color: #D3D3D3;
                    border-radius: 3px;
                    border: 2px solid white;
                    font-size: 80px;
                    color: #1E3A8A;
                }
            """)
            user_icon.setAlignment(Qt.AlignCenter)
        
        right_layout.addWidget(user_icon)
        
        # ID Card info
        id_label = QLabel("Test ID Card")
        id_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 32px;
                font-weight: bold;
                background-color: transparent;
                margin-top: 20px;
            }
        """)
        right_layout.addWidget(id_label, alignment=Qt.AlignCenter)
        
        role_label = QLabel("(Test User Role)")
        role_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                background-color: transparent;
            }
        """)
        right_layout.addWidget(role_label, alignment=Qt.AlignCenter)
        
        # Time check-in
        time_check_label = QLabel("Time Check-in:")
        time_check_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                background-color: transparent;
                margin-top: 40px;
            }
        """)
        right_layout.addWidget(time_check_label, alignment=Qt.AlignCenter)
        
        current_time = datetime.now().strftime("%I:%M:%S %p")
        time_value = QLabel(current_time)
        time_value.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                background-color: transparent;
            }
        """)
        right_layout.addWidget(time_value, alignment=Qt.AlignCenter)
        
        content_layout.addWidget(right_panel, 30)  # 30% width
        main_layout.addWidget(content_area)
        
        # Bottom bar - Light blue and dark blue
        bottom_bar = QFrame()
        bottom_bar.setFixedHeight(100)
        bottom_layout = QHBoxLayout(bottom_bar)
        bottom_layout.setSpacing(0)
        bottom_layout.setContentsMargins(0, 0, 0, 0)
        
        # Date section - Light blue
        date_frame = QFrame()
        date_frame.setStyleSheet("background-color: #87CEEB;")
        date_layout = QVBoxLayout(date_frame)
        
        current_date = datetime.now().strftime("%B %d, %Y")
        date_label = QLabel(current_date)
        date_label.setAlignment(Qt.AlignCenter)
        date_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                font-weight: bold;
                background-color: transparent;
            }
        """)
        date_layout.addWidget(date_label)
        bottom_layout.addWidget(date_frame)
        
        # Time section - Dark blue
        time_frame = QFrame()
        time_frame.setStyleSheet("background-color: #021C37;")
        time_layout = QVBoxLayout(time_frame)
        
        time_display = QLabel(current_time)
        time_display.setAlignment(Qt.AlignCenter)
        time_display.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                font-weight: bold;
                background-color: transparent;
            }
        """)
        time_layout.addWidget(time_display)
        bottom_layout.addWidget(time_frame)
        
        main_layout.addWidget(bottom_bar)
        
        # Show overlay
        self.scanning_overlay.show()
        
        # Timer for next step
        self.status_timer = QTimer()
        self.status_timer.timeout.connect(self.show_scanning_progress)
        self.status_timer.start(3000)  # 3 seconds
        print(f"Timer started for step {self.scanning_sequence_step} - will call show_scanning_progress in 3 seconds")
    
    def show_scanning_progress(self):
        """Show scanning in progress screen"""
        self.scanning_sequence_step = 3
        
        # Stop any existing timer
        if hasattr(self, 'status_timer') and self.status_timer:
            self.status_timer.stop()
        
        # Clear previous content
        self.clear_overlay_content()
        
        # Create main layout for overlay
        main_layout = QVBoxLayout(self.scanning_overlay)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Top banner
        top_banner = QFrame()
        top_banner.setFixedHeight(80)
        top_banner.setStyleSheet("background-color: #87CEEB;")
        
        progress_label = QLabel("Scanning is in progress… Please do not move.")
        progress_label.setAlignment(Qt.AlignCenter)
        progress_label.setStyleSheet("""
            QLabel {
                color: black;
                font-size: 28px;
                font-weight: bold;
                background-color: transparent;
            }
        """)
        
        top_banner_layout = QVBoxLayout(top_banner)
        top_banner_layout.addWidget(progress_label)
        main_layout.addWidget(top_banner)
        
        # Main content area - black background
        content_area = QFrame()
        content_area.setStyleSheet("background-color: black;")
        content_layout = QVBoxLayout(content_area)
        content_layout.setAlignment(Qt.AlignCenter)
        
        # Scanning text
        scanning_text = QLabel("Scanning...")
        scanning_text.setAlignment(Qt.AlignCenter)
        scanning_text.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 48px;
                font-weight: bold;
                background-color: transparent;
            }
        """)
        content_layout.addWidget(scanning_text)
        
        main_layout.addWidget(content_area)
        
        # Bottom bar
        bottom_bar = QFrame()
        bottom_bar.setFixedHeight(100)
        bottom_layout = QHBoxLayout(bottom_bar)
        bottom_layout.setSpacing(0)
        bottom_layout.setContentsMargins(0, 0, 0, 0)
        
        # Date section
        date_frame = QFrame()
        date_frame.setStyleSheet("background-color: #87CEEB;")
        date_layout = QVBoxLayout(date_frame)
        
        current_date = datetime.now().strftime("%B %d, %Y")
        date_label = QLabel(current_date)
        date_label.setAlignment(Qt.AlignCenter)
        date_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                font-weight: bold;
                background-color: transparent;
            }
        """)
        date_layout.addWidget(date_label)
        bottom_layout.addWidget(date_frame)
        
        # Time section
        time_frame = QFrame()
        time_frame.setStyleSheet("background-color: #021C37;")
        time_layout = QVBoxLayout(time_frame)
        
        current_time = datetime.now().strftime("%I:%M:%S %p")
        time_display = QLabel(current_time)
        time_display.setAlignment(Qt.AlignCenter)
        time_display.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                font-weight: bold;
                background-color: transparent;
            }
        """)
        time_layout.addWidget(time_display)
        bottom_layout.addWidget(time_frame)
        
        main_layout.addWidget(bottom_bar)
        
        # Show overlay
        self.scanning_overlay.show()
        
        # Timer for next step
        self.status_timer = QTimer()
        self.status_timer.timeout.connect(self.show_scanning_complete)
        self.status_timer.start(3000)  # 3 seconds
        print(f"Timer started for step {self.scanning_sequence_step} - will call show_scanning_complete in 3 seconds")
    
    def show_scanning_complete(self):
        """Show scanning complete screen"""
        self.scanning_sequence_step = 4
        print(f"Entering show_scanning_complete - step {self.scanning_sequence_step}")
        
        # Stop any existing timer
        if hasattr(self, 'status_timer') and self.status_timer:
            self.status_timer.stop()
        
        # Clear previous content
        self.clear_overlay_content()
        
        # Create main layout for overlay
        main_layout = QVBoxLayout(self.scanning_overlay)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Top banner
        top_banner = QFrame()
        top_banner.setFixedHeight(80)
        top_banner.setStyleSheet("background-color: #87CEEB;")
        
        result_label = QLabel("Please wait for the result.")
        result_label.setAlignment(Qt.AlignCenter)
        result_label.setStyleSheet("""
            QLabel {
                color: black;
                font-size: 28px;
                font-weight: bold;
                background-color: transparent;
            }
        """)
        
        top_banner_layout = QVBoxLayout(top_banner)
        top_banner_layout.addWidget(result_label)
        main_layout.addWidget(top_banner)
        
        # Main content area - Split layout like reference
        content_area = QFrame()
        content_layout = QHBoxLayout(content_area)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        
        # Left side - Scanning complete content (70% width)
        left_panel = QFrame()
        left_panel.setStyleSheet("background-color: black;")
        left_layout = QVBoxLayout(left_panel)
        left_layout.setAlignment(Qt.AlignCenter)
        
        # Load scan-ok image
        scan_ok_path = os.path.join("image-elements", "scan-ok.png")
        if os.path.exists(scan_ok_path):
            scan_ok_label = QLabel()
            pixmap = QPixmap(scan_ok_path)
            # Scale the scan-ok image (70% bigger than before: 300 * 1.7 = 510)
            scaled_pixmap = pixmap.scaled(1024, 1024, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            scan_ok_label.setPixmap(scaled_pixmap)
            scan_ok_label.setAlignment(Qt.AlignCenter)
            left_layout.addWidget(scan_ok_label)
        
        content_layout.addWidget(left_panel, 70)  # 70% width
        
        # Right panel - User info (30% width) - Dark blue background
        right_panel = QFrame()
        right_panel.setStyleSheet("background-color: #1E3A8A;")
        right_layout = QVBoxLayout(right_panel)
        right_layout.setAlignment(Qt.AlignCenter)
        
        # User icon - Load Generic User Image with rounded corners
        user_image_path = os.path.join("image-elements", "Generic User Image.jpg")
        if os.path.exists(user_image_path):
            user_icon = QLabel()
            pixmap = QPixmap(user_image_path)
            # Scale the user image
            scaled_pixmap = pixmap.scaled(180, 180, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            
            # Create rounded corners on the image itself
            rounded_pixmap = QPixmap(scaled_pixmap.size())
            rounded_pixmap.fill(Qt.transparent)
            
            painter = QPainter(rounded_pixmap)
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setRenderHint(QPainter.SmoothPixmapTransform)
            
            # Create rounded rectangle path
            path = QPainterPath()
            path.addRoundedRect(0, 0, scaled_pixmap.width(), scaled_pixmap.height(), 3, 3)
            painter.setClipPath(path)
            
            # Draw the image
            painter.drawPixmap(0, 0, scaled_pixmap)
            painter.end()
            
            user_icon.setPixmap(rounded_pixmap)
            user_icon.setAlignment(Qt.AlignCenter)
            user_icon.setStyleSheet("""
                QLabel {
                    background-color: transparent;
                }
            """)
        else:
            # Fallback if image not found
            user_icon = QLabel("👤")
            user_icon.setFixedSize(180, 180)
            user_icon.setStyleSheet("""
                QLabel {
                    background-color: #D3D3D3;
                    border-radius: 3px;
                    border: 2px solid white;
                    font-size: 80px;
                    color: #1E3A8A;
                }
            """)
            user_icon.setAlignment(Qt.AlignCenter)
        
        right_layout.addWidget(user_icon)
        
        # ID Card info
        id_label = QLabel("Test ID Card")
        id_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 32px;
                font-weight: bold;
                background-color: transparent;
                margin-top: 20px;
            }
        """)
        right_layout.addWidget(id_label, alignment=Qt.AlignCenter)
        
        role_label = QLabel("(Test User Role)")
        role_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                background-color: transparent;
            }
        """)
        right_layout.addWidget(role_label, alignment=Qt.AlignCenter)
        
        # Time check-in
        time_check_label = QLabel("Time Check-in:")
        time_check_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                background-color: transparent;
                margin-top: 40px;
            }
        """)
        right_layout.addWidget(time_check_label, alignment=Qt.AlignCenter)
        
        current_time = datetime.now().strftime("%I:%M:%S %p")
        time_value = QLabel(current_time)
        time_value.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                background-color: transparent;
            }
        """)
        right_layout.addWidget(time_value, alignment=Qt.AlignCenter)
        
        content_layout.addWidget(right_panel, 30)  # 30% width
        main_layout.addWidget(content_area)
        
        # Bottom bar
        bottom_bar = QFrame()
        bottom_bar.setFixedHeight(100)
        bottom_layout = QHBoxLayout(bottom_bar)
        bottom_layout.setSpacing(0)
        bottom_layout.setContentsMargins(0, 0, 0, 0)
        
        # Date section
        date_frame = QFrame()
        date_frame.setStyleSheet("background-color: #87CEEB;")
        date_layout = QVBoxLayout(date_frame)
        
        current_date = datetime.now().strftime("%B %d, %Y")
        date_label = QLabel(current_date)
        date_label.setAlignment(Qt.AlignCenter)
        date_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                font-weight: bold;
                background-color: transparent;
            }
        """)
        date_layout.addWidget(date_label)
        bottom_layout.addWidget(date_frame)
        
        # Time section
        time_frame = QFrame()
        time_frame.setStyleSheet("background-color: #021C37;")
        time_layout = QVBoxLayout(time_frame)
        
        current_time = datetime.now().strftime("%I:%M:%S %p")
        time_display = QLabel(current_time)
        time_display.setAlignment(Qt.AlignCenter)
        time_display.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                font-weight: bold;
                background-color: transparent;
            }
        """)
        time_layout.addWidget(time_display)
        bottom_layout.addWidget(time_frame)
        
        main_layout.addWidget(bottom_bar)
        
        # Show overlay
        self.scanning_overlay.show()
        
        # Timer to close overlay and return to normal
        self.status_timer = QTimer()
        self.status_timer.timeout.connect(self.end_scanning_sequence)
        self.status_timer.start(3000)  # 3 seconds
        print(f"Timer started for step {self.scanning_sequence_step} - will call end_scanning_sequence in 3 seconds")
    
    def create_scanning_overlay(self):
        """Create the scanning overlay widget"""
        try:
            # Properly clean up existing overlay
            if hasattr(self, 'scanning_overlay') and self.scanning_overlay:
                self.scanning_overlay.hide()
                self.scanning_overlay.deleteLater()
                self.scanning_overlay = None
            
            # Create new overlay
            self.scanning_overlay = QWidget(self)
            self.scanning_overlay.setGeometry(0, 0, 1920, 1080)
            self.scanning_overlay.setStyleSheet("background-color: rgba(0, 0, 0, 180);")
        except Exception as e:
            print(f"Error creating scanning overlay: {e}")
            # Fallback: try to create a simple overlay
            try:
                self.scanning_overlay = QWidget(self)
                self.scanning_overlay.setGeometry(0, 0, 1920, 1080)
                self.scanning_overlay.setStyleSheet("background-color: rgba(0, 0, 0, 180);")
            except Exception as e2:
                print(f"Failed to create fallback overlay: {e2}")
                self.scanning_overlay = None
    
    def clear_overlay_content(self):
        """Clear the overlay content by recreating the overlay"""
        if self.scanning_overlay:
            self.scanning_overlay.hide()
            self.scanning_overlay.deleteLater()
            self.scanning_overlay = None
        
        # Recreate the overlay
        self.scanning_overlay = QWidget(self)
        self.scanning_overlay.setGeometry(0, 0, 1920, 1080)
        self.scanning_overlay.setStyleSheet("background-color: rgba(0, 0, 0, 180);")
    
    def end_scanning_sequence(self):
        """End the scanning sequence and show verification dialog"""
        print("Entering end_scanning_sequence - showing verification dialog")
        
        # Stop any existing timer
        if hasattr(self, 'status_timer') and self.status_timer:
            self.status_timer.stop()
        
        if self.scanning_overlay:
            self.scanning_overlay.hide()
            self.scanning_overlay.deleteLater()
            self.scanning_overlay = None
        
        self.scanning_sequence_step = 0
        
        # Show verification dialog
        self.show_verification_dialog()
        print("Showing verification dialog")
    
    def show_verification_dialog(self):
        """Show the verification dialog after scanning"""
        self.verification_dialog = QDialog(self)
        self.verification_dialog.setWindowTitle("Developer Mode")
        self.verification_dialog.setFixedSize(800, 600)
        self.verification_dialog.setModal(True)
        
        # Main layout
        main_layout = QVBoxLayout(self.verification_dialog)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Header - Mustard yellow
        header = QFrame()
        header.setFixedHeight(80)
        header.setStyleSheet("background-color: #DAA520;")
        
        header_label = QLabel("Developer Mode")
        header_label.setAlignment(Qt.AlignCenter)
        header_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 36px;
                font-weight: bold;
                background-color: transparent;
            }
        """)
        
        header_layout = QVBoxLayout(header)
        header_layout.addWidget(header_label)
        main_layout.addWidget(header)
        
        # Content area - Dark blue
        content = QFrame()
        content.setStyleSheet("background-color: #1E3A8A;")
        content_layout = QVBoxLayout(content)
        content_layout.setAlignment(Qt.AlignCenter)
        
        # Accept Automatically button - Green
        accept_button = QPushButton("Accept Automatically")
        accept_button.setFixedSize(400, 80)
        accept_button.setStyleSheet("""
            QPushButton {
                background-color: #28A745;
                color: white;
                font-size: 24px;
                font-weight: bold;
                border: none;
                border-radius: 20px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
            QPushButton:pressed {
                background-color: #1E7E34;
            }
        """)
        accept_button.clicked.connect(self.accept_automatically)
        content_layout.addWidget(accept_button, alignment=Qt.AlignCenter)
        
        # Manual Verification button - Red
        manual_button = QPushButton("Manual Verification")
        manual_button.setFixedSize(400, 80)
        manual_button.setStyleSheet("""
            QPushButton {
                background-color: #DC3545;
                color: white;
                font-size: 24px;
                font-weight: bold;
                border: none;
                border-radius: 20px;
                padding: 10px;
                margin-top: 20px;
            }
            QPushButton:hover {
                background-color: #C82333;
            }
            QPushButton:pressed {
                background-color: #BD2130;
            }
        """)
        manual_button.clicked.connect(self.manual_verification)
        content_layout.addWidget(manual_button, alignment=Qt.AlignCenter)
        
        main_layout.addWidget(content)
        
        self.verification_dialog.show()
    
    def accept_automatically(self):
        """Handle Accept Automatically button click"""
        print("Accept Automatically clicked - showing success screen")
        self.verification_dialog.close()
        self.show_success_screen()
    
    def manual_verification(self):
        """Handle Manual Verification button click"""
        print("Manual Verification clicked - showing unable to verify screen")
        self.verification_dialog.close()
        self.show_unable_to_verify_screen()
    
    def show_success_screen(self):
        """Show the success screen after accepting automatically"""
        # Create overlay for success screen
        self.create_scanning_overlay()
        
        # Create main layout for overlay
        main_layout = QVBoxLayout(self.scanning_overlay)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Top banner - Light green
        top_banner = QFrame()
        top_banner.setFixedHeight(80)
        top_banner.setStyleSheet("background-color: #90EE90;")
        
        success_label = QLabel("User Identity Verified. Thank You!")
        success_label.setAlignment(Qt.AlignCenter)
        success_label.setStyleSheet("""
            QLabel {
                color: black;
                font-size: 28px;
                font-weight: bold;
                background-color: transparent;
            }
        """)
        
        top_banner_layout = QVBoxLayout(top_banner)
        top_banner_layout.addWidget(success_label)
        main_layout.addWidget(top_banner)
        
        # Main content area - Split layout
        content_area = QFrame()
        content_layout = QHBoxLayout(content_area)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        
        # Left panel - White background with STI logo (70% width)
        left_panel = QFrame()
        left_panel.setStyleSheet("background-color: white;")
        left_layout = QVBoxLayout(left_panel)
        left_layout.setAlignment(Qt.AlignCenter)
        
        # Load and display STI Logo
        logo_path = os.path.join("image-elements", "STI Balagtas Logo.png")
        if os.path.exists(logo_path):
            logo_label = QLabel()
            pixmap = QPixmap(logo_path)
            # Scale the logo
            scaled_pixmap = pixmap.scaled(400, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo_label.setPixmap(scaled_pixmap)
            logo_label.setAlignment(Qt.AlignCenter)
            left_layout.addWidget(logo_label)
        else:
            # Fallback if logo not found
            fallback_label = QLabel("STI Balagtas Logo")
            fallback_label.setAlignment(Qt.AlignCenter)
            fallback_label.setStyleSheet("""
                QLabel {
                    font-size: 24px;
                    font-weight: bold;
                    color: #0066CC;
                    background-color: #FFD700;
                    padding: 20px;
                    border-radius: 3px;
                }
            """)
            left_layout.addWidget(fallback_label)
        
        content_layout.addWidget(left_panel, 70)  # 70% width
        
        # Right panel - User info (30% width) - Dark blue background
        right_panel = QFrame()
        right_panel.setStyleSheet("background-color: #1E3A8A;")
        right_layout = QVBoxLayout(right_panel)
        right_layout.setAlignment(Qt.AlignCenter)
        
        # User icon - Load Generic User Image with rounded corners
        user_image_path = os.path.join("image-elements", "Generic User Image.jpg")
        if os.path.exists(user_image_path):
            user_icon = QLabel()
            pixmap = QPixmap(user_image_path)
            # Scale the user image
            scaled_pixmap = pixmap.scaled(180, 180, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            
            # Create rounded corners on the image itself
            rounded_pixmap = QPixmap(scaled_pixmap.size())
            rounded_pixmap.fill(Qt.transparent)
            
            painter = QPainter(rounded_pixmap)
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setRenderHint(QPainter.SmoothPixmapTransform)
            
            # Create rounded rectangle path
            path = QPainterPath()
            path.addRoundedRect(0, 0, scaled_pixmap.width(), scaled_pixmap.height(), 3, 3)
            painter.setClipPath(path)
            
            # Draw the image
            painter.drawPixmap(0, 0, scaled_pixmap)
            painter.end()
            
            user_icon.setPixmap(rounded_pixmap)
            user_icon.setAlignment(Qt.AlignCenter)
            user_icon.setStyleSheet("""
                QLabel {
                    background-color: transparent;
                }
            """)
        else:
            # Fallback if image not found
            user_icon = QLabel("👤")
            user_icon.setFixedSize(180, 180)
            user_icon.setStyleSheet("""
                QLabel {
                    background-color: #D3D3D3;
                    border-radius: 3px;
                    border: 2px solid white;
                    font-size: 80px;
                    color: #1E3A8A;
                }
            """)
            user_icon.setAlignment(Qt.AlignCenter)
        
        right_layout.addWidget(user_icon)
        
        # ID Card info
        id_label = QLabel("Test ID Card")
        id_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 32px;
                font-weight: bold;
                background-color: transparent;
                margin-top: 20px;
            }
        """)
        right_layout.addWidget(id_label, alignment=Qt.AlignCenter)
        
        role_label = QLabel("(Test User Role)")
        role_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                background-color: transparent;
            }
        """)
        right_layout.addWidget(role_label, alignment=Qt.AlignCenter)
        
        # Time check-in
        time_check_label = QLabel("Time Check-in:")
        time_check_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                background-color: transparent;
                margin-top: 40px;
            }
        """)
        right_layout.addWidget(time_check_label, alignment=Qt.AlignCenter)
        
        current_time = datetime.now().strftime("%I:%M:%S %p")
        time_value = QLabel(current_time)
        time_value.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                background-color: transparent;
            }
        """)
        right_layout.addWidget(time_value, alignment=Qt.AlignCenter)
        
        content_layout.addWidget(right_panel, 30)  # 30% width
        main_layout.addWidget(content_area)
        
        # Bottom bar - Light blue and dark blue
        bottom_bar = QFrame()
        bottom_bar.setFixedHeight(100)
        bottom_layout = QHBoxLayout(bottom_bar)
        bottom_layout.setSpacing(0)
        bottom_layout.setContentsMargins(0, 0, 0, 0)
        
        # Date section - Light blue
        date_frame = QFrame()
        date_frame.setStyleSheet("background-color: #87CEEB;")
        date_layout = QVBoxLayout(date_frame)
        
        current_date = datetime.now().strftime("%B %d, %Y")
        date_label = QLabel(current_date)
        date_label.setAlignment(Qt.AlignCenter)
        date_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                font-weight: bold;
                background-color: transparent;
            }
        """)
        date_layout.addWidget(date_label)
        bottom_layout.addWidget(date_frame)
        
        # Time section - Dark blue
        time_frame = QFrame()
        time_frame.setStyleSheet("background-color: #021C37;")
        time_layout = QVBoxLayout(time_frame)
        
        current_time = datetime.now().strftime("%I:%M:%S %p")
        time_display = QLabel(current_time)
        time_display.setAlignment(Qt.AlignCenter)
        time_display.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                font-weight: bold;
                background-color: transparent;
            }
        """)
        time_layout.addWidget(time_display)
        bottom_layout.addWidget(time_frame)
        
        main_layout.addWidget(bottom_bar)
        
        # Show overlay
        self.scanning_overlay.show()
        
        # Timer to return to main screen after 5 seconds
        self.status_timer = QTimer()
        self.status_timer.timeout.connect(self.return_to_main_screen)
        self.status_timer.start(5000)  # 5 seconds
        print("Success screen shown - will return to main screen in 5 seconds")
    
    def return_to_main_screen(self):
        """Return to main screen after success screen"""
        try:
            print("Returning to main screen")
            
            # Stop all timers
            self.stop_all_timers()
            
            # Hide and clean up overlay
            if hasattr(self, 'scanning_overlay') and self.scanning_overlay:
                self.scanning_overlay.hide()
                self.scanning_overlay.deleteLater()
                self.scanning_overlay = None
            
            # Reset to main screen
            self.reset_to_main_screen()
        except Exception as e:
            print(f"Error returning to main screen: {e}")
            # Force reset to main screen
            try:
                self.reset_to_main_screen()
            except Exception as e2:
                print(f"Error in fallback reset: {e2}")
    
    def show_special_pass_success_screen(self):
        """Show the special pass success screen"""
        # Create overlay for special pass success screen
        self.create_scanning_overlay()
        
        # Create main layout for overlay
        main_layout = QVBoxLayout(self.scanning_overlay)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Top banner - Light green
        top_banner = QFrame()
        top_banner.setFixedHeight(80)
        top_banner.setStyleSheet("background-color: #90EE90;")
        
        success_label = QLabel("User Identity Verified. Thank You!")
        success_label.setAlignment(Qt.AlignCenter)
        success_label.setStyleSheet("""
            QLabel {
                color: black;
                font-size: 28px;
                font-weight: bold;
                background-color: transparent;
            }
        """)
        
        top_banner_layout = QVBoxLayout(top_banner)
        top_banner_layout.addWidget(success_label)
        main_layout.addWidget(top_banner)
        
        # Main content area - Split layout
        content_area = QFrame()
        content_layout = QHBoxLayout(content_area)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        
        # Left panel - White background with STI logo (70% width)
        left_panel = QFrame()
        left_panel.setStyleSheet("background-color: white;")
        left_layout = QVBoxLayout(left_panel)
        left_layout.setAlignment(Qt.AlignCenter)
        
        # Load and display STI Logo
        logo_path = os.path.join("image-elements", "STI Balagtas Logo.png")
        if os.path.exists(logo_path):
            logo_label = QLabel()
            pixmap = QPixmap(logo_path)
            # Scale the logo
            scaled_pixmap = pixmap.scaled(400, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo_label.setPixmap(scaled_pixmap)
            logo_label.setAlignment(Qt.AlignCenter)
            left_layout.addWidget(logo_label)
        else:
            # Fallback if logo not found
            fallback_label = QLabel("STI Balagtas Logo")
            fallback_label.setAlignment(Qt.AlignCenter)
            fallback_label.setStyleSheet("""
                QLabel {
                    font-size: 24px;
                    font-weight: bold;
                    color: #0066CC;
                    background-color: #FFD700;
                    padding: 20px;
                    border-radius: 3px;
                }
            """)
            left_layout.addWidget(fallback_label)
        
        content_layout.addWidget(left_panel, 70)  # 70% width
        
        # Right panel - User info (30% width) - Dark blue background
        right_panel = QFrame()
        right_panel.setStyleSheet("background-color: #1E3A8A;")
        right_layout = QVBoxLayout(right_panel)
        right_layout.setAlignment(Qt.AlignCenter)
        
        # User icon - Load Generic User Image with rounded corners
        user_image_path = os.path.join("image-elements", "Generic User Image.jpg")
        if os.path.exists(user_image_path):
            user_icon = QLabel()
            pixmap = QPixmap(user_image_path)
            # Scale the user image
            scaled_pixmap = pixmap.scaled(180, 180, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            
            # Create rounded corners on the image itself
            rounded_pixmap = QPixmap(scaled_pixmap.size())
            rounded_pixmap.fill(Qt.transparent)
            
            painter = QPainter(rounded_pixmap)
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setRenderHint(QPainter.SmoothPixmapTransform)
            
            # Create rounded rectangle path
            path = QPainterPath()
            path.addRoundedRect(0, 0, scaled_pixmap.width(), scaled_pixmap.height(), 3, 3)
            painter.setClipPath(path)
            
            # Draw the image
            painter.drawPixmap(0, 0, scaled_pixmap)
            painter.end()
            
            user_icon.setPixmap(rounded_pixmap)
            user_icon.setAlignment(Qt.AlignCenter)
            user_icon.setStyleSheet("""
                QLabel {
                    background-color: transparent;
                }
            """)
        else:
            # Fallback if image not found
            user_icon = QLabel("👤")
            user_icon.setFixedSize(180, 180)
            user_icon.setStyleSheet("""
                QLabel {
                    background-color: #D3D3D3;
                    border-radius: 3px;
                    border: 2px solid white;
                    font-size: 80px;
                    color: #1E3A8A;
                }
            """)
            user_icon.setAlignment(Qt.AlignCenter)
        
        right_layout.addWidget(user_icon)
        
        # Special Pass info instead of Test ID Card
        id_label = QLabel("Special Pass")
        id_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 32px;
                font-weight: bold;
                background-color: transparent;
                margin-top: 20px;
            }
        """)
        right_layout.addWidget(id_label, alignment=Qt.AlignCenter)
        
        ref_label = QLabel("Ref. 001")
        ref_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                background-color: transparent;
            }
        """)
        right_layout.addWidget(ref_label, alignment=Qt.AlignCenter)
        
        # Time check-in
        time_check_label = QLabel("Time Check-in:")
        time_check_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                background-color: transparent;
                margin-top: 40px;
            }
        """)
        right_layout.addWidget(time_check_label, alignment=Qt.AlignCenter)
        
        current_time = datetime.now().strftime("%I:%M:%S %p")
        time_value = QLabel(current_time)
        time_value.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                background-color: transparent;
            }
        """)
        right_layout.addWidget(time_value, alignment=Qt.AlignCenter)
        
        content_layout.addWidget(right_panel, 30)  # 30% width
        main_layout.addWidget(content_area)
        
        # Bottom bar - Light blue and dark blue
        bottom_bar = QFrame()
        bottom_bar.setFixedHeight(100)
        bottom_layout = QHBoxLayout(bottom_bar)
        bottom_layout.setSpacing(0)
        bottom_layout.setContentsMargins(0, 0, 0, 0)
        
        # Date section - Light blue
        date_frame = QFrame()
        date_frame.setStyleSheet("background-color: #87CEEB;")
        date_layout = QVBoxLayout(date_frame)
        
        current_date = datetime.now().strftime("%B %d, %Y")
        date_label = QLabel(current_date)
        date_label.setAlignment(Qt.AlignCenter)
        date_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                font-weight: bold;
                background-color: transparent;
            }
        """)
        date_layout.addWidget(date_label)
        bottom_layout.addWidget(date_frame)
        
        # Time section - Dark blue
        time_frame = QFrame()
        time_frame.setStyleSheet("background-color: #021C37;")
        time_layout = QVBoxLayout(time_frame)
        
        current_time = datetime.now().strftime("%I:%M:%S %p")
        time_display = QLabel(current_time)
        time_display.setAlignment(Qt.AlignCenter)
        time_display.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                font-weight: bold;
                background-color: transparent;
            }
        """)
        time_layout.addWidget(time_display)
        bottom_layout.addWidget(time_frame)
        
        main_layout.addWidget(bottom_bar)
        
        # Show overlay
        self.scanning_overlay.show()
        
        # Timer to return to main screen after 5 seconds
        self.status_timer = QTimer()
        self.status_timer.timeout.connect(self.return_to_main_screen)
        self.status_timer.start(5000)  # 5 seconds
        print("Special pass success screen shown - will return to main screen in 5 seconds")
    
    def show_special_pass_checkout_screen(self):
        """Show the special pass check-out screen"""
        # Create overlay for special pass check-out screen
        self.create_scanning_overlay()
        
        # Create main layout for overlay
        main_layout = QVBoxLayout(self.scanning_overlay)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Top banner - Light green
        top_banner = QFrame()
        top_banner.setFixedHeight(80)
        top_banner.setStyleSheet("background-color: #90EE90;")
        
        success_label = QLabel("User Identity Verified. Thank You!")
        success_label.setAlignment(Qt.AlignCenter)
        success_label.setStyleSheet("""
            QLabel {
                color: black;
                font-size: 28px;
                font-weight: bold;
                background-color: transparent;
            }
        """)
        
        top_banner_layout = QVBoxLayout(top_banner)
        top_banner_layout.addWidget(success_label)
        main_layout.addWidget(top_banner)
        
        # Main content area - Split layout
        content_area = QFrame()
        content_layout = QHBoxLayout(content_area)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        
        # Left panel - White background with STI logo (70% width)
        left_panel = QFrame()
        left_panel.setStyleSheet("background-color: white;")
        left_layout = QVBoxLayout(left_panel)
        left_layout.setAlignment(Qt.AlignCenter)
        
        # Load and display STI Logo
        logo_path = os.path.join("image-elements", "STI Balagtas Logo.png")
        if os.path.exists(logo_path):
            logo_label = QLabel()
            pixmap = QPixmap(logo_path)
            # Scale the logo
            scaled_pixmap = pixmap.scaled(400, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo_label.setPixmap(scaled_pixmap)
            logo_label.setAlignment(Qt.AlignCenter)
            left_layout.addWidget(logo_label)
        else:
            # Fallback if logo not found
            fallback_label = QLabel("STI Balagtas Logo")
            fallback_label.setAlignment(Qt.AlignCenter)
            fallback_label.setStyleSheet("""
                QLabel {
                    font-size: 24px;
                    font-weight: bold;
                    color: #0066CC;
                    background-color: #FFD700;
                    padding: 20px;
                    border-radius: 3px;
                }
            """)
            left_layout.addWidget(fallback_label)
        
        content_layout.addWidget(left_panel, 70)  # 70% width
        
        # Right panel - User info (30% width) - Dark blue background
        right_panel = QFrame()
        right_panel.setStyleSheet("background-color: #1E3A8A;")
        right_layout = QVBoxLayout(right_panel)
        right_layout.setAlignment(Qt.AlignCenter)
        
        # User icon - Load Generic User Image with rounded corners
        user_image_path = os.path.join("image-elements", "Generic User Image.jpg")
        if os.path.exists(user_image_path):
            user_icon = QLabel()
            pixmap = QPixmap(user_image_path)
            # Scale the user image
            scaled_pixmap = pixmap.scaled(180, 180, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            
            # Create rounded corners on the image itself
            rounded_pixmap = QPixmap(scaled_pixmap.size())
            rounded_pixmap.fill(Qt.transparent)
            
            painter = QPainter(rounded_pixmap)
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setRenderHint(QPainter.SmoothPixmapTransform)
            
            # Create rounded rectangle path
            path = QPainterPath()
            path.addRoundedRect(0, 0, scaled_pixmap.width(), scaled_pixmap.height(), 3, 3)
            painter.setClipPath(path)
            
            # Draw the image
            painter.drawPixmap(0, 0, scaled_pixmap)
            painter.end()
            
            user_icon.setPixmap(rounded_pixmap)
            user_icon.setAlignment(Qt.AlignCenter)
            user_icon.setStyleSheet("""
                QLabel {
                    background-color: transparent;
                }
            """)
        else:
            # Fallback if image not found
            user_icon = QLabel("👤")
            user_icon.setFixedSize(180, 180)
            user_icon.setStyleSheet("""
                QLabel {
                    background-color: #D3D3D3;
                    border-radius: 3px;
                    border: 2px solid white;
                    font-size: 80px;
                    color: #1E3A8A;
                }
            """)
            user_icon.setAlignment(Qt.AlignCenter)
        
        right_layout.addWidget(user_icon)
        
        # Special Pass info instead of Test ID Card
        id_label = QLabel("Special Pass")
        id_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 32px;
                font-weight: bold;
                background-color: transparent;
                margin-top: 20px;
            }
        """)
        right_layout.addWidget(id_label, alignment=Qt.AlignCenter)
        
        ref_label = QLabel("Ref. 001")
        ref_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                background-color: transparent;
            }
        """)
        right_layout.addWidget(ref_label, alignment=Qt.AlignCenter)
        
        # Time check-out (instead of check-in)
        time_check_label = QLabel("Time Check-out:")
        time_check_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                background-color: transparent;
                margin-top: 40px;
            }
        """)
        right_layout.addWidget(time_check_label, alignment=Qt.AlignCenter)
        
        current_time = datetime.now().strftime("%I:%M:%S %p")
        time_value = QLabel(current_time)
        time_value.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                background-color: transparent;
            }
        """)
        right_layout.addWidget(time_value, alignment=Qt.AlignCenter)
        
        content_layout.addWidget(right_panel, 30)  # 30% width
        main_layout.addWidget(content_area)
        
        # Bottom bar - Light blue and dark blue
        bottom_bar = QFrame()
        bottom_bar.setFixedHeight(100)
        bottom_layout = QHBoxLayout(bottom_bar)
        bottom_layout.setSpacing(0)
        bottom_layout.setContentsMargins(0, 0, 0, 0)
        
        # Date section - Light blue
        date_frame = QFrame()
        date_frame.setStyleSheet("background-color: #87CEEB;")
        date_layout = QVBoxLayout(date_frame)
        
        current_date = datetime.now().strftime("%B %d, %Y")
        date_label = QLabel(current_date)
        date_label.setAlignment(Qt.AlignCenter)
        date_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                font-weight: bold;
                background-color: transparent;
            }
        """)
        date_layout.addWidget(date_label)
        bottom_layout.addWidget(date_frame)
        
        # Time section - Dark blue
        time_frame = QFrame()
        time_frame.setStyleSheet("background-color: #021C37;")
        time_layout = QVBoxLayout(time_frame)
        
        current_time = datetime.now().strftime("%I:%M:%S %p")
        time_display = QLabel(current_time)
        time_display.setAlignment(Qt.AlignCenter)
        time_display.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                font-weight: bold;
                background-color: transparent;
            }
        """)
        time_layout.addWidget(time_display)
        bottom_layout.addWidget(time_frame)
        
        main_layout.addWidget(bottom_bar)
        
        # Show overlay
        self.scanning_overlay.show()
        
        # Timer to return to main screen after 5 seconds
        self.status_timer = QTimer()
        self.status_timer.timeout.connect(self.return_to_main_screen)
        self.status_timer.start(5000)  # 5 seconds
        print("Special pass check-out screen shown - will return to main screen in 5 seconds")
    
    def show_student_staff_checkout_screen(self):
        """Show the student/teacher/staff check-out screen"""
        # Create overlay for student/staff check-out screen
        self.create_scanning_overlay()
        
        # Create main layout for overlay
        main_layout = QVBoxLayout(self.scanning_overlay)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Top banner - Light green
        top_banner = QFrame()
        top_banner.setFixedHeight(80)
        top_banner.setStyleSheet("background-color: #90EE90;")
        
        success_label = QLabel("User Identity Verified. Thank You!")
        success_label.setAlignment(Qt.AlignCenter)
        success_label.setStyleSheet("""
            QLabel {
                color: black;
                font-size: 28px;
                font-weight: bold;
                background-color: transparent;
            }
        """)
        
        top_banner_layout = QVBoxLayout(top_banner)
        top_banner_layout.addWidget(success_label)
        main_layout.addWidget(top_banner)
        
        # Main content area - Split layout
        content_area = QFrame()
        content_layout = QHBoxLayout(content_area)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        
        # Left panel - White background with STI logo (70% width)
        left_panel = QFrame()
        left_panel.setStyleSheet("background-color: white;")
        left_layout = QVBoxLayout(left_panel)
        left_layout.setAlignment(Qt.AlignCenter)
        
        # Load and display STI Logo
        logo_path = os.path.join("image-elements", "STI Balagtas Logo.png")
        if os.path.exists(logo_path):
            logo_label = QLabel()
            pixmap = QPixmap(logo_path)
            # Scale the logo
            scaled_pixmap = pixmap.scaled(400, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo_label.setPixmap(scaled_pixmap)
            logo_label.setAlignment(Qt.AlignCenter)
            left_layout.addWidget(logo_label)
        else:
            # Fallback if logo not found
            fallback_label = QLabel("STI Balagtas Logo")
            fallback_label.setAlignment(Qt.AlignCenter)
            fallback_label.setStyleSheet("""
                QLabel {
                    font-size: 24px;
                    font-weight: bold;
                    color: #0066CC;
                    background-color: #FFD700;
                    padding: 20px;
                    border-radius: 3px;
                }
            """)
            left_layout.addWidget(fallback_label)
        
        content_layout.addWidget(left_panel, 70)  # 70% width
        
        # Right panel - User info (30% width) - Dark blue background
        right_panel = QFrame()
        right_panel.setStyleSheet("background-color: #1E3A8A;")
        right_layout = QVBoxLayout(right_panel)
        right_layout.setAlignment(Qt.AlignCenter)
        
        # User icon - Load Generic User Image with rounded corners
        user_image_path = os.path.join("image-elements", "Generic User Image.jpg")
        if os.path.exists(user_image_path):
            user_icon = QLabel()
            pixmap = QPixmap(user_image_path)
            # Scale the user image
            scaled_pixmap = pixmap.scaled(180, 180, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            
            # Create rounded corners on the image itself
            rounded_pixmap = QPixmap(scaled_pixmap.size())
            rounded_pixmap.fill(Qt.transparent)
            
            painter = QPainter(rounded_pixmap)
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setRenderHint(QPainter.SmoothPixmapTransform)
            
            # Create rounded rectangle path
            path = QPainterPath()
            path.addRoundedRect(0, 0, scaled_pixmap.width(), scaled_pixmap.height(), 3, 3)
            painter.setClipPath(path)
            
            # Draw the image
            painter.drawPixmap(0, 0, scaled_pixmap)
            painter.end()
            
            user_icon.setPixmap(rounded_pixmap)
            user_icon.setAlignment(Qt.AlignCenter)
            user_icon.setStyleSheet("""
                QLabel {
                    background-color: transparent;
                }
            """)
        else:
            # Fallback if image not found
            user_icon = QLabel("👤")
            user_icon.setFixedSize(180, 180)
            user_icon.setStyleSheet("""
                QLabel {
                    background-color: #D3D3D3;
                    border-radius: 3px;
                    border: 2px solid white;
                    font-size: 80px;
                    color: #1E3A8A;
                }
            """)
            user_icon.setAlignment(Qt.AlignCenter)
        
        right_layout.addWidget(user_icon)
        
        # Test ID Card info (standard user info)
        id_label = QLabel("Test ID Card")
        id_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 32px;
                font-weight: bold;
                background-color: transparent;
                margin-top: 20px;
            }
        """)
        right_layout.addWidget(id_label, alignment=Qt.AlignCenter)
        
        role_label = QLabel("(Test User Role)")
        role_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                background-color: transparent;
            }
        """)
        right_layout.addWidget(role_label, alignment=Qt.AlignCenter)
        
        # Time check-out
        time_check_label = QLabel("Time Check-out:")
        time_check_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                background-color: transparent;
                margin-top: 40px;
            }
        """)
        right_layout.addWidget(time_check_label, alignment=Qt.AlignCenter)
        
        current_time = datetime.now().strftime("%I:%M:%S %p")
        time_value = QLabel(current_time)
        time_value.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                background-color: transparent;
            }
        """)
        right_layout.addWidget(time_value, alignment=Qt.AlignCenter)
        
        content_layout.addWidget(right_panel, 30)  # 30% width
        main_layout.addWidget(content_area)
        
        # Bottom bar - Light blue and dark blue
        bottom_bar = QFrame()
        bottom_bar.setFixedHeight(100)
        bottom_layout = QHBoxLayout(bottom_bar)
        bottom_layout.setSpacing(0)
        bottom_layout.setContentsMargins(0, 0, 0, 0)
        
        # Date section - Light blue
        date_frame = QFrame()
        date_frame.setStyleSheet("background-color: #87CEEB;")
        date_layout = QVBoxLayout(date_frame)
        
        current_date = datetime.now().strftime("%B %d, %Y")
        date_label = QLabel(current_date)
        date_label.setAlignment(Qt.AlignCenter)
        date_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                font-weight: bold;
                background-color: transparent;
            }
        """)
        date_layout.addWidget(date_label)
        bottom_layout.addWidget(date_frame)
        
        # Time section - Dark blue
        time_frame = QFrame()
        time_frame.setStyleSheet("background-color: #021C37;")
        time_layout = QVBoxLayout(time_frame)
        
        current_time = datetime.now().strftime("%I:%M:%S %p")
        time_display = QLabel(current_time)
        time_display.setAlignment(Qt.AlignCenter)
        time_display.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                font-weight: bold;
                background-color: transparent;
            }
        """)
        time_layout.addWidget(time_display)
        bottom_layout.addWidget(time_frame)
        
        main_layout.addWidget(bottom_bar)
        
        # Show overlay
        self.scanning_overlay.show()
        
        # Timer to return to main screen after 5 seconds
        self.status_timer = QTimer()
        self.status_timer.timeout.connect(self.return_to_main_screen)
        self.status_timer.start(5000)  # 5 seconds
        print("Student/staff check-out screen shown - will return to main screen in 5 seconds")
    
    def show_unable_to_verify_screen(self):
        """Show the unable to verify identity screen"""
        # Create overlay for unable to verify screen
        self.create_scanning_overlay()
        
        # Create main layout for overlay
        main_layout = QVBoxLayout(self.scanning_overlay)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Top banner - Orange/yellow background
        top_banner = QFrame()
        top_banner.setFixedHeight(80)
        top_banner.setStyleSheet("background-color: #FFA500;")
        
        unable_label = QLabel("Unable to Verify your Identity")
        unable_label.setAlignment(Qt.AlignCenter)
        unable_label.setStyleSheet("""
            QLabel {
                color: black;
                font-size: 28px;
                font-weight: bold;
                background-color: transparent;
            }
        """)
        
        top_banner_layout = QVBoxLayout(top_banner)
        top_banner_layout.addWidget(unable_label)
        main_layout.addWidget(top_banner)
        
        # Main content area - Split layout
        content_area = QFrame()
        content_layout = QHBoxLayout(content_area)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        
        # Left panel - White background with STI logo (70% width)
        left_panel = QFrame()
        left_panel.setStyleSheet("background-color: white;")
        left_layout = QVBoxLayout(left_panel)
        left_layout.setAlignment(Qt.AlignCenter)
        
        # Load and display STI Logo
        logo_path = os.path.join("image-elements", "STI Balagtas Logo.png")
        if os.path.exists(logo_path):
            logo_label = QLabel()
            pixmap = QPixmap(logo_path)
            # Scale the logo
            scaled_pixmap = pixmap.scaled(400, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo_label.setPixmap(scaled_pixmap)
            logo_label.setAlignment(Qt.AlignCenter)
            left_layout.addWidget(logo_label)
        else:
            # Fallback if logo not found
            fallback_label = QLabel("STI Balagtas Logo")
            fallback_label.setAlignment(Qt.AlignCenter)
            fallback_label.setStyleSheet("""
                QLabel {
                    font-size: 24px;
                    font-weight: bold;
                    color: #0066CC;
                    background-color: #FFD700;
                    padding: 20px;
                    border-radius: 3px;
                }
            """)
            left_layout.addWidget(fallback_label)
        
        content_layout.addWidget(left_panel, 70)  # 70% width
        
        # Right panel - User info (30% width) - Dark blue background
        right_panel = QFrame()
        right_panel.setStyleSheet("background-color: #1E3A8A;")
        right_layout = QVBoxLayout(right_panel)
        right_layout.setAlignment(Qt.AlignCenter)
        
        # User icon - Load Generic User Image with rounded corners
        user_image_path = os.path.join("image-elements", "Generic User Image.jpg")
        if os.path.exists(user_image_path):
            user_icon = QLabel()
            pixmap = QPixmap(user_image_path)
            # Scale the user image
            scaled_pixmap = pixmap.scaled(180, 180, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            
            # Create rounded corners on the image itself
            rounded_pixmap = QPixmap(scaled_pixmap.size())
            rounded_pixmap.fill(Qt.transparent)
            
            painter = QPainter(rounded_pixmap)
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setRenderHint(QPainter.SmoothPixmapTransform)
            
            # Create rounded rectangle path
            path = QPainterPath()
            path.addRoundedRect(0, 0, scaled_pixmap.width(), scaled_pixmap.height(), 3, 3)
            painter.setClipPath(path)
            
            # Draw the image
            painter.drawPixmap(0, 0, scaled_pixmap)
            painter.end()
            
            user_icon.setPixmap(rounded_pixmap)
            user_icon.setAlignment(Qt.AlignCenter)
            user_icon.setStyleSheet("""
                QLabel {
                    background-color: transparent;
                }
            """)
        else:
            # Fallback if image not found
            user_icon = QLabel("👤")
            user_icon.setFixedSize(180, 180)
            user_icon.setStyleSheet("""
                QLabel {
                    background-color: #D3D3D3;
                    border-radius: 3px;
                    border: 2px solid white;
                    font-size: 80px;
                    color: #1E3A8A;
                }
            """)
            user_icon.setAlignment(Qt.AlignCenter)
        
        right_layout.addWidget(user_icon)
        
        # ID Card info
        id_label = QLabel("Test ID Card")
        id_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 32px;
                font-weight: bold;
                background-color: transparent;
                margin-top: 20px;
            }
        """)
        right_layout.addWidget(id_label, alignment=Qt.AlignCenter)
        
        role_label = QLabel("(Test User Role)")
        role_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                background-color: transparent;
            }
        """)
        right_layout.addWidget(role_label, alignment=Qt.AlignCenter)
        
        # Time check-in
        time_check_label = QLabel("Time Check-in:")
        time_check_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                background-color: transparent;
                margin-top: 40px;
            }
        """)
        right_layout.addWidget(time_check_label, alignment=Qt.AlignCenter)
        
        current_time = datetime.now().strftime("%I:%M:%S %p")
        time_value = QLabel(current_time)
        time_value.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                background-color: transparent;
            }
        """)
        right_layout.addWidget(time_value, alignment=Qt.AlignCenter)
        
        content_layout.addWidget(right_panel, 30)  # 30% width
        main_layout.addWidget(content_area)
        
        # Bottom bar - Light blue and dark blue
        bottom_bar = QFrame()
        bottom_bar.setFixedHeight(100)
        bottom_layout = QHBoxLayout(bottom_bar)
        bottom_layout.setSpacing(0)
        bottom_layout.setContentsMargins(0, 0, 0, 0)
        
        # Date section - Light blue
        date_frame = QFrame()
        date_frame.setStyleSheet("background-color: #87CEEB;")
        date_layout = QVBoxLayout(date_frame)
        
        current_date = datetime.now().strftime("%B %d, %Y")
        date_label = QLabel(current_date)
        date_label.setAlignment(Qt.AlignCenter)
        date_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                font-weight: bold;
                background-color: transparent;
            }
        """)
        date_layout.addWidget(date_label)
        bottom_layout.addWidget(date_frame)
        
        # Time section - Dark blue
        time_frame = QFrame()
        time_frame.setStyleSheet("background-color: #021C37;")
        time_layout = QVBoxLayout(time_frame)
        
        current_time = datetime.now().strftime("%I:%M:%S %p")
        time_display = QLabel(current_time)
        time_display.setAlignment(Qt.AlignCenter)
        time_display.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                font-weight: bold;
                background-color: transparent;
            }
        """)
        time_layout.addWidget(time_display)
        bottom_layout.addWidget(time_frame)
        
        main_layout.addWidget(bottom_bar)
        
        # Show overlay
        self.scanning_overlay.show()
        
        # Timer to show manual verification dialog after 3 seconds
        self.status_timer = QTimer()
        self.status_timer.setSingleShot(True)  # Ensure timer only fires once
        self.status_timer.timeout.connect(self.show_manual_verification_dialog)
        self.status_timer.start(3000)  # 3 seconds
        print("Unable to verify screen shown - will show manual verification dialog in 3 seconds")
    
    def show_manual_verification_dialog(self):
        """Show the manual verification dialog after unable to verify screen"""
        # Stop any existing timer first
        if hasattr(self, 'status_timer') and self.status_timer:
            self.status_timer.stop()
        
        # Hide the overlay first
        if self.scanning_overlay:
            self.scanning_overlay.hide()
        
        # Check if dialog already exists and close it
        if hasattr(self, 'manual_verification_dialog') and self.manual_verification_dialog:
            self.manual_verification_dialog.close()
        
        self.manual_verification_dialog = QDialog(self)
        self.manual_verification_dialog.setWindowTitle("Developer Mode")
        self.manual_verification_dialog.setFixedSize(800, 600)
        self.manual_verification_dialog.setModal(True)
        
        # Main layout
        main_layout = QVBoxLayout(self.manual_verification_dialog)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Header - Mustard yellow
        header = QFrame()
        header.setFixedHeight(80)
        header.setStyleSheet("background-color: #DAA520;")
        
        header_label = QLabel("Developer Mode")
        header_label.setAlignment(Qt.AlignCenter)
        header_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 36px;
                font-weight: bold;
                background-color: transparent;
            }
        """)
        
        header_layout = QVBoxLayout(header)
        header_layout.addWidget(header_label)
        main_layout.addWidget(header)
        
        # Content area - Dark blue
        content = QFrame()
        content.setStyleSheet("background-color: #1E3A8A;")
        content_layout = QVBoxLayout(content)
        content_layout.setAlignment(Qt.AlignCenter)
        
        # Manual verification text
        manual_text = QLabel("For Manual Verification:")
        manual_text.setAlignment(Qt.AlignCenter)
        manual_text.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 28px;
                font-weight: bold;
                background-color: transparent;
                margin-bottom: 30px;
            }
        """)
        content_layout.addWidget(manual_text, alignment=Qt.AlignCenter)
        
        # Accept Entry button - Green
        accept_entry_button = QPushButton("Accept Entry")
        accept_entry_button.setFixedSize(400, 80)
        accept_entry_button.setStyleSheet("""
            QPushButton {
                background-color: #28A745;
                color: white;
                font-size: 24px;
                font-weight: bold;
                border: none;
                border-radius: 20px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
            QPushButton:pressed {
                background-color: #1E7E34;
            }
        """)
        accept_entry_button.clicked.connect(self.accept_entry)
        content_layout.addWidget(accept_entry_button, alignment=Qt.AlignCenter)
        
        # Deny Entry button - Red
        deny_entry_button = QPushButton("Deny Entry")
        deny_entry_button.setFixedSize(400, 80)
        deny_entry_button.setStyleSheet("""
            QPushButton {
                background-color: #DC3545;
                color: white;
                font-size: 24px;
                font-weight: bold;
                border: none;
                border-radius: 20px;
                padding: 10px;
                margin-top: 20px;
            }
            QPushButton:hover {
                background-color: #C82333;
            }
            QPushButton:pressed {
                background-color: #BD2130;
            }
        """)
        deny_entry_button.clicked.connect(self.deny_entry)
        content_layout.addWidget(deny_entry_button, alignment=Qt.AlignCenter)
        
        main_layout.addWidget(content)
        
        self.manual_verification_dialog.show()
    
    def accept_entry(self):
        """Handle Accept Entry button click"""
        print("Accept Entry clicked - showing success screen")
        
        # Stop any existing timer
        if hasattr(self, 'status_timer') and self.status_timer:
            self.status_timer.stop()
        
        self.manual_verification_dialog.close()
        self.show_success_screen()
    
    def deny_entry(self):
        """Handle Deny Entry button click"""
        print("Deny Entry clicked - showing uniform issue screen")
        
        # Stop any existing timer
        if hasattr(self, 'status_timer') and self.status_timer:
            self.status_timer.stop()
        
        self.manual_verification_dialog.close()
        self.show_uniform_issue_screen()
    
    def show_uniform_issue_screen(self):
        """Show the uniform issue screen after denying entry"""
        # Create overlay for uniform issue screen
        self.create_scanning_overlay()
        
        # Create main layout for overlay
        main_layout = QVBoxLayout(self.scanning_overlay)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Top banner - Light orange/tan background
        top_banner = QFrame()
        top_banner.setFixedHeight(80)
        top_banner.setStyleSheet("background-color: #D2B48C;")
        
        uniform_label = QLabel("Different / Incomplete Uniform Found.")
        uniform_label.setAlignment(Qt.AlignCenter)
        uniform_label.setStyleSheet("""
            QLabel {
                color: black;
                font-size: 28px;
                font-weight: bold;
                background-color: transparent;
            }
        """)
        
        top_banner_layout = QVBoxLayout(top_banner)
        top_banner_layout.addWidget(uniform_label)
        main_layout.addWidget(top_banner)
        
        # Main content area - Split layout
        content_area = QFrame()
        content_layout = QHBoxLayout(content_area)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        
        # Left panel - White background with STI logo (70% width)
        left_panel = QFrame()
        left_panel.setStyleSheet("background-color: white;")
        left_layout = QVBoxLayout(left_panel)
        left_layout.setAlignment(Qt.AlignCenter)
        
        # Load and display STI Logo
        logo_path = os.path.join("image-elements", "STI Balagtas Logo.png")
        if os.path.exists(logo_path):
            logo_label = QLabel()
            pixmap = QPixmap(logo_path)
            # Scale the logo
            scaled_pixmap = pixmap.scaled(400, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo_label.setPixmap(scaled_pixmap)
            logo_label.setAlignment(Qt.AlignCenter)
            left_layout.addWidget(logo_label)
        else:
            # Fallback if logo not found
            fallback_label = QLabel("STI Balagtas Logo")
            fallback_label.setAlignment(Qt.AlignCenter)
            fallback_label.setStyleSheet("""
                QLabel {
                    font-size: 24px;
                    font-weight: bold;
                    color: #0066CC;
                    background-color: #FFD700;
                    padding: 20px;
                    border-radius: 3px;
                }
            """)
            left_layout.addWidget(fallback_label)
        
        content_layout.addWidget(left_panel, 70)  # 70% width
        
        # Right panel - User info (30% width) - Dark blue background
        right_panel = QFrame()
        right_panel.setStyleSheet("background-color: #1E3A8A;")
        right_layout = QVBoxLayout(right_panel)
        right_layout.setAlignment(Qt.AlignCenter)
        
        # User icon - Load Generic User Image with rounded corners
        user_image_path = os.path.join("image-elements", "Generic User Image.jpg")
        if os.path.exists(user_image_path):
            user_icon = QLabel()
            pixmap = QPixmap(user_image_path)
            # Scale the user image
            scaled_pixmap = pixmap.scaled(180, 180, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            
            # Create rounded corners on the image itself
            rounded_pixmap = QPixmap(scaled_pixmap.size())
            rounded_pixmap.fill(Qt.transparent)
            
            painter = QPainter(rounded_pixmap)
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setRenderHint(QPainter.SmoothPixmapTransform)
            
            # Create rounded rectangle path
            path = QPainterPath()
            path.addRoundedRect(0, 0, scaled_pixmap.width(), scaled_pixmap.height(), 3, 3)
            painter.setClipPath(path)
            
            # Draw the image
            painter.drawPixmap(0, 0, scaled_pixmap)
            painter.end()
            
            user_icon.setPixmap(rounded_pixmap)
            user_icon.setAlignment(Qt.AlignCenter)
            user_icon.setStyleSheet("""
                QLabel {
                    background-color: transparent;
                }
            """)
        else:
            # Fallback if image not found
            user_icon = QLabel("👤")
            user_icon.setFixedSize(180, 180)
            user_icon.setStyleSheet("""
                QLabel {
                    background-color: #D3D3D3;
                    border-radius: 3px;
                    border: 2px solid white;
                    font-size: 80px;
                    color: #1E3A8A;
                }
            """)
            user_icon.setAlignment(Qt.AlignCenter)
        
        right_layout.addWidget(user_icon)
        
        # ID Card info
        id_label = QLabel("Test ID Card")
        id_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 32px;
                font-weight: bold;
                background-color: transparent;
                margin-top: 20px;
            }
        """)
        right_layout.addWidget(id_label, alignment=Qt.AlignCenter)
        
        role_label = QLabel("(Test User Role)")
        role_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                background-color: transparent;
            }
        """)
        right_layout.addWidget(role_label, alignment=Qt.AlignCenter)
        
        # Time check-in
        time_check_label = QLabel("Time Check-in:")
        time_check_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                background-color: transparent;
                margin-top: 40px;
            }
        """)
        right_layout.addWidget(time_check_label, alignment=Qt.AlignCenter)
        
        current_time = datetime.now().strftime("%I:%M:%S %p")
        time_value = QLabel(current_time)
        time_value.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                background-color: transparent;
            }
        """)
        right_layout.addWidget(time_value, alignment=Qt.AlignCenter)
        
        content_layout.addWidget(right_panel, 30)  # 30% width
        main_layout.addWidget(content_area)
        
        # Bottom bar - Light blue and dark blue
        bottom_bar = QFrame()
        bottom_bar.setFixedHeight(100)
        bottom_layout = QHBoxLayout(bottom_bar)
        bottom_layout.setSpacing(0)
        bottom_layout.setContentsMargins(0, 0, 0, 0)
        
        # Date section - Light blue
        date_frame = QFrame()
        date_frame.setStyleSheet("background-color: #87CEEB;")
        date_layout = QVBoxLayout(date_frame)
        
        current_date = datetime.now().strftime("%B %d, %Y")
        date_label = QLabel(current_date)
        date_label.setAlignment(Qt.AlignCenter)
        date_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                font-weight: bold;
                background-color: transparent;
            }
        """)
        date_layout.addWidget(date_label)
        bottom_layout.addWidget(date_frame)
        
        # Time section - Dark blue
        time_frame = QFrame()
        time_frame.setStyleSheet("background-color: #021C37;")
        time_layout = QVBoxLayout(time_frame)
        
        current_time = datetime.now().strftime("%I:%M:%S %p")
        time_display = QLabel(current_time)
        time_display.setAlignment(Qt.AlignCenter)
        time_display.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                font-weight: bold;
                background-color: transparent;
            }
        """)
        time_layout.addWidget(time_display)
        bottom_layout.addWidget(time_frame)
        
        main_layout.addWidget(bottom_bar)
        
        # Show overlay
        self.scanning_overlay.show()
        
        # Timer to return to main screen after 5 seconds
        self.status_timer = QTimer()
        self.status_timer.timeout.connect(self.return_to_main_screen)
        self.status_timer.start(5000)  # 5 seconds
        print("Uniform issue screen shown - will return to main screen in 5 seconds")

    def show_instructions_then_person(self, person_name, person_role, time_value, guard_name):
        """Show the instructions overlay first, then show the person info on the main screen."""
        try:
            # Guard: prevent double-start
            if getattr(self, 'sequence_in_progress', False):
                print("Sequence already in progress; ignoring duplicate call")
                return
            self.sequence_in_progress = True

            # Stop any existing short timers
            if hasattr(self, 'status_timer') and self.status_timer:
                self.status_timer.stop()

            # Create overlay
            self.create_scanning_overlay()

            # Build simple overlay with top banner and instructions image
            overlay_layout = QVBoxLayout(self.scanning_overlay)
            overlay_layout.setContentsMargins(0, 0, 0, 0)
            overlay_layout.setSpacing(0)

            # Top banner
            top_banner = QFrame()
            top_banner.setFixedHeight(120)
            top_banner.setStyleSheet("background-color: #ADD8E6;")  # Light blue like screenshot
            top_layout = QVBoxLayout(top_banner)
            banner_label = QLabel("Getting ready in 3 second(s)...")
            banner_label.setAlignment(Qt.AlignCenter)
            banner_label.setStyleSheet("""
                QLabel { color: black; font-size: 36px; font-weight: bold; background-color: transparent; }
            """)
            top_layout.addWidget(banner_label)
            overlay_layout.addWidget(top_banner)

            # Content area split 70/30 like the instructions screen
            content_area = QFrame()
            content_layout = QHBoxLayout(content_area)
            content_layout.setContentsMargins(0, 0, 0, 0)
            content_layout.setSpacing(0)

            # Left: instructions image
            left_panel = QFrame()
            left_panel.setStyleSheet("background-color: white;")
            left_layout = QVBoxLayout(left_panel)
            left_layout.setAlignment(Qt.AlignCenter)
            instructions_path = os.path.join("image-elements", "Instructions Scan.png")
            if os.path.exists(instructions_path):
                img_label = QLabel()
                pix = QPixmap(instructions_path)
                scaled = pix.scaled(1344, 900, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                img_label.setPixmap(scaled)
                img_label.setAlignment(Qt.AlignCenter)
                left_layout.addWidget(img_label)
            else:
                fallback = QLabel("Instructions Scan image not found")
                fallback.setAlignment(Qt.AlignCenter)
                fallback.setStyleSheet("QLabel { color: red; font-size: 24px; font-weight: bold; }")
                left_layout.addWidget(fallback)
            content_layout.addWidget(left_panel, 70)

            # Right: simple person summary (optional)
            right_panel = QFrame()
            right_panel.setStyleSheet("background-color: #1E3A8A;")
            right_layout = QVBoxLayout(right_panel)
            right_layout.setAlignment(Qt.AlignCenter)

            # Generic user icon
            user_image_path = os.path.join("image-elements", "Generic User Image.jpg")
            icon_label = QLabel()
            if os.path.exists(user_image_path):
                upix = QPixmap(user_image_path).scaled(180, 180, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                icon_label.setPixmap(upix)
            icon_label.setAlignment(Qt.AlignCenter)
            icon_label.setStyleSheet("background-color: transparent;")
            right_layout.addWidget(icon_label)

            # Name and role (smaller preview)
            preview_name = QLabel(person_name)
            preview_name.setAlignment(Qt.AlignCenter)
            preview_name.setStyleSheet("QLabel { color: white; font-size: 28px; font-weight: bold; background: transparent; margin-top: 10px; }")
            right_layout.addWidget(preview_name)

            preview_role = QLabel(f"({person_role})")
            preview_role.setAlignment(Qt.AlignCenter)
            preview_role.setStyleSheet("QLabel { color: white; font-size: 20px; background: transparent; }")
            right_layout.addWidget(preview_role)

            # Time
            preview_time_label = QLabel("Time Check-in:")
            preview_time_label.setAlignment(Qt.AlignCenter)
            preview_time_label.setStyleSheet("QLabel { color: white; font-size: 18px; background: transparent; margin-top: 20px; }")
            right_layout.addWidget(preview_time_label)

            preview_time_val = QLabel(time_value)
            preview_time_val.setAlignment(Qt.AlignCenter)
            preview_time_val.setStyleSheet("QLabel { color: white; font-size: 18px; background: transparent; }")
            right_layout.addWidget(preview_time_val)

            content_layout.addWidget(right_panel, 30)
            overlay_layout.addWidget(content_area)

            # Bottom bar (date/time like existing)
            bottom_bar = QFrame()
            bottom_bar.setFixedHeight(100)
            bottom_layout = QHBoxLayout(bottom_bar)
            bottom_layout.setSpacing(0)
            bottom_layout.setContentsMargins(0, 0, 0, 0)

            date_frame = QFrame(); date_frame.setStyleSheet("background-color: #87CEEB;")
            date_layout = QVBoxLayout(date_frame)
            date_label = QLabel(datetime.now().strftime("%B %d, %Y"))
            date_label.setAlignment(Qt.AlignCenter)
            date_label.setStyleSheet("QLabel { color: white; font-size: 24px; font-weight: bold; background: transparent; }")
            date_layout.addWidget(date_label)
            bottom_layout.addWidget(date_frame)

            time_frame = QFrame(); time_frame.setStyleSheet("background-color: #021C37;")
            time_layout = QVBoxLayout(time_frame)
            time_label = QLabel(datetime.now().strftime("%I:%M:%S %p"))
            time_label.setAlignment(Qt.AlignCenter)
            time_label.setStyleSheet("QLabel { color: white; font-size: 24px; font-weight: bold; background: transparent; }")
            time_layout.addWidget(time_label)
            bottom_layout.addWidget(time_frame)

            overlay_layout.addWidget(bottom_bar)

            # Show overlay and schedule two-phase sequence:
            # 1) 3s Getting ready  ->  2) 5s Scanning in progress  ->  Person info
            if self.scanning_overlay:
                self.scanning_overlay.show()

            # Phase 1 timer (3s)
            self.status_timer = QTimer(self)
            def _start_scanning_phase():
                try:
                    if self.status_timer:
                        self.status_timer.stop()
                except Exception:
                    pass

                # Update banner to scanning message
                try:
                    banner_label.setText("Scanning is in progress... Please do not move.")
                except Exception:
                    pass

                # Phase 2 timer (5s) then show "Scanning Complete" for 2s, then finish
                self.status_timer = QTimer(self)
                def _show_scanning_complete():
                    try:
                        if self.status_timer:
                            self.status_timer.stop()
                    except Exception:
                        pass

                    # Update banner to result message
                    try:
                        banner_label.setText("Please wait for the result.")
                    except Exception:
                        pass

                    # Replace left panel content with scan-ok image on black background
                    try:
                        left_panel.setStyleSheet("background-color: black;")
                        # Clear existing items in left_layout
                        try:
                            while left_layout.count():
                                item = left_layout.takeAt(0)
                                w = item.widget()
                                if w:
                                    w.deleteLater()
                        except Exception:
                            pass

                        ok_path = os.path.join("image-elements", "scan-ok.png")
                        ok_label = QLabel()
                        if os.path.exists(ok_path):
                            ok_pix = QPixmap(ok_path)
                            ok_scaled = ok_pix.scaled(1344, 900, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                            ok_label.setPixmap(ok_scaled)
                        ok_label.setAlignment(Qt.AlignCenter)
                        ok_label.setStyleSheet("background-color: transparent;")
                        left_layout.addWidget(ok_label)
                    except Exception as e:
                        print(f"Error showing scan-ok image: {e}")

                    # Hold for 2 seconds then finish
                    self.status_timer = QTimer(self)
                    def _finish():
                        # Hide overlay and show the person info screen
                        if self.scanning_overlay:
                            self.scanning_overlay.hide()
                            self.scanning_overlay.deleteLater()
                            self.scanning_overlay = None
                        self.show_student_teacher_info(person_name, person_role, time_value, guard_name)
                        self.sequence_in_progress = False
                    self.status_timer.timeout.connect(_finish)
                    self.status_timer.setSingleShot(True)
                    self.status_timer.start(2000)  # 2 seconds for scanning complete

                self.status_timer.timeout.connect(_show_scanning_complete)
                self.status_timer.setSingleShot(True)
                self.status_timer.start(5000)  # 5 seconds scanning screen

            self.status_timer.timeout.connect(_start_scanning_phase)
            self.status_timer.setSingleShot(True)
            self.status_timer.start(3000)  # 3 seconds getting-ready screen
        except Exception as e:
            print(f"Error showing instructions then person: {e}")
            # Fallback directly to person info
            self.show_student_teacher_info(person_name, person_role, time_value, guard_name)
            self.sequence_in_progress = False

def signal_handler(signum, frame):
    """Handle termination signals"""
    print(f"Received signal {signum} - writing close status")
    try:
        with open("main_screen_status.txt", "w") as f:
            f.write("MAIN_SCREEN_CLOSED\n")
            f.write("N/A\n")
            f.write("N/A\n")
            f.write("N/A\n")
        print("Close status written to file")
    except Exception as e:
        print(f"Error writing close status: {e}")
    sys.exit(0)

def main():
    # Set up signal handlers
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    
    app = QApplication(sys.argv)
    
    # Set application style for better macOS appearance
    app.setStyle('Fusion')
    
    window = STIWelcomeScreen()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
