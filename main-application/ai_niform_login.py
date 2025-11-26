import tkinter as tk
from tkinter import ttk, messagebox, Canvas
from PIL import Image, ImageTk
import datetime
import time
import os
import cv2
import numpy as np
from ultralytics import YOLO
from database_manager import DatabaseManager
import json
import os.path
from datetime import datetime, timedelta
import subprocess
import threading
import sys
import threading
import platform

# PyQt5 imports for main screen window
try:
    from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame
    from PyQt5.QtCore import QTimer, Qt
    from PyQt5.QtGui import QPixmap, QFont
    PYQT5_AVAILABLE = True
except ImportError:
    PYQT5_AVAILABLE = False
    print("PyQt5 not available - main screen will launch as separate process")

class STIMainScreenWindow(QMainWindow):
    """PyQt5 Main Screen Window integrated into the tkinter application"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI-niform - Main Screen")
        self.setGeometry(100, 100, 1920, 1080)
        self.setFixedSize(1920, 1080)
        
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
        
        # Enable key events
        self.setFocusPolicy(Qt.StrongFocus)
    
    def setup_ui(self, layout):
        """Setup the main screen UI"""
        # Top Banner
        top_banner = QFrame()
        top_banner.setFixedHeight(120)
        top_banner.setStyleSheet("background-color: #DAA520;")
        
        welcome_label = QLabel("Welcome to STI College Balagtas!")
        welcome_label.setAlignment(Qt.AlignCenter)
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
        
        # Main Content Area
        main_content = QFrame()
        main_layout = QHBoxLayout(main_content)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Left Panel (Logo)
        left_panel = QFrame()
        left_panel.setStyleSheet("background-color: white;")
        left_layout = QVBoxLayout(left_panel)
        left_layout.setAlignment(Qt.AlignCenter)
        
        # Load and display STI Logo
        logo_path = os.path.join("image-elements", "STI Balagtas Logo.png")
        if os.path.exists(logo_path):
            logo_label = QLabel()
            pixmap = QPixmap(logo_path)
            scaled_pixmap = pixmap.scaled(400, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo_label.setPixmap(scaled_pixmap)
            logo_label.setAlignment(Qt.AlignCenter)
            left_layout.addWidget(logo_label)
        else:
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
        
        main_layout.addWidget(left_panel, 40)
        
        # Right Panel (Card Reader)
        right_panel = QFrame()
        right_panel.setStyleSheet("background-color: #4A90E2;")
        right_layout = QVBoxLayout(right_panel)
        right_layout.setAlignment(Qt.AlignCenter)
        
        # Card Reader Interface
        self.instruction_label = QLabel("Please tap your ID\nto the Card Reader")
        self.instruction_label.setAlignment(Qt.AlignCenter)
        self.instruction_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                font-weight: bold;
                background-color: transparent;
            }
        """)
        right_layout.addWidget(self.instruction_label)
        
        # Status label
        self.status_label = QLabel("Ready for scanning...")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 18px;
                background-color: transparent;
            }
        """)
        right_layout.addWidget(self.status_label)
        
        main_layout.addWidget(right_panel, 60)
        layout.addWidget(main_content)
        
        # Bottom bar
        bottom_bar = QFrame()
        bottom_bar.setFixedHeight(100)
        bottom_layout = QHBoxLayout(bottom_bar)
        
        # Date and time
        current_date = datetime.now().strftime("%B %d, %Y")
        current_time = datetime.now().strftime("%I:%M:%S %p")
        
        date_label = QLabel(current_date)
        date_label.setAlignment(Qt.AlignCenter)
        date_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 18px;
                font-weight: bold;
                background-color: #87CEEB;
            }
        """)
        
        time_label = QLabel(current_time)
        time_label.setAlignment(Qt.AlignCenter)
        time_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 18px;
                font-weight: bold;
                background-color: #021C37;
            }
        """)
        
        bottom_layout.addWidget(date_label)
        bottom_layout.addWidget(time_label)
        layout.addWidget(bottom_bar)
    
    def setup_timer(self):
        """Setup timer for updating time"""
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)
    
    def update_time(self):
        """Update the time display"""
        current_time = datetime.now().strftime("%I:%M:%S %p")
        # Update time label if it exists
        for child in self.findChildren(QLabel):
            if ":" in child.text() and len(child.text()) < 15:
                child.setText(current_time)
                break
    
    def keyPressEvent(self, event):
        """Handle key press events"""
        if event.key() == Qt.Key_Escape:
            self.close()
        else:
            super().keyPressEvent(event)
    
    def closeEvent(self, event):
        """Handle window close event"""
        # Notify the parent application that this window is closing
        if hasattr(self, 'parent_app'):
            self.parent_app.on_main_screen_closed()
        event.accept()

class YOLOCameraDetection:
    def __init__(self, model_path='best.pt', camera_id=0, confidence_threshold=0.5):
        """Initialize YOLO Camera Detection"""
        self.model_path = model_path
        self.camera_id = camera_id
        self.confidence_threshold = confidence_threshold
        self.cap = None
        self.model = None
        self.is_running = False
        
    def load_model(self):
        """Load YOLO model"""
        try:
            print(f"Loading YOLO model from {self.model_path}...")
            if os.path.exists(self.model_path):
                self.model = YOLO(self.model_path)
                print("Model loaded successfully!")
                return True
            else:
                print(f"Model file {self.model_path} not found. Using placeholder detection.")
                self.model = None
                return False
        except Exception as e:
            print(f"Error loading model: {e}")
            self.model = None
            return False
    
    def initialize_camera(self):
        """Initialize camera capture"""
        try:
            self.cap = cv2.VideoCapture(self.camera_id)
            if not self.cap.isOpened():
                print(f"Error: Could not open camera {self.camera_id}")
                return False
            
            # Set camera properties
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            self.cap.set(cv2.CAP_PROP_FPS, 30)
            
            print(f"Camera {self.camera_id} initialized successfully!")
            return True
        except Exception as e:
            print(f"Error initializing camera: {e}")
            return False
    
    def detect_objects(self, frame):
        """Perform object detection on frame"""
        try:
            if self.model is None:
                return []
            
            # Run YOLO detection
            results = self.model(frame, conf=self.confidence_threshold, verbose=False)
            
            # Process results
            detections = []
            for result in results:
                boxes = result.boxes
                if boxes is not None:
                    for box in boxes:
                        # Get box coordinates
                        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                        
                        # Get confidence and class
                        confidence = float(box.conf[0])
                        class_id = int(box.cls[0])
                        class_name = self.model.names[class_id]
                        
                        detections.append({
                            'bbox': (x1, y1, x2, y2),
                            'confidence': confidence,
                            'class_id': class_id,
                            'class_name': class_name
                        })
            
            # Print debugging information
            self.print_detection_debug(detections)
            
            return detections
        except Exception as e:
            print(f"Error during detection: {e}")
            return []
    
    def print_detection_debug(self, detections):
        """Print debugging information for YOLO detections"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n[{timestamp}] " + "="*50)
        print("YOLO DETECTION RESULTS")
        print("="*50)
        
        if not detections:
            print("ict longsleeve = 0")
            print("ict logo = 0")
            print("black shoes = 0")
            print("ict pants = 0")
            print("\nRESULT = MANUAL VERIFICATION")
            return
        
        # Count detections by class
        class_counts = {}
        for detection in detections:
            class_name = detection['class_name'].lower()
            class_counts[class_name] = class_counts.get(class_name, 0) + 1
        
        # Print counts for each expected class
        ict_longsleeve = class_counts.get('ict longsleeve', 0)
        ict_logo = class_counts.get('ict logo', 0)
        black_shoes = class_counts.get('black shoes', 0)
        ict_pants = class_counts.get('ict pants', 0)
        
        print(f"ict longsleeve = {ict_longsleeve}")
        print(f"ict logo = {ict_logo}")
        print(f"black shoes = {black_shoes}")
        print(f"ict pants = {ict_pants}")
        
        # Determine result based on detection counts
        total_detections = sum(class_counts.values())
        
        if total_detections == 0:
            print("\nRESULT = MANUAL VERIFICATION")
        elif ict_longsleeve >= 1 and ict_logo >= 1 and black_shoes >= 1 and ict_pants >= 1:
            print("\nRESULT = ENTRY ACCESS")
        else:
            print("\nRESULT = MANUAL VERIFICATION")
        
        print("="*50)
    
    def draw_detections(self, frame, detections):
        """Draw detection boxes and labels on frame"""
        for detection in detections:
            x1, y1, x2, y2 = detection['bbox']
            confidence = detection['confidence']
            class_name = detection['class_name']
            
            # Draw bounding box
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
            # Create label
            label = f"{class_name}: {confidence:.2f}"
            
            # Get label size
            (label_width, label_height), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
            
            # Draw label background
            cv2.rectangle(frame, (x1, y1 - label_height - 10), (x1 + label_width, y1), (0, 255, 0), -1)
            
            # Draw label text
            cv2.putText(frame, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
        
        return frame
    
    def get_frame_with_detection(self):
        """Get a frame with object detection"""
        if self.cap is None:
            return None
        
        ret, frame = self.cap.read()
        if not ret:
            return None
        
        # Perform object detection
        detections = self.detect_objects(frame)
        
        # Draw detections
        frame = self.draw_detections(frame, detections)
        
        return frame
    
    def cleanup(self):
        """Clean up resources"""
        self.is_running = False
        if self.cap is not None:
            self.cap.release()
        print("Camera cleanup completed")

class StudentTeacherSplashScreen:
    def __init__(self, main_frame, person_data, duration=8, app_instance=None):
        """Initialize splash screen for student/teacher"""
        self.main_frame = main_frame
        self.person_data = person_data
        self.duration = duration
        self.camera_detector = None
        self.is_running = False
        self.splash_frame = None
        self.original_widgets = []
        self.app_instance = app_instance
        
    def show_splash(self):
        """Show the splash screen in the main window"""
        # Store original widgets
        self.store_original_widgets()
        
        # Clear the main frame
        self.clear_main_frame()
        
        # Create splash content directly in main frame
        self.create_splash_content()
        
        # Initialize camera
        self.initialize_camera()
        
        # Start camera feed
        self.start_camera_feed()
        
        # Auto-close after duration
        self.main_frame.after(self.duration * 1000, self.close_splash)
        
        # Bind escape key to close
        self.main_frame.master.bind('<Escape>', lambda e: self.close_splash())
        
    def store_original_widgets(self):
        """Store the original widgets in main frame"""
        self.original_widgets = []
        for widget in self.main_frame.winfo_children():
            self.original_widgets.append(widget)
        
    def clear_main_frame(self):
        """Clear the main frame"""
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
    def restore_original_widgets(self):
        """Restore the original interface"""
        # Clear current content
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        # Recreate the guard interface
        if self.app_instance:
            self.app_instance.show_guard_interface()
    
    def create_splash_content(self):
        """Create the splash screen content"""
        # Main container
        main_container = tk.Frame(self.main_frame, bg='white')
        main_container.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Left side - Camera feed
        camera_frame = tk.Frame(main_container, bg='black', width=640, height=480)
        camera_frame.pack(side='left', padx=(0, 20))
        camera_frame.pack_propagate(False)
        
        # Camera label
        self.camera_label = tk.Label(camera_frame, bg='black', text="Initializing camera...")
        self.camera_label.pack(expand=True)
        
        # Right side - Information panel
        info_frame = tk.Frame(main_container, bg='#4A90E2', width=400, height=480)
        info_frame.pack(side='right', fill='y')
        info_frame.pack_propagate(False)
        
        # Profile picture
        self.create_profile_section(info_frame)
        
        # Information section
        self.create_info_section(info_frame)
        
        # Uniform compliance section
        self.create_compliance_section(info_frame)
        
    def create_profile_section(self, parent, person_data=None):
        """Create profile picture section"""
        profile_frame = tk.Frame(parent, bg='#4A90E2')
        profile_frame.pack(pady=20)
        
        # Use provided person_data or fall back to self.person_data
        data = person_data if person_data else self.person_data
        
        # Load profile picture
        profile_image = self.load_profile_image_for_person(data)
        if profile_image:
            # Resize to 2x2 inches (approximately 150x150 pixels)
            profile_image = profile_image.resize((150, 150), Image.Resampling.LANCZOS)
            self.profile_photo = ImageTk.PhotoImage(profile_image)
            
            profile_label = tk.Label(profile_frame, image=self.profile_photo, bg='#4A90E2')
            profile_label.pack()
        else:
            # Default profile picture
            default_label = tk.Label(profile_frame, text="No Photo", font=("Arial", 16), 
                                   bg='#4A90E2', fg='white', width=10, height=6)
            default_label.pack()
        
        # Name and role
        name_label = tk.Label(profile_frame, text=data['name'], 
                             font=("Arial", 18, "bold"), bg='#4A90E2', fg='white')
        name_label.pack(pady=(10, 5))
        
        role_label = tk.Label(profile_frame, text=f"({data['role']})", 
                             font=("Arial", 14), bg='#4A90E2', fg='white')
        role_label.pack()
    
    def create_info_section(self, parent):
        """Create information section"""
        info_frame = tk.Frame(parent, bg='#4A90E2')
        info_frame.pack(pady=20, fill='x', padx=20)
        
        # Check-in time
        checkin_time = datetime.datetime.now().strftime("%I:%M:%S %p")
        time_label = tk.Label(info_frame, text=f"Time Check-in: {checkin_time}", 
                             font=("Arial", 14), bg='#4A90E2', fg='white')
        time_label.pack(anchor='w')
        
        # Date
        checkin_date = datetime.datetime.now().strftime("%B %d, %Y")
        date_label = tk.Label(info_frame, text=f"Date: {checkin_date}", 
                             font=("Arial", 14), bg='#4A90E2', fg='white')
        date_label.pack(anchor='w', pady=(5, 0))
    
    def create_compliance_section(self, parent):
        """Create uniform compliance section"""
        compliance_frame = tk.Frame(parent, bg='#4A90E2')
        compliance_frame.pack(pady=20, fill='x', padx=20)
        
        # Compliance status (will be updated by camera detection)
        self.compliance_label = tk.Label(compliance_frame, text="Checking uniform compliance...", 
                                        font=("Arial", 14, "bold"), bg='#4A90E2', fg='white')
        self.compliance_label.pack(anchor='w')
        
        # Detection results
        self.detection_label = tk.Label(compliance_frame, text="", 
                                       font=("Arial", 12), bg='#4A90E2', fg='white')
        self.detection_label.pack(anchor='w', pady=(5, 0))
    
    def load_profile_image_for_person(self, person_data):
        """Load profile image for a specific person (RFID→student# aware)."""
        try:
            return self.load_splash_profile_image(person_data)
        except Exception as e:
            print(f"Error loading profile image: {e}")
            return None

    def load_profile_image(self):
        """Load profile image from appropriate folder using common resolver."""
        try:
            return self.load_splash_profile_image(self.person_data)
        except Exception as e:
            print(f"Error loading profile image: {e}")
            return None

    def load_profile_image_for_compliance(self):
        """Load profile image for compliance person data using common resolver."""
        try:
            return self.load_splash_profile_image(self.compliance_person_data)
        except Exception as e:
            print(f"Error loading profile image for compliance: {e}")
            return None
    
    def initialize_camera(self):
        """Initialize camera and YOLO model"""
        try:
            self.camera_detector = YOLOCameraDetection()
            if not self.camera_detector.load_model():
                print("Warning: Could not load YOLO model")
            if not self.camera_detector.initialize_camera():
                print("Warning: Could not initialize camera")
        except Exception as e:
            print(f"Error initializing camera: {e}")
    
    def start_camera_feed(self):
        """Start the camera feed update loop"""
        self.is_running = True
        self.update_camera_feed()
    
    def update_camera_feed(self):
        """Update camera feed with detection results"""
        if not self.is_running:
            return
        
        try:
            if self.camera_detector and self.camera_detector.cap:
                frame = self.camera_detector.get_frame_with_detection()
                if frame is not None:
                    # Convert frame to PIL Image
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    frame_pil = Image.fromarray(frame_rgb)
                    
                    # Resize to fit the camera frame
                    frame_pil = frame_pil.resize((640, 480), Image.Resampling.LANCZOS)
                    
                    # Convert to PhotoImage
                    self.camera_photo = ImageTk.PhotoImage(frame_pil)
                    
                    # Update camera label
                    self.camera_label.configure(image=self.camera_photo, text="")
                    
                    # Update compliance status based on detections
                    self.update_compliance_status()
            
        except Exception as e:
            print(f"Error updating camera feed: {e}")
        
        # Schedule next update
        if self.is_running:
            self.main_frame.after(33, self.update_camera_feed)  # ~30 FPS
    
    def update_compliance_status(self):
        """Update uniform compliance status based on camera detection"""
        try:
            if self.camera_detector and self.camera_detector.cap:
                frame = self.camera_detector.get_frame_with_detection()
                if frame is not None:
                    if self.camera_detector.model is None:
                        # No YOLO model available - show placeholder
                        self.compliance_label.config(text="⚠ Uniform Detection: Model Not Available", fg='orange')
                        self.detection_label.config(text="Please ensure best.pt model file is present")
                    else:
                        detections = self.camera_detector.detect_objects(frame)
                        
                        if detections:
                            # Check for uniform-related detections
                            uniform_detected = any('uniform' in det['class_name'].lower() for det in detections)
                            if uniform_detected:
                                self.compliance_label.config(text="✓ Uniform Compliance: PASS", fg='green')
                            else:
                                self.compliance_label.config(text="✗ Uniform Compliance: FAIL", fg='red')
                            
                            # Show detection details
                            detection_text = f"Detected: {', '.join([det['class_name'] for det in detections])}"
                            self.detection_label.config(text=detection_text)
                        else:
                            self.compliance_label.config(text="✓ Uniform Detection Active", fg='blue')
                            self.detection_label.config(text="No uniforms detected - checking compliance...")
        except Exception as e:
            print(f"Error updating compliance status: {e}")
    
    def close_splash(self):
        """Close the splash screen and restore original interface"""
        self.is_running = False
        if self.camera_detector:
            self.camera_detector.cleanup()
        
        # Restore the original interface
        self.restore_original_widgets()
        
        # Unbind escape key
        try:
            self.main_frame.master.unbind('<Escape>')
        except:
            pass

class AINiformLogin:
    def __init__(self, root):
        self.root = root
        self.root.title("AI-niform")
        self.root.geometry("1366x768")
        self.root.configure(bg='white')
        
        # Lock resolution to 1366x768
        self.root.resizable(False, False)
        
        # Center the window
        self.center_window()
        
        # Set up window close protocol to handle X button
        self.root.protocol("WM_DELETE_WINDOW", self.on_window_close)
        
        # Initialize processing variables
        self.is_processing = False
        self.current_guard = None
        
        # Initialize main screen process tracking
        self.main_screen_process = None
        
        # Initialize message system
        self.last_response_message = ""
        self.message_reset_after_id = None
        
        # Initialize Special Pass tracking
        self.current_special_pass = None
        self.current_special_pass_id = None
        self.current_check_type = None
        
        # Initialize database manager
        self.db_manager = DatabaseManager()
        
        # Clean up expired Special Passes on startup
        self.db_manager.cleanup_expired_special_passes()
        
        # Create main frame
        self.main_frame = tk.Frame(root, bg='white')
        self.main_frame.pack(expand=True, fill='both')
        
        # Create UI elements
        self.create_logo()
        self.create_login_button()
        self.create_status_bar()
        
        # Start time update
        self.running = True
        self.update_time()
        
        # Track concurrent beep processes to allow overlapping sounds without leaks
        self._beep_processes = []
    
    def play_beep_sound(self):
        """Play a short beep sound when ID is tapped (asynchronous)"""
        try:
            system_name = platform.system()
            if system_name == "Windows":
                # Use asynchronous PlaySound so multiple taps can overlap
                def win_beep_async():
                    try:
                        import winsound
                        winsound.PlaySound("SystemAsterisk", winsound.SND_ALIAS | winsound.SND_ASYNC | winsound.SND_NODEFAULT)
                    except Exception:
                        try:
                            import winsound as _ws
                            _ws.Beep(1000, 120)
                        except Exception:
                            os.system('echo -e "\a"')
                threading.Thread(target=win_beep_async, daemon=True).start()
            elif system_name == "Darwin":  # macOS
                # Launch afplay without waiting; allow multiple concurrent processes
                p = subprocess.Popen([
                    'afplay', '/System/Library/Sounds/Ping.aiff'
                ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                # Track and prune finished processes
                self._beep_processes = [bp for bp in self._beep_processes if bp.poll() is None]
                self._beep_processes.append(p)
                if len(self._beep_processes) > 8:
                    old = self._beep_processes.pop(0)
                    try:
                        if old.poll() is None:
                            old.terminate()
                    except Exception:
                        pass
            else:  # Linux and others
                # Try paplay asynchronously; fallback to system bell if missing
                try:
                    p = subprocess.Popen([
                        'paplay', '/usr/share/sounds/alsa/Front_Left.wav'
                    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    self._beep_processes = [bp for bp in self._beep_processes if bp.poll() is None]
                    self._beep_processes.append(p)
                    if len(self._beep_processes) > 8:
                        old = self._beep_processes.pop(0)
                        try:
                            if old.poll() is None:
                                old.terminate()
                        except Exception:
                            pass
                except FileNotFoundError:
                    os.system('echo -e "\a"')
        except Exception as e:
            # Fallback to system bell
            print(f"Beep sound error: {e}")
            os.system('echo -e "\a"')
    
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_logo(self):
        """Create the AI-niform logo"""
        logo_frame = tk.Frame(self.main_frame, bg='white')
        logo_frame.pack(expand=True)
        
        # Create a frame to hold the logo text
        logo_container = tk.Frame(logo_frame, bg='white')
        logo_container.pack(pady=(100, 20))
        
        # Al- part in light blue
        ai_part = tk.Label(
            logo_container,
            text="Al-",
            font=("Arial", 48, "bold"),
            bg='white',
            fg='#4A90E2'  # Light blue
        )
        ai_part.pack(side='left')
        
        # -niform part in dark gray/black
        niform_part = tk.Label(
            logo_container,
            text="niform",
            font=("Arial", 48, "bold"),
            bg='white',
            fg='#2C3E50'  # Dark gray/black
        )
        niform_part.pack(side='left')
    
    def create_login_button(self):
        """Create the login button with rounded corners"""
        # Create a frame to center the button
        button_frame = tk.Frame(self.main_frame, bg='white')
        button_frame.pack(expand=True)
        
        # Create a canvas for rounded rectangle effect
        self.login_canvas = tk.Canvas(
            button_frame,
            width=234,
            height=43,
            bg='white',
            highlightthickness=0
        )
        self.login_canvas.pack(pady=20)
        
        # Draw filled rectangle (simplified rounded corners)
        self.login_rect = self.login_canvas.create_rectangle(
            0, 0, 234, 43, fill='#42BE40', outline='#42BE40', width=0
        )
        
        # Add text centered on the button
        self.login_text = self.login_canvas.create_text(
            117, 21.5,  # Center of the button (234/2, 43/2)
            text="Log-in",
            font=("Inter", 16, "bold"),
            fill='white',
            anchor='center'
        )
        
        # Bind events to canvas
        self.login_canvas.bind('<Button-1>', self.login_action)
        self.login_canvas.bind('<Enter>', self.on_login_hover_enter)
        self.login_canvas.bind('<Leave>', self.on_login_hover_leave)
        
        # Configure cursor
        self.login_canvas.config(cursor='hand2')
    

    
    def create_status_bar(self):
        """Create the status bar with time, date, and quit"""
        self.status_frame = tk.Frame(self.main_frame, bg='white')
        self.status_frame.pack(side='bottom', fill='x')
        
        # Time section (blue)
        self.time_label = tk.Label(
            self.status_frame,
            text="12:34:56 pm",
            font=("Arial", 12, "bold"),
            bg='#006CB7',  # Blue
            fg='white',
            padx=20,
            pady=10
        )
        self.time_label.pack(side='left', fill='x', expand=True)
        
        # Date section (dark blue)
        self.date_label = tk.Label(
            self.status_frame,
            text="December 7, 2024",
            font=("Arial", 12, "bold"),
            bg='#021C37',  # Dark blue
            fg='white',
            padx=20,
            pady=10
        )
        self.date_label.pack(side='left', fill='x', expand=True)
        
        # Quit section (orange) - using custom button for macOS compatibility
        self.quit_button_frame = tk.Frame(
            self.status_frame,
            bg='#EF5E1D',  # Orange
            relief='flat',
            padx=20,
            pady=10
        )
        self.quit_button_frame.pack(side='left', fill='x', expand=True)
        
        self.quit_button_label = tk.Label(
            self.quit_button_frame,
            text="Quit",
            font=("Arial", 12, "bold"),
            bg='#EF5E1D',  # Orange
            fg='white',
            cursor='hand2'
        )
        self.quit_button_label.pack()
        
        # Bind events to both frame and label
        self.quit_button_frame.bind('<Button-1>', self.quit_application)
        self.quit_button_label.bind('<Button-1>', self.quit_application)
        
        # Add hover effects
        self.quit_button_frame.bind('<Enter>', self.on_quit_hover_enter)
        self.quit_button_frame.bind('<Leave>', self.on_quit_hover_leave)
        self.quit_button_label.bind('<Enter>', self.on_quit_hover_enter)
        self.quit_button_label.bind('<Leave>', self.on_quit_hover_leave)
    
    def update_time(self):
        """Update time and date continuously"""
        if self.running:
            now = datetime.now()
            
            # Update time
            time_str = now.strftime("%I:%M:%S %p")
            if hasattr(self, 'time_label') and self.time_label.winfo_exists():
                self.time_label.config(text=time_str)
            
            # Update date
            date_str = now.strftime("%B %d, %Y")
            if hasattr(self, 'date_label') and self.date_label.winfo_exists():
                self.date_label.config(text=date_str)
            
            # Schedule next update in 1 second
            self.root.after(1000, self.update_time)
    
    def login_action(self, event=None):
        """Handle login button click"""
        print("Login button clicked!")
        # Clear the main frame and show turnstile interface
        self.show_turnstile_interface()
    
    def show_turnstile_interface(self):
        """Show the turnstile system interface"""
        # Clear the main frame but keep status bar
        for widget in self.main_frame.winfo_children():
            if widget != self.status_frame:
                widget.destroy()
        
        # Create turnstile interface
        self.create_turnstile_header()
        self.create_turnstile_main_content()
        self.create_turnstile_sidebar()
        self.update_status_bar_for_turnstile()
    
    def create_turnstile_header(self):
        """Create the header with red and blue banners"""
        # Create top frame to hold both banners
        top_frame = tk.Frame(self.main_frame, bg='white', height=100)
        top_frame.pack(side='top', fill='x')
        top_frame.pack_propagate(False)
        
        # Red banner at top left (spans horizontally)
        red_banner = tk.Frame(top_frame, bg='#EA234C', height=100)
        red_banner.pack(side='left', fill='both', expand=True)
        red_banner.pack_propagate(False)
        
        turnstile_label = tk.Label(
            red_banner,
            text="Turnstile is Closed",
            font=("Arial", 16, "bold"),
            bg='#EA234C',
            fg='white'
        )
        turnstile_label.pack(expand=True)
        
        # Blue banner at top right (will extend down to form sidebar)
        blue_banner = tk.Frame(top_frame, bg='#4A90E2', height=100, width=300)
        blue_banner.pack(side='right', fill='y')
        blue_banner.pack_propagate(False)
        
        # Load and display STI BALAGTAS logo
        try:
            logo_path = os.path.join("image-elements", "STI Balagtas Logo.png")
            logo_image = Image.open(logo_path)
            # Resize logo to larger dimensions
            logo_image = logo_image.resize((120, 90), Image.Resampling.LANCZOS)
            self.logo_photo = ImageTk.PhotoImage(logo_image)
            
            logo_label = tk.Label(
                blue_banner,
                image=self.logo_photo,
                bg='#4A90E2'
            )
            logo_label.pack(expand=True, pady=5)
        except Exception as e:
            print(f"Error loading logo: {e}")
            # Fallback to text if image fails to load
            sti_frame = tk.Frame(blue_banner, bg='#4A90E2')
            sti_frame.pack(expand=True, pady=10)
            
            sti_label = tk.Label(
                sti_frame,
                text="STI",
                font=("Arial", 20, "bold"),
                bg='#4A90E2',
                fg='#FFD700'  # Yellow
            )
            sti_label.pack()
            
            balagtas_label = tk.Label(
                sti_frame,
                text="BALAGTAS",
                font=("Arial", 12, "bold"),
                bg='#4A90E2',
                fg='black'
            )
            balagtas_label.pack()
    
    def create_turnstile_main_content(self):
        """Create the main content area with AI-niform logo"""
        # Main content frame (white background)
        content_frame = tk.Frame(self.main_frame, bg='white')
        content_frame.pack(side='left', fill='both', expand=True)
        
        # AI-niform logo (centered in white area)
        logo_frame = tk.Frame(content_frame, bg='white')
        logo_frame.pack(expand=True)
        
        logo_container = tk.Frame(logo_frame, bg='white')
        logo_container.pack(pady=(100, 20))
        
        # AI- part in light blue
        ai_part = tk.Label(
            logo_container,
            text="Al-",
            font=("Arial", 48, "bold"),
            bg='white',
            fg='#4A90E2'  # Light blue
        )
        ai_part.pack(side='left')
        
        # -niform part in dark gray/black
        niform_part = tk.Label(
            logo_container,
            text="niform",
            font=("Arial", 48, "bold"),
            bg='white',
            fg='#2C3E50'  # Dark gray/black
        )
        niform_part.pack(side='left')
    
    def create_turnstile_sidebar(self):
        """Create the right sidebar with card reader instructions"""
        # Blue sidebar (extends from top to bottom)
        sidebar = tk.Frame(self.main_frame, bg='#4A90E2', width=300)
        sidebar.pack(side='right', fill='y')
        sidebar.pack_propagate(False)
        
        # Instructions (left aligned with larger font)
        instructions_frame = tk.Frame(sidebar, bg='#4A90E2')
        instructions_frame.pack(pady=(50, 30), padx=20, anchor='w')
        
        instructions_label1 = tk.Label(
            instructions_frame,
            text="Please tap your ID",
            font=("Arial", 22, "bold"),
            bg='#4A90E2',
            fg='white',
            anchor='w'
        )
        instructions_label1.pack(anchor='w')
        
        instructions_label2 = tk.Label(
            instructions_frame,
            text="to the",
            font=("Arial", 22, "bold"),
            bg='#4A90E2',
            fg='white',
            anchor='w'
        )
        instructions_label2.pack(anchor='w')
        
        instructions_label3 = tk.Label(
            instructions_frame,
            text="Card Reader.",
            font=("Arial", 22, "bold"),
            bg='#4A90E2',
            fg='white',
            anchor='w'
        )
        instructions_label3.pack(anchor='w')
        
        # Guard ID section
        guard_frame = tk.Frame(sidebar, bg='#4A90E2')
        guard_frame.pack(pady=20, padx=20)
        
        guard_label = tk.Label(
            guard_frame,
            text="Guard ID:",
            font=("Arial", 12, "bold"),
            bg='#4A90E2',
            fg='white'
        )
        guard_label.pack(anchor='w')
        
        # Guard ID input field (white with black border)
        self.guard_id_entry = tk.Entry(
            guard_frame,
            font=("Arial", 12),
            width=20,
            relief='solid',
            bd=1,
            bg='white',
            fg='black'
        )
        self.guard_id_entry.pack(pady=(5, 0), fill='x')
        
        # Bind events for automatic RFID processing
        self.guard_id_entry.bind('<KeyRelease>', self.on_rfid_input)
        self.guard_id_entry.bind('<Return>', self.process_card)
        
        # Status message
        self.status_label = tk.Label(
            sidebar,
            text="Ready for card tap...",
            font=("Arial", 12),
            bg='#4A90E2',
            fg='white'
        )
        self.status_label.pack(pady=(30, 0), padx=20)
        
        # Focus on the entry field for immediate card reading
        self.guard_id_entry.focus()
    
    def update_status_bar_for_turnstile(self):
        """Update status bar to show Back button instead of Quit"""
        # Clear existing status bar
        for widget in self.status_frame.winfo_children():
            widget.destroy()
        
        # Time section (dark blue)
        now = datetime.now()
        time_str = now.strftime("%I:%M:%S %p")
        self.time_label = tk.Label(
            self.status_frame,
            text=time_str,
            font=("Arial", 12, "bold"),
            bg='#006CB7',  # Blue
            fg='white',
            padx=20,
            pady=10
        )
        self.time_label.pack(side='left', fill='x', expand=True)
        
        # Date section (very dark blue/black)
        date_str = now.strftime("%B %d, %Y")
        self.date_label = tk.Label(
            self.status_frame,
            text=date_str,
            font=("Arial", 12, "bold"),
            bg='#021C37',  # Dark blue
            fg='white',
            padx=20,
            pady=10
        )
        self.date_label.pack(side='left', fill='x', expand=True)
        
        # Back button (orange)
        back_button_frame = tk.Frame(
            self.status_frame,
            bg='#EF5E1D',  # Orange
            relief='flat',
            padx=20,
            pady=10
        )
        back_button_frame.pack(side='left', fill='x', expand=True)
        
        back_button_label = tk.Label(
            back_button_frame,
            text="Back",
            font=("Arial", 12, "bold"),
            bg='#EF5E1D',  # Orange
            fg='white',
            cursor='hand2'
        )
        back_button_label.pack()
        
        # Bind events to back button
        back_button_frame.bind('<Button-1>', self.back_to_login)
        back_button_label.bind('<Button-1>', self.back_to_login)
        
        # Add hover effects
        back_button_frame.bind('<Enter>', self.on_back_hover_enter)
        back_button_frame.bind('<Leave>', self.on_back_hover_leave)
        back_button_label.bind('<Enter>', self.on_back_hover_enter)
        back_button_label.bind('<Leave>', self.on_back_hover_leave)
    
    def back_to_login(self, event=None):
        """Return to login screen"""
        # Clear the main frame but keep status bar
        for widget in self.main_frame.winfo_children():
            if widget != self.status_frame:
                widget.destroy()
        
        # Recreate login interface
        self.create_logo()
        self.create_login_button()
        
        # Restore original status bar
        self.update_status_bar_for_login()
    
    def update_status_bar_for_login(self):
        """Restore original status bar with Quit button"""
        # Clear existing status bar
        for widget in self.status_frame.winfo_children():
            widget.destroy()
        
        # Time section (blue)
        now = datetime.now()
        time_str = now.strftime("%I:%M:%S %p")
        self.time_label = tk.Label(
            self.status_frame,
            text=time_str,
            font=("Arial", 12, "bold"),
            bg='#006CB7',  # Blue
            fg='white',
            padx=20,
            pady=10
        )
        self.time_label.pack(side='left', fill='x', expand=True)
        
        # Date section (dark blue)
        date_str = now.strftime("%B %d, %Y")
        self.date_label = tk.Label(
            self.status_frame,
            text=date_str,
            font=("Arial", 12, "bold"),
            bg='#021C37',  # Dark blue
            fg='white',
            padx=20,
            pady=10
        )
        self.date_label.pack(side='left', fill='x', expand=True)
        
        # Quit section (orange) - using custom button for macOS compatibility
        self.quit_button_frame = tk.Frame(
            self.status_frame,
            bg='#EF5E1D',  # Orange
            relief='flat',
            padx=20,
            pady=10
        )
        self.quit_button_frame.pack(side='left', fill='x', expand=True)
        
        self.quit_button_label = tk.Label(
            self.quit_button_frame,
            text="Quit",
            font=("Arial", 12, "bold"),
            bg='#EF5E1D',  # Orange
            fg='white',
            cursor='hand2'
        )
        self.quit_button_label.pack()
        
        # Bind events to both frame and label
        self.quit_button_frame.bind('<Button-1>', self.quit_application)
        self.quit_button_label.bind('<Button-1>', self.quit_application)
        
        # Add hover effects
        self.quit_button_frame.bind('<Enter>', self.on_quit_hover_enter)
        self.quit_button_frame.bind('<Leave>', self.on_quit_hover_leave)
        self.quit_button_label.bind('<Enter>', self.on_quit_hover_enter)
        self.quit_button_label.bind('<Leave>', self.on_quit_hover_leave)
    
    def on_back_hover_enter(self, event):
        """Handle back button hover enter"""
        # Only change the button frame and label colors, not the parent
        if hasattr(event.widget, 'master') and event.widget.master:
            # If the event is on the label, change both frame and label
            if isinstance(event.widget, tk.Label):
                event.widget.master.config(bg='#D64A1A')
                event.widget.config(bg='#D64A1A')
            # If the event is on the frame, change both frame and its label
            elif isinstance(event.widget, tk.Frame):
                event.widget.config(bg='#D64A1A')
                for child in event.widget.winfo_children():
                    if isinstance(child, tk.Label):
                        child.config(bg='#D64A1A')
    
    def on_back_hover_leave(self, event):
        """Handle back button hover leave"""
        # Only change the button frame and label colors, not the parent
        if hasattr(event.widget, 'master') and event.widget.master:
            # If the event is on the label, change both frame and label
            if isinstance(event.widget, tk.Label):
                event.widget.master.config(bg='#EF5E1D')
                event.widget.config(bg='#EF5E1D')
            # If the event is on the frame, change both frame and its label
            elif isinstance(event.widget, tk.Frame):
                event.widget.config(bg='#EF5E1D')
                for child in event.widget.winfo_children():
                    if isinstance(child, tk.Label):
                        child.config(bg='#EF5E1D')
    
    def on_login_hover_enter(self, event):
        """Handle login button hover enter"""
        self.login_canvas.itemconfig(self.login_rect, fill='#3AA83A', outline='#3AA83A')
    
    def on_login_hover_leave(self, event):
        """Handle login button hover leave"""
        self.login_canvas.itemconfig(self.login_rect, fill='#42BE40', outline='#42BE40')
    
    def quit_application(self, event=None):
        """Quit the application"""
        self.running = False
        # Close the main screen window if it exists
        self.close_main_screen_window()
        self.root.quit()
    
    def on_quit_hover_enter(self, event):
        """Handle quit button hover enter"""
        self.quit_button_frame.config(bg='#D64A1A')
        self.quit_button_label.config(bg='#D64A1A')
    
    def on_quit_hover_leave(self, event):
        """Handle quit button hover leave"""
        self.quit_button_frame.config(bg='#EF5E1D')
        self.quit_button_label.config(bg='#EF5E1D')
    
    def on_rfid_input(self, event=None):
        """Handle automatic RFID keyboard input"""
        if self.is_processing:
            return  # Prevent duplicate processing
        
        card_id = self.guard_id_entry.get().strip()
        
        # Check if we have a complete RFID code (typically 10 digits)
        if len(card_id) >= 10:
            # Play beep sound when ID is tapped
            self.play_beep_sound()
            
            self.is_processing = True
            # Update status
            self.status_label.config(text="Processing card...")
            self.root.update()
            
            # Process the card after a short delay to ensure complete input
            self.root.after(100, self.process_card)
    
    def process_card(self, event=None):
        """Process the card tap"""
        if not self.is_processing:
            return  # Prevent duplicate processing from Enter key
        
        card_id = self.guard_id_entry.get().strip()
        
        if not card_id:
            self.is_processing = False
            return
        
        # Update status
        self.status_label.config(text="Validating access...")
        self.root.update()
        
        # Log the access attempt
        self.db_manager.log_access(card_id, "GUARD_LOGIN")
        
        # Find the person in database
        person = self.db_manager.find_person(card_id)
        
        if person:
            if person['role'] == 'GUARD':
                # Store current guard information
                self.current_guard = person
                # Guard access granted
                self.status_label.config(text="ACCESS GRANTED", fg='green')
                # Clear the input field
                self.guard_id_entry.delete(0, tk.END)
                # Show guard interface with main screen after 3 seconds
                self.root.after(3000, self.show_guard_interface)
            else:
                # Non-guard access denied (including teachers and students)
                self.status_label.config(text="ACCESS DENIED", fg='red')
                # Clear the input field
                self.guard_id_entry.delete(0, tk.END)
                # Reset status after delay
                self.root.after(3000, self.reset_status)
        else:
            # Person not found in database
            self.status_label.config(text="ACCESS DENIED", fg='red')
            # Clear the input field
            self.guard_id_entry.delete(0, tk.END)
            # Reset status after delay
            self.root.after(3000, self.reset_status)
        
        # Refocus the entry field for next card
        self.guard_id_entry.focus()
    
    def reset_status(self):
        """Reset the status and processing flag"""
        self.status_label.config(text="Ready for card tap...", fg='white')
        self.is_processing = False
    
    def show_guard_interface(self):
        """Show the guard interface and launch main screen in separate window"""
        # Clear the main frame but keep status bar
        for widget in self.main_frame.winfo_children():
            if widget != self.status_frame:
                widget.destroy()
        
        # Create the original guard interface
        self.create_guard_header()
        self.create_guard_main_content()
        self.create_guard_sidebar()
        self.update_status_bar_for_guard()
        
        # Clear any old status from main screen status file to prevent showing old status
        try:
            with open("main_screen_status.txt", "w") as f:
                f.write("RESET_TO_DEFAULT\n")
                f.write("N/A\n")
                f.write("N/A\n")
                f.write("N/A\n")
            print("Cleared main screen status file on guard interface launch")
        except Exception as e:
            print(f"Error clearing main screen status file: {e}")
        
        # Only launch the PyQt5 main screen if it's not already running
        should_launch = (not hasattr(self, 'main_screen_process') or 
                        self.main_screen_process is None or 
                        self.main_screen_process.poll() is not None)
        
        print(f"Main screen process check: hasattr={hasattr(self, 'main_screen_process')}, "
              f"is_none={getattr(self, 'main_screen_process', None) is None}, "
              f"poll_result={getattr(self.main_screen_process, 'poll', lambda: None)() if hasattr(self, 'main_screen_process') and self.main_screen_process else 'N/A'}, "
              f"should_launch={should_launch}")
        
        if should_launch:
            self.launch_main_screen_window()
        
        # Start checking for main screen status
        self.root.after(2000, self.check_main_screen_status)
        
        # Ensure focus is set after interface is created
        self.root.after(100, self.focus_guard_entry)
    
    def show_guard_interface_without_main_screen(self):
        """Show the guard interface without launching main screen (for back navigation)"""
        # Clear the main frame but keep status bar
        for widget in self.main_frame.winfo_children():
            if widget != self.status_frame:
                widget.destroy()
        
        # Create the original guard interface
        self.create_guard_header()
        self.create_guard_main_content()
        self.create_guard_sidebar()
        self.update_status_bar_for_guard()
        
        # Don't launch the main screen - just return to guard interface
        # Ensure focus is set after interface is created
        self.root.after(100, self.focus_guard_entry)
    
    def launch_main_screen_window(self):
        """Launch the PyQt5 main screen in a separate window"""
        # For better compatibility, always launch as separate process
        self.launch_main_screen_as_process()
    
    def launch_main_screen_as_process(self):
        """Launch main screen as separate process if PyQt5 integration fails"""
        try:
            # Get the current directory and path to testmainscreen.py
            current_dir = os.path.dirname(os.path.abspath(__file__))
            main_screen_path = os.path.join(current_dir, "testmainscreen.py")
            
            # Launch the PyQt5 application as separate process
            self.main_screen_process = subprocess.Popen([sys.executable, main_screen_path])
            print("Main screen launched as separate process")
            
        except Exception as e:
            print(f"Error launching main screen as process: {e}")
            # Set to None if launch failed
            self.main_screen_process = None
    
    def cleanup_main_screen_process(self):
        """Clean up the main screen process if it exists"""
        if hasattr(self, 'main_screen_process') and self.main_screen_process is not None:
            try:
                if self.main_screen_process.poll() is None:  # Process is still running
                    self.main_screen_process.terminate()
                    self.main_screen_process.wait(timeout=5)  # Wait up to 5 seconds
                self.main_screen_process = None
                print("Main screen process cleaned up")
            except Exception as e:
                print(f"Error cleaning up main screen process: {e}")
                self.main_screen_process = None
        else:
            # Ensure it's set to None even if it doesn't exist
            self.main_screen_process = None
            print("Main screen process reference cleared")
    def focus_guard_entry(self):
        """Focus the guard ID entry field"""
        if hasattr(self, 'guard_id_entry') and self.guard_id_entry.winfo_exists():
            self.guard_id_entry.focus()
            self.guard_id_entry.select_range(0, tk.END)  # Select all text if any
    
    def create_guard_header(self):
        """Create the header with red and blue banners"""
        # Create top frame to hold both banners
        top_frame = tk.Frame(self.main_frame, bg='white', height=100)
        top_frame.pack(side='top', fill='x')
        top_frame.pack_propagate(False)
        
        # Red banner at top left (spans horizontally)
        red_banner = tk.Frame(top_frame, bg='#EA234C', height=100)
        red_banner.pack(side='left', fill='both', expand=True)
        red_banner.pack_propagate(False)
        
        turnstile_label = tk.Label(
            red_banner,
            text="Turnstile is Closed",
            font=("Arial", 16, "bold"),
            bg='#EA234C',
            fg='white'
        )
        turnstile_label.pack(expand=True)
        
        # Blue banner at top right (will extend down to form sidebar)
        blue_banner = tk.Frame(top_frame, bg='#4A90E2', height=100, width=300)
        blue_banner.pack(side='right', fill='y')
        blue_banner.pack_propagate(False)
        
        # Load and display STI BALAGTAS logo
        try:
            logo_path = os.path.join("image-elements", "STI Balagtas Logo.png")
            logo_image = Image.open(logo_path)
            # Resize logo to larger dimensions
            logo_image = logo_image.resize((120, 90), Image.Resampling.LANCZOS)
            self.logo_photo = ImageTk.PhotoImage(logo_image)
            
            logo_label = tk.Label(
                blue_banner,
                image=self.logo_photo,
                bg='#4A90E2'
            )
            logo_label.pack(expand=True, pady=5)
        except Exception as e:
            print(f"Error loading logo: {e}")
            # Fallback to text if image fails to load
            sti_frame = tk.Frame(blue_banner, bg='#4A90E2')
            sti_frame.pack(expand=True, pady=10)
            
            sti_label = tk.Label(
                sti_frame,
                text="STI",
                font=("Arial", 20, "bold"),
                bg='#4A90E2',
                fg='#FFD700'  # Yellow
            )
            sti_label.pack()
            
            balagtas_label = tk.Label(
                sti_frame,
                text="BALAGTAS",
                font=("Arial", 12, "bold"),
                bg='#4A90E2',
                fg='black'
            )
            balagtas_label.pack()
    
    def create_guard_main_content(self):
        """Create the main content area with AI-niform logo"""
        # Main content frame (white background)
        content_frame = tk.Frame(self.main_frame, bg='white')
        content_frame.pack(side='left', fill='both', expand=True)
        
        # AI-niform logo (centered in white area)
        logo_frame = tk.Frame(content_frame, bg='white')
        logo_frame.pack(expand=True)
        
        logo_container = tk.Frame(logo_frame, bg='white')
        logo_container.pack(pady=(100, 20))
        
        # Al- part in light blue
        ai_part = tk.Label(
            logo_container,
            text="Al-",
            font=("Arial", 48, "bold"),
            bg='white',
            fg='#4A90E2'  # Light blue
        )
        ai_part.pack(side='left')
        
        # -niform part in dark gray/black
        niform_part = tk.Label(
            logo_container,
            text="niform",
            font=("Arial", 48, "bold"),
            bg='white',
            fg='#2C3E50'  # Dark gray/black
        )
        niform_part.pack(side='left')
    
    def create_guard_sidebar(self):
        """Create the right sidebar with visitor/student buttons and ID input"""
        # Blue sidebar (extends from top to bottom)
        sidebar = tk.Frame(self.main_frame, bg='#4A90E2', width=300)
        sidebar.pack(side='right', fill='y')
        sidebar.pack_propagate(False)
        
        # Content frame for sidebar
        content_frame = tk.Frame(sidebar, bg='#4A90E2')
        content_frame.pack(expand=True, padx=20, pady=40)
        
        
        # Message area (shows last response or default text)
        message_text = self.last_response_message if self.last_response_message else "Awaiting ID card scan."
        self.guard_message_label = tk.Label(
            content_frame,
            text=message_text,
            font=("Arial", 18, "bold"),
            bg='#4A90E2',
            fg='white',
            wraplength=250,
            justify='center'
        )
        self.guard_message_label.pack(pady=(0, 40))
        
        # Button container for consistent alignment
        button_container = tk.Frame(content_frame, bg='#4A90E2')
        button_container.pack(fill='x', pady=(0, 40))
        
        # Visitor button
        visitor_button = tk.Button(
            button_container,
            text="Visitor",
            font=("Arial", 16, "bold"),
            bg='#d3d3d3',  # Light grey
            fg='black',
            relief='flat',
            cursor='hand2',
            command=self.visitor_action,
            width=18,
            height=2
        )
        visitor_button.pack(pady=(0, 15))
        
        # Student button
        student_button = tk.Button(
            button_container,
            text="Student",
            font=("Arial", 16, "bold"),
            bg='#d3d3d3',  # Light grey
            fg='black',
            relief='flat',
            cursor='hand2',
            command=self.student_action,
            width=18,
            height=2
        )
        student_button.pack()
        
        # ID Number section
        id_frame = tk.Frame(content_frame, bg='#4A90E2')
        id_frame.pack(fill='x', pady=(0, 40))
        
        id_label = tk.Label(
            id_frame,
            text="ID Number:",
            font=("Arial", 14, "bold"),
            bg='#4A90E2',
            fg='white'
        )
        id_label.pack(pady=(0, 10))
        
        # ID Number input field
        self.id_number_entry = tk.Entry(
            id_frame,
            font=("Arial", 14),
            width=20,
            relief='solid',
            bd=2,
            bg='white',
            fg='black',
            justify='center'
        )
        self.id_number_entry.pack(pady=(0, 20))
        
        # Bind events for automatic RFID processing
        self.id_number_entry.bind('<KeyRelease>', self.on_guard_rfid_input)
        self.id_number_entry.bind('<Return>', self.process_guard_card)
        
        # Focus on the entry field for immediate RFID input
        self.id_number_entry.focus()
        
        # Guard information
        guard_info_frame = tk.Frame(content_frame, bg='#4A90E2')
        guard_info_frame.pack(fill='x')
        
        guard_label = tk.Label(
            guard_info_frame,
            text="Guard in-charge:",
            font=("Arial", 14, "bold"),
            bg='#4A90E2',
            fg='white'
        )
        guard_label.pack(pady=(0, 5))
        
        # Get guard name from stored information or use default
        guard_name = self.current_guard['name'] if self.current_guard else "Unknown Guard"
        
        guard_name_label = tk.Label(
            guard_info_frame,
            text=guard_name,
            font=("Arial", 14),
            bg='#4A90E2',
            fg='white'
        )
        guard_name_label.pack()
    
    def update_status_bar_for_guard(self):
        """Update status bar to show Log out button"""
        # Clear existing status bar
        for widget in self.status_frame.winfo_children():
            widget.destroy()
        
        # Time section (dark blue)
        now = datetime.now()
        time_str = now.strftime("%I:%M:%S %p")
        self.time_label = tk.Label(
            self.status_frame,
            text=time_str,
            font=("Arial", 12, "bold"),
            bg='#006CB7',  # Blue
            fg='white',
            padx=20,
            pady=10
        )
        self.time_label.pack(side='left', fill='x', expand=True)
        
        # Date section (very dark blue/black)
        date_str = now.strftime("%B %d, %Y")
        self.date_label = tk.Label(
            self.status_frame,
            text=date_str,
            font=("Arial", 12, "bold"),
            bg='#021C37',  # Dark blue
            fg='white',
            padx=20,
            pady=10
        )
        self.date_label.pack(side='left', fill='x', expand=True)
        
        # Log out button (orange)
        logout_button_frame = tk.Frame(
            self.status_frame,
            bg='#EF5E1D',  # Orange
            relief='flat',
            padx=20,
            pady=10
        )
        logout_button_frame.pack(side='left', fill='x', expand=True)
        
        logout_button_label = tk.Label(
            logout_button_frame,
            text="Log out",
            font=("Arial", 12, "bold"),
            bg='#EF5E1D',  # Orange
            fg='white',
            cursor='hand2'
        )
        logout_button_label.pack()
        
        # Store references to logout button elements for enabling/disabling
        self.logout_button_frame = logout_button_frame
        self.logout_button_label = logout_button_label
        
        # Bind events to logout button
        logout_button_frame.bind('<Button-1>', self.show_logout_confirmation)
        logout_button_label.bind('<Button-1>', self.show_logout_confirmation)
        
        # Add hover effects
        logout_button_frame.bind('<Enter>', self.on_logout_hover_enter)
        logout_button_frame.bind('<Leave>', self.on_logout_hover_leave)
        logout_button_label.bind('<Enter>', self.on_logout_hover_enter)
        logout_button_label.bind('<Leave>', self.on_logout_hover_leave)
    
    def visitor_action(self):
        """Handle visitor button click"""
        print("Visitor button clicked!")
        # Show visitor form interface
        self.show_visitor_form_interface()
    
    def student_action(self):
        """Handle student button click"""
        print("Student button clicked!")
        # Show student interface
        self.show_student_interface()
    
    def show_logout_confirmation(self, event=None):
        """Show logout confirmation dialog with card tap"""
        # Create a new top-level window for logout confirmation
        self.logout_window = tk.Toplevel(self.root)
        self.logout_window.title("Logout Confirmation")
        self.logout_window.geometry("400x300")
        self.logout_window.configure(bg='white')
        self.logout_window.resizable(False, False)
        
        # Center the window
        self.logout_window.transient(self.root)
        self.logout_window.grab_set()
        
        # Create content
        title_label = tk.Label(
            self.logout_window,
            text="Logout Confirmation",
            font=("Arial", 18, "bold"),
            bg='white',
            fg='#333333'
        )
        title_label.pack(pady=(30, 20))
        
        message_label = tk.Label(
            self.logout_window,
            text="Please tap your card to confirm logout:",
            font=("Arial", 12),
            bg='white',
            fg='#333333'
        )
        message_label.pack(pady=(0, 20))
        
        # Card input field
        self.logout_card_entry = tk.Entry(
            self.logout_window,
            font=("Arial", 14),
            width=25,
            relief='solid',
            bd=1,
            bg='white',
            fg='black',
            show='*'  # Hide input for security
        )
        self.logout_card_entry.pack(pady=(0, 20))
        self.logout_card_entry.focus()
        
        # Bind events for logout card processing
        self.logout_card_entry.bind('<KeyRelease>', self.on_logout_rfid_input)
        self.logout_card_entry.bind('<Return>', self.process_logout_card)
        
        # Cancel button
        cancel_button = tk.Button(
            self.logout_window,
            text="Cancel",
            font=("Arial", 12),
            bg='#6c757d',
            fg='white',
            relief='flat',
            cursor='hand2',
            command=self.cancel_logout
        )
        cancel_button.pack(pady=(0, 20))
    
    def on_logout_rfid_input(self, event=None):
        """Handle logout RFID input"""
        card_id = self.logout_card_entry.get().strip()
        
        # Check if we have a complete RFID code (typically 10 digits)
        if len(card_id) >= 10:
            # Play beep sound when ID is tapped
            self.play_beep_sound()
            
            # Process the logout card
            self.process_logout_card()
    
    def process_logout_card(self, event=None):
        """Process logout card tap"""
        card_id = self.logout_card_entry.get().strip()
        
        if not card_id:
            return
        
        # Check if the card matches the currently logged-in guard
        if self.current_guard and card_id == self.current_guard['id']:
            # Card matches - allow logout
            # Close logout window
            self.logout_window.destroy()
            
            # Close the main screen window if it exists
            self.close_main_screen_window()
            
            # Log the logout
            self.db_manager.log_access(card_id, "GUARD_LOGOUT")
            
            # Clear current guard
            self.current_guard = None
            
            # Return to login screen
            self.back_to_login()
        else:
            # Card doesn't match - show error
            messagebox.showerror("Logout Error", "Card does not match the currently in-duty guard.\nPlease use the same card that was used for login.")
            # Clear the input field
            self.logout_card_entry.delete(0, tk.END)
            # Refocus the entry field
            self.logout_card_entry.focus()
    
    def close_main_screen_window(self):
        """Close the main screen window if it exists"""
        self.cleanup_main_screen_process()
    
    def on_main_screen_closed(self):
        """Handle when main screen window is closed by user"""
        if hasattr(self, 'main_screen_process'):
            self.main_screen_process = None
        print("Main screen window was closed by user")
        
        # Relaunch the main screen if guard screen is still running
        if self.running and hasattr(self, 'current_guard') and self.current_guard:
            print("Relaunching main screen...")
            self.launch_main_screen_window()
    
    def on_window_close(self):
        """Handle when guard screen window is closed (X button)"""
        # Close the main screen window if it exists
        self.close_main_screen_window()
        # Close the guard screen
        self.root.destroy()
    
    def check_main_screen_status(self):
        """Check if main screen has been closed and relaunch if needed"""
        if not self.running or not hasattr(self, 'current_guard') or not self.current_guard:
            return
        
        try:
            if os.path.exists("main_screen_status.txt"):
                with open("main_screen_status.txt", 'r') as f:
                    lines = f.readlines()
                    if lines and lines[0].strip() == "MAIN_SCREEN_CLOSED":
                        print("Detected main screen was closed - relaunching...")
                        # Clear the status file
                        with open("main_screen_status.txt", "w") as f:
                            f.write("RESET_TO_DEFAULT\n")
                            f.write("N/A\n")
                            f.write("N/A\n")
                            f.write("N/A\n")
                        # Relaunch the main screen
                        self.launch_main_screen_window()
        except Exception as e:
            print(f"Error checking main screen status: {e}")
        
        # Schedule next check in 2 seconds
        if self.running:
            self.root.after(2000, self.check_main_screen_status)
    
    def cancel_logout(self):
        """Cancel logout and close window"""
        self.logout_window.destroy()
        # Note: Main screen window remains open when logout is cancelled
    
    def on_logout_hover_enter(self, event):
        """Handle logout button hover enter"""
        # Only change the button frame and label colors, not the parent
        if hasattr(event.widget, 'master') and event.widget.master:
            # If the event is on the label, change both frame and label
            if isinstance(event.widget, tk.Label):
                event.widget.master.config(bg='#D64A1A')
                event.widget.config(bg='#D64A1A')
            # If the event is on the frame, change both frame and its label
            elif isinstance(event.widget, tk.Frame):
                event.widget.config(bg='#D64A1A')
                for child in event.widget.winfo_children():
                    if isinstance(child, tk.Label):
                        child.config(bg='#D64A1A')
    
    def on_logout_hover_leave(self, event):
        """Handle logout button hover leave"""
        # Only change the button frame and label colors, not the parent
        if hasattr(event.widget, 'master') and event.widget.master:
            # If the event is on the label, change both frame and label
            if isinstance(event.widget, tk.Label):
                event.widget.master.config(bg='#EF5E1D')
                event.widget.config(bg='#EF5E1D')
            # If the event is on the frame, change both frame and its label
            elif isinstance(event.widget, tk.Frame):
                event.widget.config(bg='#EF5E1D')
                for child in event.widget.winfo_children():
                    if isinstance(child, tk.Label):
                        child.config(bg='#EF5E1D')
    
    def disable_logout_button(self):
        """Disable the logout button (gray it out)"""
        if (hasattr(self, 'logout_button_frame') and hasattr(self, 'logout_button_label') and
            self.logout_button_frame.winfo_exists() and self.logout_button_label.winfo_exists()):
            try:
                # Gray out the button
                self.logout_button_frame.configure(bg='#CCCCCC')  # Gray
                self.logout_button_label.configure(bg='#CCCCCC', fg='#999999')  # Gray text
                
                # Unbind click events
                self.logout_button_frame.unbind('<Button-1>')
                self.logout_button_label.unbind('<Button-1>')
                
                # Change cursor to indicate disabled state
                self.logout_button_frame.configure(cursor='arrow')
                self.logout_button_label.configure(cursor='arrow')
            except tk.TclError:
                # Widget was destroyed, ignore the error
                pass
    
    def enable_logout_button(self):
        """Enable the logout button (restore normal appearance)"""
        if (hasattr(self, 'logout_button_frame') and hasattr(self, 'logout_button_label') and
            self.logout_button_frame.winfo_exists() and self.logout_button_label.winfo_exists()):
            try:
                # Restore normal colors
                self.logout_button_frame.configure(bg='#EF5E1D')  # Orange
                self.logout_button_label.configure(bg='#EF5E1D', fg='white')  # Orange with white text
                
                # Rebind click events
                self.logout_button_frame.bind('<Button-1>', self.show_logout_confirmation)
                self.logout_button_label.bind('<Button-1>', self.show_logout_confirmation)
                
                # Restore hover cursor
                self.logout_button_frame.configure(cursor='hand2')
                self.logout_button_label.configure(cursor='hand2')
            except tk.TclError:
                # Widget was destroyed, ignore the error
                pass
    
    def show_visitor_form_interface(self):
        """Show the visitor form interface"""
        # Clear the main frame but keep status bar
        for widget in self.main_frame.winfo_children():
            if widget != self.status_frame:
                widget.destroy()
        
        # Create visitor form interface
        self.create_visitor_form_header()
        self.create_visitor_form_content()
        self.create_visitor_form_sidebar()
        self.update_status_bar_for_visitor_form()
        
        # Ensure focus is set after interface is created
        self.root.after(100, self.focus_visitor_entry)
    
    def focus_visitor_entry(self):
        """Focus the visitor ID entry field"""
        if hasattr(self, 'visitor_id_number_entry') and self.visitor_id_number_entry.winfo_exists():
            self.visitor_id_number_entry.focus()
            self.visitor_id_number_entry.select_range(0, tk.END)  # Select all text if any
    
    def create_visitor_form_header(self):
        """Create the header with red and blue banners"""
        # Create top frame to hold both banners
        top_frame = tk.Frame(self.main_frame, bg='white', height=100)
        top_frame.pack(side='top', fill='x')
        top_frame.pack_propagate(False)
        
        # Red banner at top left (spans horizontally)
        red_banner = tk.Frame(top_frame, bg='#EA234C', height=100)
        red_banner.pack(side='left', fill='both', expand=True)
        red_banner.pack_propagate(False)
        
        turnstile_label = tk.Label(
            red_banner,
            text="Turnstile is Closed",
            font=("Arial", 16, "bold"),
            bg='#EA234C',
            fg='white'
        )
        turnstile_label.pack(expand=True)
        
        # Blue banner at top right (will extend down to form sidebar)
        blue_banner = tk.Frame(top_frame, bg='#4A90E2', height=100, width=300)
        blue_banner.pack(side='right', fill='y')
        blue_banner.pack_propagate(False)
        
        # Load and display STI BALAGTAS logo
        try:
            logo_path = os.path.join("image-elements", "STI Balagtas Logo.png")
            logo_image = Image.open(logo_path)
            # Resize logo to larger dimensions
            logo_image = logo_image.resize((120, 90), Image.Resampling.LANCZOS)
            self.logo_photo = ImageTk.PhotoImage(logo_image)
            
            logo_label = tk.Label(
                blue_banner,
                image=self.logo_photo,
                bg='#4A90E2'
            )
            logo_label.pack(expand=True, pady=5)
        except Exception as e:
            print(f"Error loading logo: {e}")
            # Fallback to text if image fails to load
            sti_frame = tk.Frame(blue_banner, bg='#4A90E2')
            sti_frame.pack(expand=True, pady=10)
            
            sti_label = tk.Label(
                sti_frame,
                text="STI",
                font=("Arial", 20, "bold"),
                bg='#4A90E2',
                fg='#FFD700'  # Yellow
            )
            sti_label.pack()
            
            balagtas_label = tk.Label(
                sti_frame,
                text="BALAGTAS",
                font=("Arial", 12, "bold"),
                bg='#4A90E2',
                fg='black'
            )
            balagtas_label.pack()
    
    def create_visitor_form_content(self):
        """Create the visitor form content"""
        # Main content frame (white background)
        content_frame = tk.Frame(self.main_frame, bg='white')
        content_frame.pack(side='left', fill='both', expand=True)
        
        # Create a canvas with scrollbar for the form
        canvas = tk.Canvas(content_frame, bg='white', highlightthickness=0)
        scrollbar = ttk.Scrollbar(content_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='white')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Bind mouse wheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Unbind mouse wheel when leaving the canvas
        def _on_leave(event):
            canvas.unbind_all("<MouseWheel>")
        
        def _on_enter(event):
            canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        canvas.bind("<Enter>", _on_enter)
        canvas.bind("<Leave>", _on_leave)
        
        # Form container
        form_container = tk.Frame(scrollable_frame, bg='white')
        form_container.pack(expand=True, padx=50, pady=30)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Form title
        title_label = tk.Label(
            form_container,
            text="Visitor Registration Form",
            font=("Arial", 20, "bold"),
            fg='black',
            bg='white'
        )
        title_label.pack(pady=(0, 30))
        
        # Initialize form variables
        self.visitor_name_var = tk.StringVar()
        self.visitor_contact_var = tk.StringVar()
        self.visitor_type_var = tk.StringVar()
        self.visitor_purpose_var = tk.StringVar()
        self.visitor_visiting_var = tk.StringVar()
        self.visitor_id_type_var = tk.StringVar()
        self.visitor_special_pass_var = tk.StringVar()
        
        # Full Name
        name_label = tk.Label(form_container, text="Full Name:", font=("Arial", 12, "bold"), fg='black', bg='white')
        name_label.pack(anchor='w', pady=(0, 5))
        name_entry = tk.Entry(form_container, textvariable=self.visitor_name_var, font=("Arial", 12), 
                             width=40, relief='solid', bd=1, bg='#f0f0f0')
        name_entry.pack(fill='x', pady=(0, 15))
        
        # Contact Number
        contact_label = tk.Label(form_container, text="Contact Number:", font=("Arial", 12, "bold"), fg='black', bg='white')
        contact_label.pack(anchor='w', pady=(0, 5))
        contact_entry = tk.Entry(form_container, textvariable=self.visitor_contact_var, font=("Arial", 12), 
                                width=40, relief='solid', bd=1, bg='#f0f0f0')
        contact_entry.pack(fill='x', pady=(0, 15))
        
        # Visiting as
        visiting_as_label = tk.Label(form_container, text="Visiting as:", font=("Arial", 12, "bold"), fg='black', bg='white')
        visiting_as_label.pack(anchor='w', pady=(0, 5))
        visiting_as_combo = ttk.Combobox(form_container, textvariable=self.visitor_type_var, 
                                        values=["Guest", "Contractor", "Vendor", "Official Visitor", "Other"], 
                                        state="readonly", width=37)
        visiting_as_combo.pack(fill='x', pady=(0, 15))
        
        # Purpose of Visit
        purpose_label = tk.Label(form_container, text="Purpose of Visit:", font=("Arial", 12, "bold"), fg='black', bg='white')
        purpose_label.pack(anchor='w', pady=(0, 5))
        purpose_entry = tk.Entry(form_container, textvariable=self.visitor_purpose_var, font=("Arial", 12), 
                                width=40, relief='solid', bd=1, bg='#f0f0f0')
        purpose_entry.pack(fill='x', pady=(0, 15))
        
        # Who are you visiting
        visiting_label = tk.Label(form_container, text="Who are you visiting?:", font=("Arial", 12, "bold"), fg='black', bg='white')
        visiting_label.pack(anchor='w', pady=(0, 5))
        visiting_entry = tk.Entry(form_container, textvariable=self.visitor_visiting_var, font=("Arial", 12), 
                                 width=40, relief='solid', bd=1, bg='#f0f0f0')
        visiting_entry.pack(fill='x', pady=(0, 15))
        
        # Type of Valid ID
        id_type_label = tk.Label(form_container, text="Type of Valid ID:", font=("Arial", 12, "bold"), fg='black', bg='white')
        id_type_label.pack(anchor='w', pady=(0, 5))
        id_type_combo = ttk.Combobox(form_container, textvariable=self.visitor_id_type_var, 
                                    values=["Driver's License", "Passport", "National ID", "Company ID", "Other"], 
                                    state="readonly", width=37)
        id_type_combo.pack(fill='x', pady=(0, 15))
        
        # Special Pass ID
        special_pass_label = tk.Label(form_container, text="Special Pass ID:", font=("Arial", 12, "bold"), fg='black', bg='white')
        special_pass_label.pack(anchor='w', pady=(0, 5))
        special_pass_entry = tk.Entry(form_container, textvariable=self.visitor_special_pass_var, 
                                     font=("Arial", 12), width=37, relief='solid', bd=1)
        special_pass_entry.pack(fill='x', pady=(0, 40))
        
        # Submit button
        submit_button = tk.Button(
            form_container,
            text="Submit",
            font=("Arial", 14, "bold"),
            bg='#007BFF',  # Blue
            fg='white',
            relief='flat',
            cursor='hand2',
            command=self.submit_visitor_form,
            padx=20,
            pady=10
        )
        submit_button.pack(anchor='e', pady=(0, 20))
    
    def create_visitor_form_sidebar(self):
        """Create the right sidebar for visitor form"""
        # Blue sidebar (extends from top to bottom)
        sidebar = tk.Frame(self.main_frame, bg='#4A90E2', width=300)
        sidebar.pack(side='right', fill='y')
        sidebar.pack_propagate(False)
        
        # Content frame for sidebar
        content_frame = tk.Frame(sidebar, bg='#4A90E2')
        content_frame.pack(expand=True, padx=20, pady=40)
        
        # Instructions
        instructions_label = tk.Label(
            content_frame,
            text="Awaiting ID card scan.",
            font=("Arial", 17, "bold"),
            bg='#4A90E2',
            fg='white'
        )
        instructions_label.pack(anchor='w', pady=(0, 30))
        
        # Visitor button (bright yellow - active)
        visitor_button = tk.Button(
            content_frame,
            text="Visitor",
            font=("Arial", 16, "bold"),
            bg='#FFD700',  # Bright yellow
            fg='black',
            relief='flat',
            cursor='hand2',
            command=self.visitor_action
        )
        visitor_button.pack(fill='x', pady=(0, 10))
        
        # Student button (light grey - inactive)
        student_button = tk.Button(
            content_frame,
            text="Student",
            font=("Arial", 16, "bold"),
            bg='#d3d3d3',  # Light grey
            fg='black',
            relief='flat',
            cursor='hand2',
            command=self.student_action
        )
        student_button.pack(fill='x', pady=(0, 30))
        
        # ID Number section
        id_frame = tk.Frame(content_frame, bg='#4A90E2')
        id_frame.pack(fill='x')
        
        id_label = tk.Label(
            id_frame,
            text="ID Number:",
            font=("Arial", 12, "bold"),
            bg='#4A90E2',
            fg='white'
        )
        id_label.pack(anchor='w')
        
        # ID Number input field
        self.visitor_id_number_entry = tk.Entry(
            id_frame,
            font=("Arial", 12),
            width=20,
            relief='solid',
            bd=1,
            bg='white',
            fg='black'
        )
        self.visitor_id_number_entry.pack(fill='x', pady=(5, 0))
        
        # Bind events for automatic RFID processing
        self.visitor_id_number_entry.bind('<KeyRelease>', self.on_visitor_rfid_input)
        self.visitor_id_number_entry.bind('<Return>', self.process_visitor_card)
        
        # Focus on the entry field for immediate RFID input
        self.visitor_id_number_entry.focus()
        
        # Guard information
        guard_info_frame = tk.Frame(content_frame, bg='#4A90E2')
        guard_info_frame.pack(pady=(30, 0))
        
        guard_label = tk.Label(
            guard_info_frame,
            text="Guard in-charge:",
            font=("Arial", 12, "bold"),
            bg='#4A90E2',
            fg='white'
        )
        guard_label.pack(anchor='w')
        
        # Get guard name from stored information or use default
        guard_name = self.current_guard['name'] if self.current_guard else "Unknown Guard"
        
        guard_name_label = tk.Label(
            guard_info_frame,
            text=guard_name,
            font=("Arial", 12),
            bg='#4A90E2',
            fg='white'
        )
        guard_name_label.pack(anchor='w')
    
    def update_status_bar_for_visitor_form(self):
        """Update status bar to show Back button for visitor form"""
        # Clear existing status bar
        for widget in self.status_frame.winfo_children():
            widget.destroy()
        
        # Time section (dark blue)
        now = datetime.now()
        time_str = now.strftime("%I:%M:%S %p")
        self.time_label = tk.Label(
            self.status_frame,
            text=time_str,
            font=("Arial", 12, "bold"),
            bg='#006CB7',  # Blue
            fg='white',
            padx=20,
            pady=10
        )
        self.time_label.pack(side='left', fill='x', expand=True)
        
        # Date section (very dark blue/black)
        date_str = now.strftime("%B %d, %Y")
        self.date_label = tk.Label(
            self.status_frame,
            text=date_str,
            font=("Arial", 12, "bold"),
            bg='#021C37',  # Dark blue
            fg='white',
            padx=20,
            pady=10
        )
        self.date_label.pack(side='left', fill='x', expand=True)
        
        # Back button (orange)
        back_button_frame = tk.Frame(
            self.status_frame,
            bg='#EF5E1D',  # Orange
            relief='flat',
            padx=20,
            pady=10
        )
        back_button_frame.pack(side='left', fill='x', expand=True)
        
        back_button_label = tk.Label(
            back_button_frame,
            text="Back",
            font=("Arial", 12, "bold"),
            bg='#EF5E1D',  # Orange
            fg='white',
            cursor='hand2'
        )
        back_button_label.pack()
        
        # Bind events to back button
        back_button_frame.bind('<Button-1>', self.back_to_guard_interface)
        back_button_label.bind('<Button-1>', self.back_to_guard_interface)
        
        # Add hover effects
        back_button_frame.bind('<Enter>', self.on_back_hover_enter)
        back_button_frame.bind('<Leave>', self.on_back_hover_leave)
        back_button_label.bind('<Enter>', self.on_back_hover_enter)
        back_button_label.bind('<Leave>', self.on_back_hover_leave)
    
    def submit_visitor_form(self):
        """Handle visitor form submission"""
        # Get form data
        name = self.visitor_name_var.get().strip()
        contact = self.visitor_contact_var.get().strip()
        visiting_as = self.visitor_type_var.get()
        purpose = self.visitor_purpose_var.get().strip()
        visiting = self.visitor_visiting_var.get().strip()
        id_type = self.visitor_id_type_var.get()
        special_pass = self.visitor_special_pass_var.get().strip()
        
        # Validate required fields
        if not name or not contact or not visiting_as or not purpose or not visiting or not id_type:
            messagebox.showwarning("Missing Information", "Please fill in all required fields")
            return
        
        # Check if special pass ID is provided
        if not special_pass:
            messagebox.showwarning("Special Pass Required", "Please make sure to use a Special Pass ID.")
            return
        
        # Check if special pass ID is available for registration (includes cleanup)
        is_available = self.db_manager.is_special_pass_available_for_registration(special_pass)
        if not is_available:
            # Check if it's currently in use (not expired)
            is_in_use, existing_visitor = self.db_manager.is_special_pass_in_use(special_pass)
            if is_in_use:
                # Show error splash screen
                self.show_visitor_error_screen(special_pass, existing_visitor['name'], existing_visitor['expires_at'])
                return
            else:
                # This shouldn't happen, but just in case
                messagebox.showwarning("Special Pass Error", "This Special Pass ID is not available for registration.")
                return
        
        # Get current timestamp
        current_time = datetime.now()
        expiry_time = current_time + timedelta(hours=24)
        
        # Create visitor record
        visitor_data = {
            'name': name,
            'contact': contact,
            'visiting_as': visiting_as,
            'purpose': purpose,
            'visiting': visiting,
            'id_type': id_type,
            'special_pass': special_pass,
            'created_at': current_time.strftime("%Y-%m-%d %H:%M:%S"),
            'expires_at': expiry_time.strftime("%Y-%m-%d %H:%M:%S"),
            'status': 'ACTIVE'
        }
        
        # Save to database
        success = self.db_manager.add_visitor(visitor_data)
        
        if success:
            # Log the visitor entry using Special Pass ID
            self.db_manager.log_access(special_pass, "VISITOR_REGISTRATION")
            
            # Store current Special Pass ID for success screen
            self.current_visitor_id = special_pass
            
            # Show success screen
            self.show_visitor_success_screen(special_pass, name)
        else:
            messagebox.showerror("Registration Failed", "Failed to register visitor. Please try again.")
    
    def show_visitor_success_screen(self, visitor_id, visitor_name):
        """Show visitor registration success screen"""
        # Clear the main frame but keep status bar
        for widget in self.main_frame.winfo_children():
            if widget != self.status_frame:
                widget.destroy()
        
        # Create success interface
        self.create_visitor_form_header()
        self.create_visitor_success_content()
        self.create_visitor_form_sidebar()
        self.update_status_bar_for_visitor_form()
    
    def create_visitor_success_content(self):
        """Create the visitor success content"""
        # Main content frame (white background)
        content_frame = tk.Frame(self.main_frame, bg='white')
        content_frame.pack(side='left', fill='both', expand=True)
        
        # Success message frame
        success_frame = tk.Frame(content_frame, bg='white')
        success_frame.pack(expand=True)
        
        # INFORMATION LINKED text
        info_linked_label = tk.Label(
            success_frame,
            text="INFORMATION LINKED",
            font=("Arial", 36, "bold"),
            fg='#28a745',  # Green
            bg='white'
        )
        info_linked_label.pack(pady=(0, 20))
        
        # Special Pass ready message
        pass_ready_label = tk.Label(
            success_frame,
            text=f"Special Pass No. {self.current_visitor_id} is ready to use",
            font=("Arial", 16),
            fg='black',
            bg='white'
        )
        pass_ready_label.pack(pady=(0, 40))
        
        # OK button
        ok_button = tk.Button(
            success_frame,
            text="OK",
            font=("Arial", 18, "bold"),
            bg='#007BFF',  # Blue
            fg='white',
            relief='flat',
            cursor='hand2',
            command=self.visitor_success_ok_action
        )
        ok_button.pack()
    
    def show_visitor_error_screen(self, special_pass_id, visitor_name, expires_at):
        """Show visitor registration error screen"""
        # Clear the main frame but keep status bar
        for widget in self.main_frame.winfo_children():
            if widget != self.status_frame:
                widget.destroy()
        
        # Create error interface
        self.create_visitor_form_header()
        self.create_visitor_error_content(special_pass_id, visitor_name, expires_at)
        self.create_visitor_form_sidebar()
        self.update_status_bar_for_visitor_form()
    
    def create_visitor_error_content(self, special_pass_id, visitor_name, expires_at):
        """Create the visitor error content"""
        # Main content frame (white background)
        content_frame = tk.Frame(self.main_frame, bg='white')
        content_frame.pack(side='left', fill='both', expand=True)
        
        # Error message frame
        error_frame = tk.Frame(content_frame, bg='white')
        error_frame.pack(expand=True)
        
        # ERROR text
        error_label = tk.Label(
            error_frame,
            text="ERROR",
            font=("Arial", 36, "bold"),
            fg='#dc3545',  # Red
            bg='white'
        )
        error_label.pack(pady=(0, 20))
        
        # Special Pass active message
        pass_active_label = tk.Label(
            error_frame,
            text=f"Special Pass No. {special_pass_id} is currently active",
            font=("Arial", 16),
            fg='black',
            bg='white'
        )
        pass_active_label.pack(pady=(0, 10))
        
        # Wait 24 hours message
        wait_message_label = tk.Label(
            error_frame,
            text="Please wait 24 hours after its submission before resubmitting.",
            font=("Arial", 14),
            fg='black',
            bg='white'
        )
        wait_message_label.pack(pady=(0, 40))
        
        # OK button
        ok_button = tk.Button(
            error_frame,
            text="OK",
            font=("Arial", 18, "bold"),
            bg='#007BFF',  # Blue
            fg='white',
            relief='flat',
            cursor='hand2',
            command=self.visitor_error_ok_action
        )
        ok_button.pack()
    
    def visitor_success_ok_action(self):
        """Handle visitor success OK button"""
        # Return to guard interface
        self.show_guard_interface()
    
    def visitor_error_ok_action(self):
        """Handle visitor error OK button"""
        # Return to visitor form
        self.show_visitor_form_interface()
    
    def back_to_guard_interface(self, event=None):
        """Return to guard interface from visitor form"""
        self.show_guard_interface_without_main_screen()
    
    def on_visitor_rfid_input(self, event=None):
        """Handle visitor RFID input"""
        card_id = self.visitor_id_number_entry.get().strip()
        
        # Check if we have a complete RFID code (typically 10 digits)
        if len(card_id) >= 10:
            # Play beep sound when ID is tapped
            self.play_beep_sound()
            
            # Process the visitor card
            self.process_visitor_card()
    
    def process_visitor_card(self, event=None):
        """Process visitor card tap"""
        card_id = self.visitor_id_number_entry.get().strip()
        
        if not card_id:
            return
        
        print(f"Processing visitor card: {card_id}")  # Debug print
        
        # Find the person in database
        person = self.db_manager.find_person(card_id)
        
        if person:
            print(f"Person found: {person['name']}, Role: {person['role']}")  # Debug print
            if person['role'] == 'SPECIAL':
                # Special pass found - populate the special pass field
                print(f"Special pass accepted: {card_id}")  # Debug print
                self.visitor_special_pass_var.set(card_id)
                # Clear the ID number field
                self.visitor_id_number_entry.delete(0, tk.END)
                # Show success message
                messagebox.showinfo("Special Pass Found", f"Special Pass ID {card_id} has been linked to the form.")
            elif person['role'] in ['GUARD', 'STUDENT', 'TEACHER']:
                # Non-special pass (GUARD, STUDENT, or TEACHER) - show error screen
                print(f"Non-special pass detected: {person['role']} - showing error screen")  # Debug print
                self.show_visitor_special_pass_error()
                # Clear the ID number field
                self.visitor_id_number_entry.delete(0, tk.END)
            else:
                # Unknown role
                print(f"Unknown role detected: {person['role']}")  # Debug print
                messagebox.showwarning("Invalid Role", f"Card has unknown role: {person['role']}")
                # Clear the ID number field
                self.visitor_id_number_entry.delete(0, tk.END)
        else:
            # Person not found
            print(f"Person not found for card: {card_id}")  # Debug print
            messagebox.showwarning("Invalid ID", "Unknown / Invalid ID\nhas been scanned.")
            # Clear the ID number field
            self.visitor_id_number_entry.delete(0, tk.END)
        
        # Refocus the entry field for next card
        self.visitor_id_number_entry.focus()
    
    def show_visitor_special_pass_error(self):
        """Show visitor special pass error screen"""
        print("Showing visitor special pass error screen")  # Debug print
        
        # Clear the main frame but keep status bar
        for widget in self.main_frame.winfo_children():
            if widget != self.status_frame:
                widget.destroy()
        
        # Create error interface
        self.create_visitor_form_header()
        self.create_visitor_special_pass_error_content()
        self.create_visitor_form_sidebar()
        self.update_status_bar_for_visitor_form()
    
    def create_visitor_special_pass_error_content(self):
        """Create the visitor special pass error content"""
        # Main content frame (white background)
        content_frame = tk.Frame(self.main_frame, bg='white')
        content_frame.pack(side='left', fill='both', expand=True)
        
        # Error message frame
        error_frame = tk.Frame(content_frame, bg='white')
        error_frame.pack(expand=True)
        
        # ERROR text
        error_label = tk.Label(
            error_frame,
            text="ERROR",
            font=("Arial", 36, "bold"),
            fg='#dc3545',  # Red
            bg='white'
        )
        error_label.pack(pady=(0, 20))
        
        # Only Special Pass IDs are allowed message
        pass_only_label = tk.Label(
            error_frame,
            text="Only Special Pass IDs are allowed on this form.",
            font=("Arial", 16),
            fg='black',
            bg='white'
        )
        pass_only_label.pack(pady=(0, 10))
        
        # Please make sure to use a Special Pass ID message
        please_use_label = tk.Label(
            error_frame,
            text="Please make sure to use a Special Pass ID.",
            font=("Arial", 16),
            fg='black',
            bg='white'
        )
        please_use_label.pack(pady=(0, 40))
        
        # OK button
        ok_button = tk.Button(
            error_frame,
            text="OK",
            font=("Arial", 18, "bold"),
            bg='#007BFF',  # Blue
            fg='white',
            relief='flat',
            cursor='hand2',
            command=self.visitor_special_pass_error_ok_action
        )
        ok_button.pack()
    
    def visitor_special_pass_error_ok_action(self):
        """Handle visitor special pass error OK button"""
        # Return to visitor form
        self.show_visitor_form_interface()
    
    def show_student_interface(self):
        """Show the student interface"""
        # Clear the main frame but keep status bar
        for widget in self.main_frame.winfo_children():
            if widget != self.status_frame:
                widget.destroy()
        
        # Create student interface
        self.create_student_header()
        self.create_student_content()
        self.create_student_sidebar()
        self.update_status_bar_for_student()
        
        # Ensure focus is set after interface is created
        self.root.after(100, self.focus_student_entry)
    
    def focus_student_entry(self):
        """Focus the student number entry field"""
        if hasattr(self, 'student_number_entry') and self.student_number_entry.winfo_exists():
            self.student_number_entry.focus()
            self.student_number_entry.select_range(0, tk.END)
    
    def create_student_header(self):
        """Create the header with red and blue banners"""
        # Create top frame to hold both banners
        top_frame = tk.Frame(self.main_frame, bg='white', height=100)
        top_frame.pack(side='top', fill='x')
        top_frame.pack_propagate(False)
        
        # Red banner at top left (spans horizontally)
        red_banner = tk.Frame(top_frame, bg='#EA234C', height=100)
        red_banner.pack(side='left', fill='both', expand=True)
        red_banner.pack_propagate(False)
        
        turnstile_label = tk.Label(
            red_banner,
            text="Turnstile is Closed",
            font=("Arial", 16, "bold"),
            bg='#EA234C',
            fg='white'
        )
        turnstile_label.pack(expand=True)
        
        # Blue banner at top right (will extend down to form sidebar)
        blue_banner = tk.Frame(top_frame, bg='#4A90E2', height=100, width=300)
        blue_banner.pack(side='right', fill='y')
        blue_banner.pack_propagate(False)
        
        # Load and display STI BALAGTAS logo
        try:
            logo_path = os.path.join("image-elements", "STI Balagtas Logo.png")
            logo_image = Image.open(logo_path)
            # Resize logo to larger dimensions
            logo_image = logo_image.resize((120, 90), Image.Resampling.LANCZOS)
            self.logo_photo = ImageTk.PhotoImage(logo_image)
            
            logo_label = tk.Label(
                blue_banner,
                image=self.logo_photo,
                bg='#4A90E2'
            )
            logo_label.pack(expand=True, pady=5)
        except Exception as e:
            print(f"Error loading logo: {e}")
            # Fallback to text if image fails to load
            sti_frame = tk.Frame(blue_banner, bg='#4A90E2')
            sti_frame.pack(expand=True, pady=10)
            
            sti_label = tk.Label(
                sti_frame,
                text="STI",
                font=("Arial", 20, "bold"),
                bg='#4A90E2',
                fg='#FFD700'  # Yellow
            )
            sti_label.pack()
            
            balagtas_label = tk.Label(
                sti_frame,
                text="BALAGTAS",
                font=("Arial", 12, "bold"),
                bg='#4A90E2',
                fg='black'
            )
            balagtas_label.pack()
    
    def create_student_content(self):
        """Create the student content"""
        # Main content frame (white background)
        content_frame = tk.Frame(self.main_frame, bg='white')
        content_frame.pack(side='left', fill='both', expand=True)
        
        # Content container
        content_container = tk.Frame(content_frame, bg='white')
        content_container.pack(expand=True)
        
        # Student number prompt
        prompt_label = tk.Label(
            content_container,
            text="Enter the Student Number:",
            font=("Arial", 16, "bold"),
            fg='black',
            bg='white'
        )
        prompt_label.pack(pady=(0, 20))
        
        # Student number input field
        self.student_number_entry = tk.Entry(
            content_container,
            font=("Arial", 14),
            width=30,
            relief='solid',
            bd=1,
            bg='#f0f0f0'
        )
        self.student_number_entry.pack(pady=(0, 30))
        
        # Submit button
        submit_button = tk.Button(
            content_container,
            text="Submit",
            font=("Arial", 14, "bold"),
            bg='#007BFF',  # Blue
            fg='white',
            relief='flat',
            cursor='hand2',
            command=self.submit_student_number
        )
        submit_button.pack()
    
    def create_student_sidebar(self):
        """Create the right sidebar for student interface"""
        # Blue sidebar (extends from top to bottom)
        sidebar = tk.Frame(self.main_frame, bg='#4A90E2', width=300)
        sidebar.pack(side='right', fill='y')
        sidebar.pack_propagate(False)
        
        # Content frame for sidebar
        content_frame = tk.Frame(sidebar, bg='#4A90E2')
        content_frame.pack(expand=True, padx=20, pady=40)
        
        # Instructions
        instructions_label = tk.Label(
            content_frame,
            text="Awaiting ID card scan.",
            font=("Arial", 17, "bold"),
            bg='#4A90E2',
            fg='white'
        )
        instructions_label.pack(anchor='w', pady=(0, 30))
        
        # Visitor button (light grey - inactive)
        visitor_button = tk.Button(
            content_frame,
            text="Visitor",
            font=("Arial", 16, "bold"),
            bg='#d3d3d3',  # Light grey
            fg='black',
            relief='flat',
            cursor='hand2',
            command=self.visitor_action
        )
        visitor_button.pack(fill='x', pady=(0, 10))
        
        # Student button (bright yellow - active)
        student_button = tk.Button(
            content_frame,
            text="Student",
            font=("Arial", 16, "bold"),
            bg='#FFD700',  # Bright yellow
            fg='black',
            relief='flat',
            cursor='hand2',
            command=self.student_action
        )
        student_button.pack(fill='x', pady=(0, 30))
        
        # ID Number section
        id_frame = tk.Frame(content_frame, bg='#4A90E2')
        id_frame.pack(fill='x')
        
        id_label = tk.Label(
            id_frame,
            text="ID Number:",
            font=("Arial", 12, "bold"),
            bg='#4A90E2',
            fg='white'
        )
        id_label.pack(anchor='w')
        
        # ID Number input field
        self.student_id_number_entry = tk.Entry(
            id_frame,
            font=("Arial", 12),
            width=20,
            relief='solid',
            bd=1,
            bg='white',
            fg='black'
        )
        self.student_id_number_entry.pack(fill='x', pady=(5, 0))
        
        # Guard information
        guard_info_frame = tk.Frame(content_frame, bg='#4A90E2')
        guard_info_frame.pack(pady=(30, 0))
        
        guard_label = tk.Label(
            guard_info_frame,
            text="Guard in-charge:",
            font=("Arial", 12, "bold"),
            bg='#4A90E2',
            fg='white'
        )
        guard_label.pack(anchor='w')
        
        # Get guard name from stored information or use default
        guard_name = self.current_guard['name'] if self.current_guard else "Unknown Guard"
        
        guard_name_label = tk.Label(
            guard_info_frame,
            text=guard_name,
            font=("Arial", 12),
            bg='#4A90E2',
            fg='white'
        )
        guard_name_label.pack(anchor='w')
    
    def update_status_bar_for_student(self):
        """Update status bar to show Back button for student interface"""
        # Clear existing status bar
        for widget in self.status_frame.winfo_children():
            widget.destroy()
        
        # Time section (dark blue)
        now = datetime.now()
        time_str = now.strftime("%I:%M:%S %p")
        self.time_label = tk.Label(
            self.status_frame,
            text=time_str,
            font=("Arial", 12, "bold"),
            bg='#006CB7',  # Blue
            fg='white',
            padx=20,
            pady=10
        )
        self.time_label.pack(side='left', fill='x', expand=True)
        
        # Date section (very dark blue/black)
        date_str = now.strftime("%B %d, %Y")
        self.date_label = tk.Label(
            self.status_frame,
            text=date_str,
            font=("Arial", 12, "bold"),
            bg='#021C37',  # Dark blue
            fg='white',
            padx=20,
            pady=10
        )
        self.date_label.pack(side='left', fill='x', expand=True)
        
        # Back button (orange)
        back_button_frame = tk.Frame(
            self.status_frame,
            bg='#EF5E1D',  # Orange
            relief='flat',
            padx=20,
            pady=10
        )
        back_button_frame.pack(side='left', fill='x', expand=True)
        
        back_button_label = tk.Label(
            back_button_frame,
            text="Back",
            font=("Arial", 12, "bold"),
            bg='#EF5E1D',  # Orange
            fg='white',
            cursor='hand2'
        )
        back_button_label.pack()
        
        # Bind events to back button
        back_button_frame.bind('<Button-1>', self.back_to_guard_interface)
        back_button_label.bind('<Button-1>', self.back_to_guard_interface)
        
        # Add hover effects
        back_button_frame.bind('<Enter>', self.on_back_hover_enter)
        back_button_frame.bind('<Leave>', self.on_back_hover_leave)
        back_button_label.bind('<Enter>', self.on_back_hover_enter)
        back_button_label.bind('<Leave>', self.on_back_hover_leave)
    
    def submit_student_number(self):
        """Handle student number submission"""
        student_number = self.student_number_entry.get().strip()
        
        if not student_number:
            messagebox.showwarning("Missing Information", "Please enter a student number.")
            return
        
        # Check if student number exists in database
        is_valid = self.db_manager.is_student_number_valid(student_number)
        
        if is_valid:
            # Get the person data for the student number
            person_data = self.db_manager.get_person_by_student_number(student_number)
            
            if person_data:
                # Log the access attempt
                self.db_manager.log_access(student_number, "STUDENT_NUMBER_SCAN")
                
                # Clear the input field
                self.student_number_entry.delete(0, tk.END)
                
                # Trigger the scanning process (same as RFID card tap)
                self.trigger_scanning_process_for_student(person_data)
            else:
                messagebox.showwarning("Database Error", "Student data not found in database.")
                self.student_number_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Invalid Student", "This is not a Valid Student Number")
            # Clear the input field
            self.student_number_entry.delete(0, tk.END)
        
        # Refocus the entry field
        self.student_number_entry.focus()
    
    def trigger_scanning_process_for_student(self, person_data):
        """Trigger the scanning process for a student (simulate RFID card tap)"""
        print(f"Triggering scanning process for student: {person_data['name']}")
        
        # Store the person data for the scanning process
        self.compliance_person_data = person_data
        
        # Show the student/teacher splash screen which will trigger the scanning process
        self.show_student_teacher_splash(person_data, duration=8)
    
    def on_guard_rfid_input(self, event=None):
        """Handle automatic RFID keyboard input for guard interface"""
        if self.is_processing:
            return  # Prevent duplicate processing
        
        card_id = self.id_number_entry.get().strip()
        
        # Check if we have a complete RFID code (typically 10 digits)
        if len(card_id) >= 10:
            # Play beep sound when ID is tapped
            self.play_beep_sound()
            
            self.is_processing = True
            # Process the card after a short delay to ensure complete input
            self.root.after(100, self.process_guard_card)
    
    def process_guard_card(self, event=None):
        """Process the card tap in guard interface"""
        if not self.is_processing:
            return  # Prevent duplicate processing from Enter key
        
        card_id = self.id_number_entry.get().strip()
        
        if not card_id:
            self.is_processing = False
            return
        
        # Log the access attempt
        self.db_manager.log_access(card_id, "GUARD_CARD_SCAN")
        
        # Clean up expired Special Passes before processing
        self.db_manager.cleanup_expired_special_passes()
        
        # Find the person in database
        person = self.db_manager.find_person(card_id)
        
        if person:
            # Check if it's a Special Pass and handle grace period
            if person['role'] == 'SPECIAL':
                # Get current check status first
                check_status = self.db_manager.get_special_pass_check_status(card_id)
                
                # Check if trying to check-in after expiration
                if check_status == "CHECKED_OUT" and self.db_manager.is_special_pass_expired_for_checkin(card_id):
                    # Special Pass has expired for check-in - show deactivated message
                    self.last_response_message = "Deactivated Pass has been scanned."
                    if hasattr(self, 'guard_message_label') and self.guard_message_label.winfo_exists():
                        self.guard_message_label.config(text=self.last_response_message)
                    
                    # Send deactivated pass status to main screen
                    try:
                        with open("main_screen_status.txt", "w") as f:
                            f.write("DEACTIVATED_PASS\n")
                            f.write("N/A\n")
                            f.write("N/A\n")
                            f.write("N/A\n")
                        print("Deactivated pass status sent to main screen")
                    except Exception as e:
                        print(f"Error writing status file: {e}")
                    
                    # Clear the input field
                    self.id_number_entry.delete(0, tk.END)
                    # Schedule message reset after 5 seconds
                    self._schedule_message_reset()
                    print(f"Expired Special Pass tried to check-in: {person['name']}")
                elif check_status == "CHECKED_IN" and self.db_manager.is_special_pass_in_grace_period(card_id):
                    # Special Pass is in grace period - allow check-out
                    self.current_special_pass = person
                    self.current_special_pass_id = card_id
                    
                    # Ensure Special Pass record exists in visitors file
                    self.db_manager.ensure_special_pass_record(card_id, person)
                    
                    # Allow check-out in grace period
                    self.db_manager.record_special_pass_check(card_id, "CHECK_OUT")
                    self.current_check_type = "CHECK_OUT"
                    print(f"Special Pass {card_id} checked out in grace period")
                    
                    # Clear the input field
                    self.id_number_entry.delete(0, tk.END)
                    # Show Special Pass active interface
                    self.show_special_pass_active_interface()
                    print(f"Special Pass checked out in grace period: {person['name']}")
                elif self.db_manager.is_special_pass_expired(card_id):
                    # Special Pass has expired and not in grace period - show deactivated message
                    self.last_response_message = "Deactivated Pass has been scanned."
                    if hasattr(self, 'guard_message_label') and self.guard_message_label.winfo_exists():
                        self.guard_message_label.config(text=self.last_response_message)
                    
                    # Send deactivated pass status to main screen
                    try:
                        with open("main_screen_status.txt", "w") as f:
                            f.write("DEACTIVATED_PASS\n")
                            f.write("N/A\n")
                            f.write("N/A\n")
                            f.write("N/A\n")
                        print("Deactivated pass status sent to main screen")
                    except Exception as e:
                        print(f"Error writing status file: {e}")
                    
                    # Clear the input field
                    self.id_number_entry.delete(0, tk.END)
                    # Schedule message reset after 5 seconds
                    self._schedule_message_reset()
                    print(f"Expired Special Pass scanned: {person['name']}")
                else:
                    # Special Pass is still valid - handle normal check-in/check-out
                    self.current_special_pass = person
                    self.current_special_pass_id = card_id
                    
                    # Ensure Special Pass record exists in visitors file
                    self.db_manager.ensure_special_pass_record(card_id, person)
                    
                    if check_status == "CHECKED_OUT":
                        # Need to check in
                        self.db_manager.record_special_pass_check(card_id, "CHECK_IN")
                        self.current_check_type = "CHECK_IN"
                        print(f"Special Pass {card_id} checked in")
                    else:
                        # Need to check out
                        self.db_manager.record_special_pass_check(card_id, "CHECK_OUT")
                        self.current_check_type = "CHECK_OUT"
                        print(f"Special Pass {card_id} checked out")
                    
                    # Clear the input field
                    self.id_number_entry.delete(0, tk.END)
                    # Show Special Pass active interface
                    self.show_special_pass_active_interface()
                    print(f"Valid Special Pass scanned: {person['name']}")
            else:
                # Non-Special Pass (GUARD, STUDENT, TEACHER, etc.)
                if person['role'] in ['STUDENT', 'TEACHER']:
                    # Show splash screen for students and teachers
                    print(f"Student/Teacher card scanned: {person['name']} ({person['role']})")
                    
                    # Clear the input field
                    self.id_number_entry.delete(0, tk.END)
                    
                    # Show splash screen in the same window
                    self.show_student_teacher_splash(person, 8)
                    
                    # Log the access
                    self.db_manager.log_access(card_id, f"{person['role']}_ACCESS")
                else:
                    # For other roles (GUARD, etc.) - clear message and show success
                    self.last_response_message = ""
                    if hasattr(self, 'guard_message_label') and self.guard_message_label.winfo_exists():
                        self.guard_message_label.config(text="Awaiting ID card scan.")
                    # Clear the input field
                    self.id_number_entry.delete(0, tk.END)
                    # Show success message (optional)
                    print(f"Valid card scanned: {person['name']} ({person['role']})")
        else:
            # Person not found - show error message
            self.last_response_message = "Unknown / Invalid ID\nhas been scanned."
            if hasattr(self, 'guard_message_label') and self.guard_message_label.winfo_exists():
                self.guard_message_label.config(text=self.last_response_message)
            
            # Send invalid ID status to main screen
            try:
                with open("main_screen_status.txt", "w") as f:
                    f.write("INVALID_ID\n")
                    f.write("N/A\n")
                    f.write("N/A\n")
                    f.write("N/A\n")
                print("Invalid ID status sent to main screen")
            except Exception as e:
                print(f"Error writing status file: {e}")
            
            # Clear the input field
            self.id_number_entry.delete(0, tk.END)
            # Schedule message reset after 5 seconds
            self._schedule_message_reset()
        
        # Reset processing flag
        self.is_processing = False
        
        # Refocus the entry field for next card (only if it exists)
        try:
            if hasattr(self, 'id_number_entry') and self.id_number_entry.winfo_exists():
                self.id_number_entry.focus()
        except Exception as e:
            print(f"Error focusing entry field: {e}")
    
    def show_student_teacher_splash(self, person_data, duration=8):
        """Show splash screen for student/teacher in the same window"""
        # Store current interface state
        self.splash_camera_detector = None
        self.splash_is_running = False
        self.compliance_person_data = person_data
        self.no_detection_count = 0  # Counter for consecutive frames with no detection
        
        # Disable logout button during splash screen
        self.disable_logout_button()

        # Write initial student/teacher info status to main screen
        try:
            current_time = datetime.now().strftime("%I:%M:%S %p")
            guard_name = self.current_guard['name'] if self.current_guard else "Unknown Guard"
            person_name = person_data.get('name', 'Unknown')
            person_role = person_data.get('role', 'USER')
            with open("main_screen_status.txt", "w") as f:
                f.write("STUDENT_TEACHER_INFO\n")
                f.write(f"{person_name}\n")
                f.write(f"{person_role}\n")
                f.write(f"{current_time}\n")
                f.write(f"{guard_name}\n")
        except Exception as e:
            print(f"Error writing student/teacher info status: {e}")
        
        # Clear the main frame but keep header and status bar
        for widget in self.main_frame.winfo_children():
            if widget not in [self.status_frame]:
                widget.destroy()
        
        # Create header (Turnstile is Closed + Guard in-charge)
        self.create_splash_header()
        
        # Create splash content
        self.create_splash_content_integrated(person_data)
        
        # Initialize camera
        self.initialize_splash_camera()
        
        # Start camera feed
        self.start_splash_camera_feed()

        # Initialize timed status sequence (3s ready -> 3s scanning -> 2s result)
        try:
            self._splash_timers = []
            self.set_splash_status("Getting ready in 3 second(s)...")
            self._schedule_splash(3000, lambda: self.set_splash_status("Scanning is in progress... Please do not move."))
            # At 6s, show result frame for ~2s
            self._schedule_splash(6000, self._show_scan_complete_overlay)
        except Exception as _e:
            pass
        
        # Auto-close after duration
        self.main_frame.after(duration * 1000, self.close_splash_and_restore)
        
        # Bind escape key to close
        self.root.bind('<Escape>', lambda e: self.close_splash_and_restore())
    
    def create_splash_content_integrated(self, person_data):
        """Create the splash screen content in the main window"""
        # Main container
        main_container = tk.Frame(self.main_frame, bg='white')
        main_container.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Left side - Camera feed
        camera_frame = tk.Frame(main_container, bg='black', width=640, height=480)
        camera_frame.pack(side='left', padx=(0, 20))
        camera_frame.pack_propagate(False)
        
        # Camera label
        self.splash_camera_label = tk.Label(camera_frame, bg='black', text="Initializing camera...")
        self.splash_camera_label.pack(expand=True)
        
        # Right side - Information panel
        info_frame = tk.Frame(main_container, bg='#4A90E2', width=400, height=480)
        info_frame.pack(side='right', fill='y')
        info_frame.pack_propagate(False)
        
        # Profile picture
        self.create_splash_profile_section(info_frame, person_data)
        
        # Information section
        self.create_splash_info_section(info_frame)
        
        # Guard in-charge section
        self.create_splash_guard_section(info_frame)

        # Status banner below camera (light blue) for step messages
        status_bar = tk.Frame(self.main_frame, bg='#ADD8E6', height=40)
        status_bar.pack(side='top', fill='x')
        status_bar.pack_propagate(False)
        self.splash_status_label = tk.Label(status_bar, text="", font=("Arial", 16, "bold"), bg='#ADD8E6', fg='black')
        self.splash_status_label.pack(expand=True)

    def set_splash_status(self, text):
        try:
            if hasattr(self, 'splash_status_label') and self.splash_status_label.winfo_exists():
                self.splash_status_label.config(text=text)
        except Exception:
            pass

    def _schedule_splash(self, delay_ms, func):
        try:
            self.main_frame.after(delay_ms, func)
        except Exception:
            pass

    def _show_scan_complete_overlay(self):
        # Replace left camera area with scan-ok image on black background
        try:
            self.set_splash_status("Please wait for the result.")
            # Find the left camera label and replace its image/content
            ok_path = os.path.join("image-elements", "scan-ok.png")
            if os.path.exists(ok_path):
                img = Image.open(ok_path)
                img = img.resize((640, 360), Image.Resampling.LANCZOS)
                self._scan_ok_photo = ImageTk.PhotoImage(img)
                if hasattr(self, 'splash_camera_label') and self.splash_camera_label.winfo_exists():
                    self.splash_camera_label.config(image=self._scan_ok_photo, text="", bg='black')
        except Exception as _e:
            pass
    
    def create_splash_profile_section(self, parent, person_data):
        """Create profile picture section for splash screen"""
        profile_frame = tk.Frame(parent, bg='#4A90E2')
        profile_frame.pack(pady=20)
        
        # Load profile picture
        profile_image = self.load_splash_profile_image(person_data)
        if profile_image:
            # Resize to 2x2 inches (approximately 150x150 pixels)
            profile_image = profile_image.resize((150, 150), Image.Resampling.LANCZOS)
            self.splash_profile_photo = ImageTk.PhotoImage(profile_image)
            
            profile_label = tk.Label(profile_frame, image=self.splash_profile_photo, bg='#4A90E2')
            profile_label.pack()
        else:
            # Default profile picture
            default_label = tk.Label(profile_frame, text="No Photo", font=("Arial", 16), 
                                   bg='#4A90E2', fg='white', width=10, height=6)
            default_label.pack()
        
        # Name and role
        name_label = tk.Label(profile_frame, text=person_data['name'], 
                             font=("Arial", 18, "bold"), bg='#4A90E2', fg='white')
        name_label.pack(pady=(10, 5))
        
        role_label = tk.Label(profile_frame, text=f"({person_data['role']})", 
                             font=("Arial", 14), bg='#4A90E2', fg='white')
        role_label.pack()
    
    def create_splash_info_section(self, parent):
        """Create information section for splash screen"""
        info_frame = tk.Frame(parent, bg='#4A90E2')
        info_frame.pack(pady=20, fill='both', expand=True, padx=20)
        
        # Check-in time
        checkin_time = datetime.now().strftime("%I:%M:%S %p")
        time_label = tk.Label(info_frame, text=f"Time Check-in: {checkin_time}", 
                             font=("Arial", 14), bg='#4A90E2', fg='white')
        time_label.pack(anchor='w')
        
        # Date
        checkin_date = datetime.now().strftime("%B %d, %Y")
        date_label = tk.Label(info_frame, text=f"Date: {checkin_date}", 
                             font=("Arial", 14, "bold"), bg='#4A90E2', fg='white')
        date_label.pack(anchor='w', pady=(10, 0))
    
    def create_splash_guard_section(self, parent):
        """Create guard in-charge section for splash screen"""
        guard_frame = tk.Frame(parent, bg='#4A90E2')
        guard_frame.pack(pady=20, fill='x', padx=20)
        
        # Guard in-charge label
        guard_label = tk.Label(guard_frame, text="Guard in-charge:", 
                              font=("Arial", 14, "bold"), bg='#4A90E2', fg='white')
        guard_label.pack(anchor='w')
        
        # Get guard name from stored information or use default
        guard_name = self.current_guard['name'] if self.current_guard else "Unknown Guard"
        
        # Guard name
        guard_name_label = tk.Label(guard_frame, text=guard_name, 
                                   font=("Arial", 14), bg='#4A90E2', fg='white')
        guard_name_label.pack(anchor='w', pady=(5, 0))
    
    def load_splash_profile_image(self, person_data):
        """Load profile image from appropriate folder"""
        try:
            person_id = person_data['id']
            role = person_data['role'].lower()
            
            # For students, get the student number from the database
            if role == 'student':
                student_number = self.get_student_number_from_rfid(person_id)
                if student_number:
                    person_id = student_number
                    folder = 'image-students'
                else:
                    print(f"Could not find student number for RFID: {person_id}")
                    return None
            elif role == 'teacher':
                folder = 'image-teachers'
            else:
                return None
            
            # Try different image extensions
            extensions = ['.jpg', '.jpeg', '.png', '.bmp']
            for ext in extensions:
                image_path = os.path.join(folder, f"{person_id}{ext}")
                if os.path.exists(image_path):
                    print(f"Loading profile image: {image_path}")
                    return Image.open(image_path)
            
            # If no image found, return None
            print(f"No profile image found for {person_id} in {folder}")
            return None
            
        except Exception as e:
            print(f"Error loading profile image: {e}")
            return None
    
    def get_student_number_from_rfid(self, rfid_id):
        """Get student number from RFID ID"""
        try:
            with open(self.db_manager.db_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith('#') or not line:
                        continue
                    
                    parts = line.split(',')
                    if len(parts) >= 3:
                        db_id = parts[0]
                        role = parts[1]
                        
                        # Check if this is a STUDENT_RFID entry that matches our RFID
                        if role == 'STUDENT_RFID' and db_id == rfid_id:
                            # The student number is in the third column
                            if len(parts) >= 3:
                                student_number = parts[2]
                                print(f"Found student number {student_number} for RFID {rfid_id}")
                                return student_number
            
            print(f"No student number found for RFID: {rfid_id}")
            return None
            
        except Exception as e:
            print(f"Error getting student number: {e}")
            return None
    
    def initialize_splash_camera(self):
        """Initialize camera and YOLO model for splash screen"""
        try:
            self.splash_camera_detector = YOLOCameraDetection()
            if not self.splash_camera_detector.load_model():
                print("Warning: Could not load YOLO model")
            if not self.splash_camera_detector.initialize_camera():
                print("Warning: Could not initialize camera")
        except Exception as e:
            print(f"Error initializing camera: {e}")
    
    def start_splash_camera_feed(self):
        """Start the camera feed update loop for splash screen"""
        self.splash_is_running = True
        # Add a small delay to let camera initialize, then start detection
        self.main_frame.after(1000, self.update_splash_camera_feed)
    
    def update_splash_camera_feed(self):
        """Update camera feed with detection results for splash screen"""
        if not self.splash_is_running:
            return
        
        try:
            if self.splash_camera_detector and self.splash_camera_detector.cap:
                frame = self.splash_camera_detector.get_frame_with_detection()
                if frame is not None:
                    # Convert frame to PIL Image
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    frame_pil = Image.fromarray(frame_rgb)
                    
                    # Resize to fit the camera frame
                    frame_pil = frame_pil.resize((640, 480), Image.Resampling.LANCZOS)
                    
                    # Convert to PhotoImage
                    self.splash_camera_photo = ImageTk.PhotoImage(frame_pil)
                    
                    # Update camera label
                    self.splash_camera_label.configure(image=self.splash_camera_photo, text="")
                    
                    # Add detection logic here
                    if self.splash_camera_detector.model is not None:
                        detections = self.splash_camera_detector.detect_objects(frame)
                        print(f"Detection count: {len(detections)}")  # Debug print
                        
                        if detections:
                            # Reset no detection counter
                            self.no_detection_count = 0
                            
                            # Analyze detections to determine result
                            class_counts = {}
                            for detection in detections:
                                class_name = detection['class_name'].lower()
                                class_counts[class_name] = class_counts.get(class_name, 0) + 1
                            
                            # Check if all required items are detected
                            ict_longsleeve = class_counts.get('ict longsleeve', 0)
                            ict_logo = class_counts.get('ict logo', 0)
                            black_shoes = class_counts.get('black shoes', 0)
                            ict_pants = class_counts.get('ict pants', 0)
                            
                            if ict_longsleeve >= 1 and ict_logo >= 1 and black_shoes >= 1 and ict_pants >= 1:
                                # All required items detected - clean
                                self.compliance_result = "clean"
                            else:
                                # Partial detection - manual verification needed
                                self.compliance_result = "manual_verification"
                                print("Manual verification needed - showing compliance interface")
                                # Stop the splash screen first
                                self.splash_is_running = False
                                if self.splash_camera_detector:
                                    self.splash_camera_detector.cleanup()
                                # Show the guard screen with Approve/Deny buttons
                                self.show_uniform_compliance_interface(self.compliance_person_data, "manual_verification")
                                return  # Stop camera feed updates
                        else:
                            # No detections - increment counter
                            self.no_detection_count += 1
                            print(f"No objects detected - count: {self.no_detection_count}")  # Debug print
                            
                            # Show guard screen with Approve/Deny buttons after 3 seconds (90 frames at 30fps)
                            if self.no_detection_count >= 90:
                                print("No objects detected for 3 seconds - showing guard screen with Approve/Deny buttons")  # Debug print
                                self.compliance_result = "manual_verification"
                                # Stop the splash screen first
                                self.splash_is_running = False
                                if self.splash_camera_detector:
                                    self.splash_camera_detector.cleanup()
                                # Show the guard screen with Approve/Deny buttons
                                self.show_uniform_compliance_interface(self.compliance_person_data, "manual_verification")
                                return  # Stop camera feed updates
                    else:
                        # No model available - assume clean
                        print("No model available - assuming clean")  # Debug print
                        self.compliance_result = "clean"
            
        except Exception as e:
            print(f"Error updating camera feed: {e}")
        
        # Schedule next update
        if self.splash_is_running:
            self.main_frame.after(33, self.update_splash_camera_feed)  # ~30 FPS
    

    
    def close_splash_and_restore(self):
        """Close the splash screen and then show the Approve/Deny frame"""
        self.splash_is_running = False
        if self.splash_camera_detector:
            self.splash_camera_detector.cleanup()
        
        # Enable logout button after splash screen closes
        self.enable_logout_button()
        
        # After the splash, present the compliance interface (Approve/Deny)
        try:
            detection_result = getattr(self, 'compliance_result', 'manual_verification')
            # Show compliance UI inline
            self.show_uniform_compliance_interface(self.compliance_person_data, detection_result)
        except Exception as e:
            print(f"Error showing compliance interface after splash: {e}")
            # Fallback to guard interface
            self.show_guard_interface()
        
        # Unbind escape key
        try:
            self.root.unbind('<Escape>')
        except:
            pass
    
    def create_splash_header(self):
        """Create the header with Turnstile is Closed and Guard in-charge"""
        # Create top frame to hold both banners
        top_frame = tk.Frame(self.main_frame, bg='white', height=100)
        top_frame.pack(side='top', fill='x')
        top_frame.pack_propagate(False)
        
        # Red banner at top left (spans horizontally)
        red_banner = tk.Frame(top_frame, bg='#EA234C', height=100)
        red_banner.pack(side='left', fill='both', expand=True)
        red_banner.pack_propagate(False)
        
        turnstile_label = tk.Label(
            red_banner,
            text="Turnstile is Closed",
            font=("Arial", 16, "bold"),
            bg='#EA234C',
            fg='white'
        )
        turnstile_label.pack(expand=True)
        
        # Blue banner at top right (will extend down to form sidebar)
        blue_banner = tk.Frame(top_frame, bg='#4A90E2', height=100, width=300)
        blue_banner.pack(side='right', fill='y')
        blue_banner.pack_propagate(False)
        
        # Load and display STI BALAGTAS logo
        try:
            logo_path = os.path.join("image-elements", "STI Balagtas Logo.png")
            logo_image = Image.open(logo_path)
            # Resize logo to larger dimensions
            logo_image = logo_image.resize((120, 90), Image.Resampling.LANCZOS)
            self.splash_logo_photo = ImageTk.PhotoImage(logo_image)
            
            logo_label = tk.Label(
                blue_banner,
                image=self.splash_logo_photo,
                bg='#4A90E2'
            )
            logo_label.pack(expand=True, pady=5)
        except Exception as e:
            print(f"Error loading logo: {e}")
            # Fallback to text if image fails to load
            sti_frame = tk.Frame(blue_banner, bg='#4A90E2')
            sti_frame.pack(expand=True, pady=10)
            
            sti_label = tk.Label(
                sti_frame,
                text="STI",
                font=("Arial", 20, "bold"),
                bg='#4A90E2',
                fg='#FFD700'  # Yellow
            )
            sti_label.pack()
            
            balagtas_label = tk.Label(
                sti_frame,
                text="BALAGTAS",
                font=("Arial", 12, "bold"),
                bg='#4A90E2',
                fg='black'
            )
            balagtas_label.pack()
        
        # Guard information will be integrated into the main content area
    
    def _schedule_message_reset(self):
        """Schedule the message to reset back to default in 5 seconds"""
        if self.message_reset_after_id is not None:
            try:
                self.root.after_cancel(self.message_reset_after_id)
            except Exception:
                pass
        
        self.message_reset_after_id = self.root.after(5000, self.reset_guard_message)
    
    def reset_main_screen_message(self):
        """Reset the main screen message back to default"""
        try:
            with open("main_screen_status.txt", "w") as f:
                f.write("RESET_TO_DEFAULT\n")
                f.write("N/A\n")
                f.write("N/A\n")
                f.write("N/A\n")
            print("Reset to default status sent to main screen")
        except Exception as e:
            print(f"Error writing reset status file: {e}")
    
    def reset_guard_message(self):
        """Reset the guard message back to default"""
        self.last_response_message = ""
        if self.message_reset_after_id is not None:
            try:
                self.root.after_cancel(self.message_reset_after_id)
            except Exception:
                pass
            self.message_reset_after_id = None
        
        if hasattr(self, 'guard_message_label') and self.guard_message_label.winfo_exists():
            self.guard_message_label.config(text="Awaiting ID card scan.")
        
        # Also reset the main screen message
        self.reset_main_screen_message()
    
    def show_special_pass_active_interface(self):
        """Show the Special Pass active interface"""
        # Clear the main frame but keep status bar
        for widget in self.main_frame.winfo_children():
            if widget != self.status_frame:
                widget.destroy()
        
        # Write status to main screen status file based on check type
        try:
            current_time = datetime.now().strftime("%I:%M:%S %p")
            guard_name = self.current_guard['name'] if self.current_guard else "Unknown Guard"
            special_pass_id = self.current_special_pass_id if hasattr(self, 'current_special_pass_id') else "Unknown"
            
            # Determine status based on check type
            if hasattr(self, 'current_check_type') and self.current_check_type == "CHECK_OUT":
                status = "SPECIAL_PASS_CHECKOUT"
                print(f"Special Pass checkout status sent to main screen for {special_pass_id}")
            else:
                status = "TURNSTILE_OPEN"
                print(f"Turnstile opened status sent to main screen for Special Pass {special_pass_id}")
            
            with open("main_screen_status.txt", "w") as f:
                f.write(f"{status}\n")
                f.write(f"{special_pass_id}\n")
                f.write(f"{current_time}\n")
                f.write(f"{guard_name}\n")
        except Exception as e:
            print(f"Error writing status file: {e}")
        
        # Create Special Pass active interface
        self.create_special_pass_active_header()
        self.create_special_pass_active_main_content()
        self.create_special_pass_active_sidebar()
        self.update_status_bar_for_special_pass_active()
    
    def create_special_pass_active_header(self):
        """Create the header with green and blue banners for Special Pass active"""
        # Create top frame to hold both banners
        top_frame = tk.Frame(self.main_frame, bg='white', height=120)
        top_frame.pack(side='top', fill='x')
        top_frame.pack_propagate(False)
        
        # Green banner at top (Turnstile is Open)
        green_banner = tk.Frame(top_frame, bg='#90EE90', height=60)  # Light green
        green_banner.pack(side='top', fill='x')
        green_banner.pack_propagate(False)
        
        turnstile_open_label = tk.Label(
            green_banner,
            text="Turnstile is Open",
            font=("Arial", 16, "bold"),
            bg='#90EE90',
            fg='black'
        )
        turnstile_open_label.pack(expand=True)
        
        # Blue banner below (Special Pass Active + Close button)
        blue_banner = tk.Frame(top_frame, bg='#87CEEB', height=60)  # Light blue
        blue_banner.pack(side='top', fill='x')
        blue_banner.pack_propagate(False)
        
        # Left side - Special Pass Active message
        pass_active_label = tk.Label(
            blue_banner,
            text="This Special Pass is Active.",
            font=("Arial", 14, "bold"),
            bg='#87CEEB',
            fg='black'
        )
        pass_active_label.pack(side='left', padx=20, pady=20)
        
        # Right side - Close Turnstile button
        close_button = tk.Button(
            blue_banner,
            text="Close the Turnstile",
            font=("Arial", 12, "bold"),
            bg='#FFA500',  # Orange
            fg='black',
            relief='flat',
            cursor='hand2',
            command=self.close_turnstile_action
        )
        close_button.pack(side='right', padx=20, pady=15)
    
    def create_special_pass_active_main_content(self):
        """Create the main content area with AI-niform logo"""
        # Main content frame (white background)
        content_frame = tk.Frame(self.main_frame, bg='white')
        content_frame.pack(side='left', fill='both', expand=True)
        
        # AI-niform logo (centered in white area)
        logo_frame = tk.Frame(content_frame, bg='white')
        logo_frame.pack(expand=True)
        
        logo_container = tk.Frame(logo_frame, bg='white')
        logo_container.pack(pady=(100, 20))
        
        # Al- part in light blue
        ai_part = tk.Label(
            logo_container,
            text="Al-",
            font=("Arial", 48, "bold"),
            bg='white',
            fg='#4A90E2'  # Light blue
        )
        ai_part.pack(side='left')
        
        # -niform part in dark gray/black
        niform_part = tk.Label(
            logo_container,
            text="niform",
            font=("Arial", 48, "bold"),
            bg='white',
            fg='#2C3E50'  # Dark gray/black
        )
        niform_part.pack(side='left')
    
    def create_special_pass_active_sidebar(self):
        """Create the right sidebar with Special Pass details and user image"""
        # Blue sidebar (extends from top to bottom)
        sidebar = tk.Frame(self.main_frame, bg='#4A90E2', width=300)
        sidebar.pack(side='right', fill='y')
        sidebar.pack_propagate(False)
        
        # Content frame for sidebar
        content_frame = tk.Frame(sidebar, bg='#4A90E2')
        content_frame.pack(expand=True, padx=20, pady=40)
        
        # STI BALAGTAS logo at top
        try:
            logo_path = os.path.join("image-elements", "STI Balagtas Logo.png")
            logo_image = Image.open(logo_path)
            # Resize logo to smaller dimensions
            logo_image = logo_image.resize((60, 45), Image.Resampling.LANCZOS)
            self.sti_logo_photo = ImageTk.PhotoImage(logo_image)
            
            logo_label = tk.Label(
                content_frame,
                image=self.sti_logo_photo,
                bg='#4A90E2'
            )
            logo_label.pack(pady=(0, 20))
        except Exception as e:
            print(f"Error loading STI logo: {e}")
            # Fallback to text
            sti_label = tk.Label(
                content_frame,
                text="STI BALAGTAS",
                font=("Arial", 14, "bold"),
                bg='#4A90E2',
                fg='white'
            )
            sti_label.pack(pady=(0, 20))
        
        # Generic User Image
        try:
            user_image_path = os.path.join("image-elements", "Generic User Image.jpg")
            user_image = Image.open(user_image_path)
            # Resize to square format
            user_image = user_image.resize((150, 150), Image.Resampling.LANCZOS)
            self.user_photo = ImageTk.PhotoImage(user_image)
            
            user_image_label = tk.Label(
                content_frame,
                image=self.user_photo,
                bg='#4A90E2'
            )
            user_image_label.pack(pady=(0, 20))
        except Exception as e:
            print(f"Error loading user image: {e}")
            # Fallback to placeholder
            placeholder_label = tk.Label(
                content_frame,
                text="[User Image]",
                font=("Arial", 12),
                bg='#4A90E2',
                fg='white',
                width=20,
                height=8
            )
            placeholder_label.pack(pady=(0, 20))
        
        # Special Pass details
        special_pass_label = tk.Label(
            content_frame,
            text="Special Pass",
            font=("Arial", 16, "bold"),
            bg='#4A90E2',
            fg='white'
        )
        special_pass_label.pack(anchor='w')
        
        # Reference number (using the actual Special Pass ID)
        ref_number = self.current_special_pass_id if self.current_special_pass_id else "0000000000"
        ref_label = tk.Label(
            content_frame,
            text=f"Ref. {ref_number}",
            font=("Arial", 12),
            bg='#4A90E2',
            fg='white'
        )
        ref_label.pack(anchor='w')
        
        # Time Check-in/Check-out
        check_in_time, check_out_time = self.db_manager.get_special_pass_check_times(self.current_special_pass_id)
        
        if self.current_check_type == "CHECK_IN" and check_in_time:
            # Show check-in time
            try:
                check_in_dt = datetime.strptime(check_in_time, "%Y-%m-%d %H:%M:%S")
                check_in_display = check_in_dt.strftime("%I:%M:%S %p")
                time_label = tk.Label(
                    content_frame,
                    text=f"Time Check-in: {check_in_display}",
                    font=("Arial", 10),
                    bg='#4A90E2',
                    fg='white'
                )
                time_label.pack(anchor='w', pady=(5, 0))
            except:
                time_label = tk.Label(
                    content_frame,
                    text=f"Time Check-in: {check_in_time}",
                    font=("Arial", 10),
                    bg='#4A90E2',
                    fg='white'
                )
                time_label.pack(anchor='w', pady=(5, 0))
        elif self.current_check_type == "CHECK_OUT" and check_out_time:
            # Show check-out time
            try:
                check_out_dt = datetime.strptime(check_out_time, "%Y-%m-%d %H:%M:%S")
                check_out_display = check_out_dt.strftime("%I:%M:%S %p")
                time_label = tk.Label(
                    content_frame,
                    text=f"Time Check-out: {check_out_display}",
                    font=("Arial", 10),
                    bg='#4A90E2',
                    fg='white'
                )
                time_label.pack(anchor='w', pady=(5, 0))
            except:
                time_label = tk.Label(
                    content_frame,
                    text=f"Time Check-out: {check_out_time}",
                    font=("Arial", 10),
                    bg='#4A90E2',
                    fg='white'
                )
                time_label.pack(anchor='w', pady=(5, 0))
        else:
            # Fallback
            current_time = datetime.now().strftime("%I:%M:%S %p")
            time_label = tk.Label(
                content_frame,
                text=f"Time Check-in: {current_time}",
                font=("Arial", 10),
                bg='#4A90E2',
                fg='white'
            )
            time_label.pack(anchor='w', pady=(5, 0))
        
        # Guard information
        guard_info_frame = tk.Frame(content_frame, bg='#4A90E2')
        guard_info_frame.pack(pady=(30, 0))
        
        guard_label = tk.Label(
            guard_info_frame,
            text="Guard in-charge:",
            font=("Arial", 12, "bold"),
            bg='#4A90E2',
            fg='white'
        )
        guard_label.pack(anchor='w')
        
        # Get guard name from stored information or use default
        guard_name = self.current_guard['name'] if self.current_guard else "Unknown Guard"
        
        guard_name_label = tk.Label(
            guard_info_frame,
            text=guard_name,
            font=("Arial", 12),
            bg='#4A90E2',
            fg='white'
        )
        guard_name_label.pack(anchor='w')
    
    def update_status_bar_for_special_pass_active(self):
        """Update status bar to show Log out button for Special Pass active interface"""
        # Clear existing status bar
        for widget in self.status_frame.winfo_children():
            widget.destroy()
        
        # Time section (dark blue)
        now = datetime.now()
        time_str = now.strftime("%I:%M:%S %p")
        self.time_label = tk.Label(
            self.status_frame,
            text=time_str,
            font=("Arial", 12, "bold"),
            bg='#006CB7',  # Blue
            fg='white',
            padx=20,
            pady=10
        )
        self.time_label.pack(side='left', fill='x', expand=True)
        
        # Date section (very dark blue/black)
        date_str = now.strftime("%B %d, %Y")
        self.date_label = tk.Label(
            self.status_frame,
            text=date_str,
            font=("Arial", 12, "bold"),
            bg='#021C37',  # Dark blue
            fg='white',
            padx=20,
            pady=10
        )
        self.date_label.pack(side='left', fill='x', expand=True)
        
        # Log out button (orange)
        logout_button_frame = tk.Frame(
            self.status_frame,
            bg='#EF5E1D',  # Orange
            relief='flat',
            padx=20,
            pady=10
        )
        logout_button_frame.pack(side='left', fill='x', expand=True)
        
        logout_button_label = tk.Label(
            logout_button_frame,
            text="Log out",
            font=("Arial", 12, "bold"),
            bg='#EF5E1D',  # Orange
            fg='white',
            cursor='hand2'
        )
        logout_button_label.pack()
        
        # Bind events to logout button
        logout_button_frame.bind('<Button-1>', self.show_logout_confirmation)
        logout_button_label.bind('<Button-1>', self.show_logout_confirmation)
        
        # Add hover effects
        logout_button_frame.bind('<Enter>', self.on_logout_hover_enter)
        logout_button_frame.bind('<Leave>', self.on_logout_hover_leave)
        logout_button_label.bind('<Enter>', self.on_logout_hover_enter)
        logout_button_label.bind('<Leave>', self.on_logout_hover_leave)
    
    def close_turnstile_action(self):
        """Handle Close the Turnstile button click"""
        print("Close the Turnstile button clicked!")
        
        # Write status to main screen status file to close turnstile
        try:
            with open("main_screen_status.txt", "w") as f:
                f.write("TURNSTILE_CLOSED\n")
                f.write("N/A\n")
                f.write("N/A\n")
                f.write("N/A\n")
            print("Turnstile closed status sent to main screen")
            
            # Verify the file was written correctly
            with open("main_screen_status.txt", "r") as f:
                content = f.read()
                print(f"Status file content written: {repr(content)}")
                
        except Exception as e:
            print(f"Error writing status file: {e}")
        
        # Return to guard interface
        self.show_guard_interface_without_main_screen()

def show_uniform_compliance_interface(self, person_data, detection_result):
    """Show uniform compliance interface based on detection result"""
    print(f"DEBUG: show_uniform_compliance_interface called with detection_result: {detection_result}")
    print(f"DEBUG: person_data: {person_data}")
    
    # Store current interface state
    self.compliance_person_data = person_data
    self.compliance_detection_result = detection_result
    
    # Disable logout button during compliance check
    self.disable_logout_button()
    
    # Clear the main frame but keep header and status bar
    for widget in self.main_frame.winfo_children():
        if widget not in [self.status_frame]:
            widget.destroy()
    
    # Embedded inline Approve/Deny UI (no external popup)
    # Render the compliance UI directly inside the guard screen
    # according to detection_result (clean/manual_verification/violation).
    # This matches the large green/orange buttons layout.
    
    # Render inline Approve/Deny UI directly
    self.create_compliance_header()
    if detection_result == "clean":
        self.create_clean_uniform_interface(person_data)
    elif detection_result == "manual_verification":
        self.create_manual_verification_interface(person_data)
    else:
        self.create_violation_interface(person_data)
    self.update_status_bar_for_compliance()

def create_compliance_header(self):
    """Create the header for compliance interface"""
    # Create top frame to hold both banners
    top_frame = tk.Frame(self.main_frame, bg='white', height=100)
    top_frame.pack(side='top', fill='x')
    top_frame.pack_propagate(False)
    
    # Red banner at top left (spans horizontally)
    red_banner = tk.Frame(top_frame, bg='#EA234C', height=100)
    red_banner.pack(side='left', fill='both', expand=True)
    red_banner.pack_propagate(False)
    
    turnstile_label = tk.Label(
        red_banner,
        text="Turnstile is Closed",
        font=("Arial", 16, "bold"),
        bg='#EA234C',
        fg='white'
    )
    turnstile_label.pack(expand=True)
    
    # Blue banner at top right
    blue_banner = tk.Frame(top_frame, bg='#4A90E2', height=100, width=300)
    blue_banner.pack(side='right', fill='y')
    blue_banner.pack_propagate(False)
    
    # Load and display STI BALAGTAS logo
    try:
        logo_path = os.path.join("image-elements", "STI Balagtas Logo.png")
        logo_image = Image.open(logo_path)
        logo_image = logo_image.resize((80, 60), Image.Resampling.LANCZOS)
        self.compliance_logo_photo = ImageTk.PhotoImage(logo_image)
        
        logo_label = tk.Label(
            blue_banner,
            image=self.compliance_logo_photo,
            bg='#4A90E2'
        )
        logo_label.pack(expand=True, pady=5)
    except Exception as e:
        print(f"Error loading logo: {e}")
        # Fallback to text
        sti_frame = tk.Frame(blue_banner, bg='#4A90E2')
        sti_frame.pack(expand=True, pady=10)
        
        sti_label = tk.Label(
            sti_frame,
            text="STI",
            font=("Arial", 20, "bold"),
            bg='#4A90E2',
            fg='#FFD700'
        )
        sti_label.pack()
        
        balagtas_label = tk.Label(
            sti_frame,
            text="BALAGTAS",
            font=("Arial", 12, "bold"),
            bg='#4A90E2',
            fg='black'
        )
        balagtas_label.pack()

def create_clean_uniform_interface(self, person_data):
    """Create interface for clean uniform (Approve/Deny options)"""
    # Main container
    main_container = tk.Frame(self.main_frame, bg='white')
    main_container.pack(expand=True, fill='both', padx=20, pady=20)
    
    # Left side - Action buttons
    action_frame = tk.Frame(main_container, bg='white')
    action_frame.pack(side='left', fill='both', expand=True, padx=(0, 20))
    
    # Approve button (Green)
    approve_button = tk.Button(
        action_frame,
        text="Approve",
        font=("Arial", 24, "bold"),
        bg='#28a745',
        fg='white',
        relief='flat',
        cursor='hand2',
        command=lambda: self.handle_approve(person_data)
    )
    approve_button.pack(fill='both', expand=True, pady=(0, 10))
    
    # Deny button (Orange)
    deny_button = tk.Button(
        action_frame,
        text="Deny",
        font=("Arial", 24, "bold"),
        bg='#fd7e14',
        fg='white',
        relief='flat',
        cursor='hand2',
        command=lambda: self.handle_deny_clean(person_data)
    )
    deny_button.pack(fill='both', expand=True)
    
    # Right side - Information panel
    info_frame = tk.Frame(main_container, bg='#4A90E2', width=400, height=480)
    info_frame.pack(side='right', fill='y')
    info_frame.pack_propagate(False)
    
    # Profile picture
    self.create_compliance_profile_section(info_frame, person_data)
    
    # Information section
    self.create_compliance_info_section(info_frame)
    
    # Guard in-charge section
    self.create_compliance_guard_section(info_frame)

def create_manual_verification_interface(self, person_data):
    """Create interface for manual verification (Approve/Deny options)"""
    print("DEBUG: create_manual_verification_interface called")
    # Main container
    main_container = tk.Frame(self.main_frame, bg='white')
    main_container.pack(expand=True, fill='both', padx=20, pady=20)
    
    # Left side - Action buttons
    action_frame = tk.Frame(main_container, bg='white')
    action_frame.pack(side='left', fill='both', expand=True, padx=(0, 20))
    
    # Approve button (Green)
    approve_button = tk.Button(
        action_frame,
        text="Approve",
        font=("Arial", 24, "bold"),
        bg='#28a745',
        fg='white',
        command=lambda: self.handle_manual_approve(person_data)
    )
    approve_button.pack(fill='both', expand=True, pady=(0, 10))
    
    # Deny button (Orange)
    deny_button = tk.Button(
        action_frame,
        text="Deny",
        font=("Arial", 24, "bold"),
        bg='#fd7e14',
        fg='white',
        command=lambda: self.handle_manual_deny(person_data)
    )
    deny_button.pack(fill='both', expand=True)
    
    # Right side - Information panel
    info_frame = tk.Frame(main_container, bg='#4A90E2', width=400, height=480)
    info_frame.pack(side='right', fill='y')
    info_frame.pack_propagate(False)
    
    # Profile picture
    self.create_compliance_profile_section(info_frame, person_data)
    
    # Violation info (if any)
    violation_count = self.get_violation_count(person_data['id'])
    if violation_count > 0:
        violation_frame = tk.Frame(info_frame, bg='#fd7e14', height=80)
        violation_frame.pack(side='top', fill='x', pady=(10, 0))
        violation_frame.pack_propagate(False)
        
        violation_label = tk.Label(
            violation_frame,
            text="The student currently has an active violation on record.",
            font=("Arial", 12, "bold"),
            bg='#fd7e14',
            fg='white',
            wraplength=380
        )
        violation_label.pack(expand=True, pady=(10, 5))
        
        count_label = tk.Label(
            violation_frame,
            text=f"Violation Count: {violation_count}",
            font=("Arial", 14, "bold"),
            bg='#fd7e14',
            fg='white'
        )
        count_label.pack(pady=(0, 10))
    
    # Guard info
    guard_frame = tk.Frame(info_frame, bg='#4A90E2')
    guard_frame.pack(side='bottom', fill='x', pady=(0, 20))
    
    guard_label = tk.Label(
        guard_frame,
        text="Guard in-charge:",
        font=("Arial", 16, "bold"),
        bg='#4A90E2',
        fg='white'
    )
    guard_label.pack()
    
    guard_name_label = tk.Label(
        guard_frame,
        text=self.current_guard['name'] if self.current_guard else "Unknown",
        font=("Arial", 14),
        bg='#4A90E2',
        fg='white'
    )
    guard_name_label.pack()

def create_violation_interface(self, person_data):
    """Create interface for uniform violation (Deny Entry only)"""
    # Main container
    main_container = tk.Frame(self.main_frame, bg='white')
    main_container.pack(expand=True, fill='both', padx=20, pady=20)
    
    # Left side - Violation alert and action
    action_frame = tk.Frame(main_container, bg='white')
    action_frame.pack(side='left', fill='both', expand=True, padx=(0, 20))
    
    # Violation alert banner (Yellow)
    violation_banner = tk.Frame(action_frame, bg='#E9DC2D', height=60)
    violation_banner.pack(fill='x', pady=(0, 10))
    violation_banner.pack_propagate(False)
    
    violation_label = tk.Label(
        violation_banner,
        text="Different / Incomplete Uniform Found.",
        font=("Arial", 16, "bold"),
        bg='#E9DC2D',
        fg='black'
    )
    violation_label.pack(expand=True)
    
    # Deny Entry button (Orange)
    deny_entry_button = tk.Button(
        action_frame,
        text="Deny Entry",
        font=("Arial", 24, "bold"),
        bg='#fd7e14',
        fg='white',
        relief='flat',
        cursor='hand2',
        command=lambda: self.handle_deny_violation(person_data)
    )
    deny_entry_button.pack(fill='both', expand=True, pady=(20, 0))
    
    # Report status banner (Red)
    report_banner = tk.Frame(action_frame, bg='#dc3545', height=80)
    report_banner.pack(fill='x', pady=(20, 0))
    report_banner.pack_propagate(False)
    
    report_label = tk.Label(
        report_banner,
        text="Report has been generated.",
        font=("Arial", 14, "bold"),
        bg='#dc3545',
        fg='white'
    )
    report_label.pack(pady=(10, 5))
    
    # Parent notification (Students only)
    if person_data['role'].upper() == 'STUDENT':
        parent_label = tk.Label(
            report_banner,
            text="Parents/Guardian has been also notified.",
            font=("Arial", 12),
            bg='#dc3545',
            fg='white'
        )
        parent_label.pack(pady=(0, 10))
    
    # Right side - Information panel
    info_frame = tk.Frame(main_container, bg='#4A90E2', width=400, height=480)
    info_frame.pack(side='right', fill='y')
    info_frame.pack_propagate(False)
    
    # Profile picture
    self.create_compliance_profile_section(info_frame, person_data)
    
    # Information section
    self.create_compliance_info_section(info_frame)
    
    # Guard in-charge section
    self.create_compliance_guard_section(info_frame)

def create_compliance_profile_section(self, parent, person_data):
    """Create profile picture section for compliance interface"""
    profile_frame = tk.Frame(parent, bg='#4A90E2')
    profile_frame.pack(pady=20)
    
    # Load profile picture
    profile_image = self.load_splash_profile_image(person_data)
    if profile_image:
        # Resize to 2x2 inches (approximately 150x150 pixels)
        profile_image = profile_image.resize((150, 150), Image.Resampling.LANCZOS)
        self.compliance_profile_photo = ImageTk.PhotoImage(profile_image)
        
        profile_label = tk.Label(profile_frame, image=self.compliance_profile_photo, bg='#4A90E2')
        profile_label.pack()
    else:
        # Default profile picture
        default_label = tk.Label(profile_frame, text="No Photo", font=("Arial", 16), 
                               bg='#4A90E2', fg='white', width=10, height=6)
        default_label.pack()
    
    # Name and role
    name_label = tk.Label(profile_frame, text=person_data['name'], 
                         font=("Arial", 18, "bold"), bg='#4A90E2', fg='white')
    name_label.pack(pady=(10, 5))
    
    role_label = tk.Label(profile_frame, text=f"({person_data['role']})", 
                         font=("Arial", 14), bg='#4A90E2', fg='white')
    role_label.pack()

def create_compliance_info_section(self, parent):
    """Create information section for compliance interface"""
    info_frame = tk.Frame(parent, bg='#4A90E2')
    info_frame.pack(pady=20, fill='both', expand=True, padx=20)
    
    # Check-in time
    checkin_time = datetime.now().strftime("%I:%M:%S %p")
    time_label = tk.Label(info_frame, text=f"Time Check-in: {checkin_time}", 
                         font=("Arial", 14), bg='#4A90E2', fg='white')
    time_label.pack(anchor='w')
    
    # Date
    checkin_date = datetime.now().strftime("%B %d, %Y")
    date_label = tk.Label(info_frame, text=f"Date: {checkin_date}", 
                         font=("Arial", 14, "bold"), bg='#4A90E2', fg='white')
    date_label.pack(anchor='w', pady=(10, 0))
    
    # Violation count (if any)
    violation_count = self.get_violation_count(self.compliance_person_data['id'])
    if violation_count > 0:
        violation_frame = tk.Frame(info_frame, bg='#fd7e14', relief='solid', bd=1)
        violation_frame.pack(fill='x', pady=(20, 0))
        
        violation_label = tk.Label(violation_frame, 
                                 text="The student currently has an active violation on record.",
                                 font=("Arial", 12, "bold"), bg='#fd7e14', fg='white')
        violation_label.pack(anchor='w', padx=10, pady=(5, 0))
        
        count_label = tk.Label(violation_frame, 
                             text=f"Violation Count: {violation_count}",
                             font=("Arial", 12), bg='#fd7e14', fg='white')
        count_label.pack(anchor='w', padx=10, pady=(0, 5))

def create_compliance_guard_section(self, parent):
    """Create guard in-charge section for compliance interface"""
    guard_frame = tk.Frame(parent, bg='#4A90E2')
    guard_frame.pack(pady=20, fill='x', padx=20)
    
    # Guard in-charge label
    guard_label = tk.Label(guard_frame, text="Guard in-charge:", 
                          font=("Arial", 14, "bold"), bg='#4A90E2', fg='white')
    guard_label.pack(anchor='w')
    
    # Get guard name from stored information or use default
    guard_name = self.current_guard['name'] if self.current_guard else "Unknown Guard"
    
    # Guard name
    guard_name_label = tk.Label(guard_frame, text=guard_name, 
                               font=("Arial", 14), bg='#4A90E2', fg='white')
    guard_name_label.pack(anchor='w', pady=(5, 0))

def update_status_bar_for_compliance(self):
    """Update status bar for compliance interface"""
    # Clear existing status bar
    for widget in self.status_frame.winfo_children():
        widget.destroy()
    
    # Time section (dark blue)
    now = datetime.now()
    time_str = now.strftime("%I:%M:%S %p")
    self.time_label = tk.Label(
        self.status_frame,
        text=time_str,
        font=("Arial", 12, "bold"),
        bg='#006CB7',  # Blue
        fg='white',
        padx=20,
        pady=10
    )
    self.time_label.pack(side='left', fill='x', expand=True)
    
    # Date section (very dark blue/black)
    date_str = now.strftime("%B %d, %Y")
    self.date_label = tk.Label(
        self.status_frame,
        text=date_str,
        font=("Arial", 12, "bold"),
        bg='#021C37',  # Dark blue
        fg='white',
        padx=20,
        pady=10
    )
    self.date_label.pack(side='left', fill='x', expand=True)
    
    # Log out button (orange) - will be disabled
    logout_button_frame = tk.Frame(
        self.status_frame,
        bg='#EF5E1D',  # Orange
        relief='flat',
        padx=20,
        pady=10
    )
    logout_button_frame.pack(side='left', fill='x', expand=True)
    
    logout_button_label = tk.Label(
        logout_button_frame,
        text="Log out",
        font=("Arial", 12, "bold"),
        bg='#EF5E1D',  # Orange
        fg='white',
        cursor='hand2'
    )
    logout_button_label.pack()
    
    # Store references to logout button elements for enabling/disabling
    self.logout_button_frame = logout_button_frame
    self.logout_button_label = logout_button_label
    
    # Bind events to logout button
    logout_button_frame.bind('<Button-1>', self.show_logout_confirmation)
    logout_button_label.bind('<Button-1>', self.show_logout_confirmation)
    
    # Add hover effects
    logout_button_frame.bind('<Enter>', self.on_logout_hover_enter)
    logout_button_frame.bind('<Leave>', self.on_logout_hover_leave)
    logout_button_label.bind('<Enter>', self.on_logout_hover_enter)
    logout_button_label.bind('<Leave>', self.on_logout_hover_leave)

def handle_approve(self, person_data):
    """Handle approve action for clean uniform"""
    # Launch guard confirmation window (approve-button.py). When it exits with
    # a successful click, proceed to the approval splash for 5 seconds.
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        approve_path = os.path.join(current_dir, "approve-button.py")
        print("Launching guard approve/deny window...")
        result = subprocess.run([sys.executable, approve_path], capture_output=True, text=True)
        output = (result.stdout or "") + ("\n" + result.stderr if result.stderr else "")
        print(output.strip())
        if "Approve Button Clicked" in output:
            # Notify main screen to show student/teacher info similar to special pass
            try:
                current_time = datetime.now().strftime("%I:%M:%S %p")
                guard_name = self.current_guard['name'] if self.current_guard else "Unknown Guard"
                person_name = person_data.get('name', 'Unknown')
                person_role = person_data.get('role', 'USER')
                with open("main_screen_status.txt", "w") as f:
                    f.write("STUDENT_TEACHER_APPROVED\n")
                    f.write(f"{person_name}\n")
                    f.write(f"{person_role}\n")
                    f.write(f"{current_time}\n")
                    f.write(f"{guard_name}\n")
            except Exception as _e:
                print(f"Error writing student/teacher approved status: {_e}")
            # Guard approved – show approval splash
            self.show_approval_interface(person_data)
        else:
            # Treat deny or window close as denial
            self.show_denial_message(person_data, "Access denied by guard.")
    except Exception as e:
        print(f"Error launching approve-button: {e}")
        # Fallback straight to approval interface to avoid blocking operations
        self.show_approval_interface(person_data)

def handle_deny_clean(self, person_data):
    """Handle deny action for clean uniform"""
    # Add violation count
    self.add_violation(person_data['id'])
    
    # Show violation interface (Different/Incomplete Uniform Found)
    self.show_violation_interface(person_data)

def handle_manual_approve(self, person_data):
    """Handle approve action for manual verification"""
    # Same guard confirmation flow as clean approve
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        approve_path = os.path.join(current_dir, "approve-button.py")
        print("Launching guard approve/deny window (manual verification)...")
        result = subprocess.run([sys.executable, approve_path], capture_output=True, text=True)
        output = (result.stdout or "") + ("\n" + result.stderr if result.stderr else "")
        print(output.strip())
        if "Approve Button Clicked" in output:
            # Notify main screen to show student/teacher info similar to special pass
            try:
                current_time = datetime.now().strftime("%I:%M:%S %p")
                guard_name = self.current_guard['name'] if self.current_guard else "Unknown Guard"
                person_name = person_data.get('name', 'Unknown')
                person_role = person_data.get('role', 'USER')
                with open("main_screen_status.txt", "w") as f:
                    f.write("STUDENT_TEACHER_APPROVED\n")
                    f.write(f"{person_name}\n")
                    f.write(f"{person_role}\n")
                    f.write(f"{current_time}\n")
                    f.write(f"{guard_name}\n")
            except Exception as _e:
                print(f"Error writing student/teacher approved status: {_e}")
            self.show_approval_interface(person_data)
        else:
            self.show_denial_message(person_data, "Access denied by guard.")
    except Exception as e:
        print(f"Error launching approve-button: {e}")
        self.show_approval_interface(person_data)

def handle_manual_deny(self, person_data):
    """Handle deny action for manual verification"""
    # Add violation count
    self.add_violation(person_data['id'])
    
    # Show violation interface (Different/Incomplete Uniform Found)
    self.show_violation_interface(person_data)

def handle_deny_violation(self, person_data):
    """Handle deny action for uniform violation"""
    # No additional violation count for uniform violations
    # Show denial message for 5 seconds
    self.show_denial_message(person_data, "Access denied due to uniform violation.")

def show_approval_interface(self, person_data):
    """Show approval interface for 5 seconds"""
    # Clear main content
    for widget in self.main_frame.winfo_children():
        if widget not in [self.status_frame]:
            widget.destroy()
    
    # Create approval header (Turnstile is Open)
    self.create_approval_header()
    
    # Create approval content
    self.create_approval_content(person_data)
    
    # Auto-close after 5 seconds
    self.main_frame.after(5000, self.close_approval_and_restore)

def create_approval_header(self):
    """Create the header for approval interface (Turnstile is Open)"""
    # Create top frame to hold both banners
    top_frame = tk.Frame(self.main_frame, bg='white', height=100)
    top_frame.pack(side='top', fill='x')
    top_frame.pack_propagate(False)
    
    # Light green banner at top left (spans horizontally)
    green_banner = tk.Frame(top_frame, bg='#90EE90', height=60)
    green_banner.pack(side='left', fill='both', expand=True)
    green_banner.pack_propagate(False)
    
    turnstile_label = tk.Label(
        green_banner,
        text="Turnstile is Open",
        font=("Arial", 16, "bold"),
        bg='#90EE90',
        fg='black'
    )
    turnstile_label.pack(expand=True)
    
    # Blue banner at top right
    blue_banner = tk.Frame(top_frame, bg='#4A90E2', height=100, width=300)
    blue_banner.pack(side='right', fill='y')
    blue_banner.pack_propagate(False)
    
    # Load and display STI BALAGTAS logo
    try:
        logo_path = os.path.join("image-elements", "STI Balagtas Logo.png")
        logo_image = Image.open(logo_path)
        logo_image = logo_image.resize((80, 60), Image.Resampling.LANCZOS)
        self.approval_logo_photo = ImageTk.PhotoImage(logo_image)
        
        logo_label = tk.Label(
            blue_banner,
            image=self.approval_logo_photo,
            bg='#4A90E2'
        )
        logo_label.pack(expand=True, pady=5)
    except Exception as e:
        print(f"Error loading logo: {e}")
        # Fallback to text
        sti_frame = tk.Frame(blue_banner, bg='#4A90E2')
        sti_frame.pack(expand=True, pady=10)
        
        sti_label = tk.Label(
            sti_frame,
            text="STI",
            font=("Arial", 20, "bold"),
            bg='#4A90E2',
            fg='#FFD700'
        )
        sti_label.pack()
        
        balagtas_label = tk.Label(
            sti_frame,
            text="BALAGTAS",
            font=("Arial", 12, "bold"),
            bg='#4A90E2',
            fg='black'
        )
        balagtas_label.pack()

def create_approval_content(self, person_data):
    """Create approval content with status bar and Deny Entry option"""
    # Status bar below header
    status_bar = tk.Frame(self.main_frame, bg='white', height=40)
    status_bar.pack(fill='x')
    status_bar.pack_propagate(False)
    
    # User Identity Verified (Light Blue)
    verified_frame = tk.Frame(status_bar, bg='#87CEEB', height=40)
    verified_frame.pack(side='left', fill='both', expand=True)
    verified_frame.pack_propagate(False)
    
    verified_label = tk.Label(
        verified_frame,
        text="User Identity Verified.",
        font=("Arial", 12, "bold"),
        bg='#87CEEB',
        fg='black'
    )
    verified_label.pack(expand=True)
    
    # Deny Entry button (Orange)
    deny_entry_frame = tk.Frame(status_bar, bg='#fd7e14', height=40)
    deny_entry_frame.pack(side='right', fill='y')
    deny_entry_frame.pack_propagate(False)
    
    deny_entry_button = tk.Button(
        deny_entry_frame,
        text="Deny Entry",
        font=("Arial", 12, "bold"),
        bg='#fd7e14',
        fg='white',
        relief='flat',
        cursor='hand2',
        command=lambda: self.handle_deny_after_approval(person_data)
    )
    deny_entry_button.pack(expand=True)
    
    # Main content area
    main_container = tk.Frame(self.main_frame, bg='white')
    main_container.pack(expand=True, fill='both', padx=20, pady=20)
    
    # AI-niform logo
    logo_frame = tk.Frame(main_container, bg='white')
    logo_frame.pack(expand=True)
    
    ai_label = tk.Label(
        logo_frame,
        text="AI-",
        font=("Arial", 48, "bold"),
        bg='white',
        fg='#87CEEB'
    )
    ai_label.pack(side='left')
    
    niform_label = tk.Label(
        logo_frame,
        text="niform",
        font=("Arial", 48, "bold"),
        bg='white',
        fg='#333333'
    )
    niform_label.pack(side='left')
    
    # Right side - Information panel
    info_frame = tk.Frame(main_container, bg='#4A90E2', width=400, height=480)
    info_frame.pack(side='right', fill='y')
    info_frame.pack_propagate(False)
    
    # Profile picture
    self.create_compliance_profile_section(info_frame, person_data)
    
    # Information section
    self.create_compliance_info_section(info_frame)
    
    # Guard in-charge section
    self.create_compliance_guard_section(info_frame)

def handle_deny_after_approval(self, person_data):
    """Handle deny action after approval (adds violation count)"""
    # Add violation count
    self.add_violation(person_data['id'])
    
    # Show denial message for 5 seconds
    self.show_denial_message(person_data, "Access denied after approval.")

def show_violation_interface(self, person_data):
    """Show violation interface (Different/Incomplete Uniform Found)"""
    # Clear main content
    for widget in self.main_frame.winfo_children():
        if widget not in [self.status_frame]:
            widget.destroy()
    
    # Create violation header (Turnstile is Open)
    self.create_violation_header()
    
    # Create violation content
    self.create_violation_content(person_data)
    
    # Auto-close after 5 seconds
    self.main_frame.after(5000, self.close_violation_and_restore)

def create_violation_header(self):
    """Create the header for violation interface (Turnstile is Open)"""
    # Create top frame to hold both banners
    top_frame = tk.Frame(self.main_frame, bg='white', height=100)
    top_frame.pack(side='top', fill='x')
    top_frame.pack_propagate(False)
    
    # Light green banner at top left (spans horizontally)
    green_banner = tk.Frame(top_frame, bg='#90EE90', height=60)
    green_banner.pack(side='left', fill='both', expand=True)
    green_banner.pack_propagate(False)
    
    turnstile_label = tk.Label(
        green_banner,
        text="Turnstile is Open",
        font=("Arial", 16, "bold"),
        bg='#90EE90',
        fg='black'
    )
    turnstile_label.pack(expand=True)
    
    # Blue banner at top right
    blue_banner = tk.Frame(top_frame, bg='#4A90E2', height=100, width=300)
    blue_banner.pack(side='right', fill='y')
    blue_banner.pack_propagate(False)
    
    # Load and display STI BALAGTAS logo
    try:
        logo_path = os.path.join("image-elements", "STI Balagtas Logo.png")
        logo_image = Image.open(logo_path)
        logo_image = logo_image.resize((80, 60), Image.Resampling.LANCZOS)
        self.violation_logo_photo = ImageTk.PhotoImage(logo_image)
        
        logo_label = tk.Label(
            blue_banner,
            image=self.violation_logo_photo,
            bg='#4A90E2'
        )
        logo_label.pack(expand=True, pady=5)
    except Exception as e:
        print(f"Error loading logo: {e}")
        # Fallback to text
        sti_frame = tk.Frame(blue_banner, bg='#4A90E2')
        sti_frame.pack(expand=True, pady=10)
        
        sti_label = tk.Label(
            sti_frame,
            text="STI",
            font=("Arial", 20, "bold"),
            bg='#4A90E2',
            fg='#FFD700'
        )
        sti_label.pack()
        
        balagtas_label = tk.Label(
            sti_frame,
            text="BALAGTAS",
            font=("Arial", 12, "bold"),
            bg='#4A90E2',
            fg='black'
        )
        balagtas_label.pack()

def create_violation_content(self, person_data):
    """Create violation content with status bars and Deny Entry option"""
    # Status bar below header
    status_bar = tk.Frame(self.main_frame, bg='white', height=40)
    status_bar.pack(fill='x')
    status_bar.pack_propagate(False)
    
    # Different/Incomplete Uniform Found (Yellow)
    violation_frame = tk.Frame(status_bar, bg='#E9DC2D', height=40)
    violation_frame.pack(side='left', fill='both', expand=True)
    violation_frame.pack_propagate(False)
    
    violation_label = tk.Label(
        violation_frame,
        text="Different / Incomplete Uniform Found.",
        font=("Arial", 12, "bold"),
        bg='#E9DC2D',
        fg='black'
    )
    violation_label.pack(expand=True)
    
    # Deny Entry button (Red)
    deny_entry_frame = tk.Frame(status_bar, bg='#dc3545', height=40)
    deny_entry_frame.pack(side='right', fill='y')
    deny_entry_frame.pack_propagate(False)
    
    deny_entry_button = tk.Button(
        deny_entry_frame,
        text="Deny Entry",
        font=("Arial", 12, "bold"),
        bg='#dc3545',
        fg='white',
        relief='flat',
        cursor='hand2',
        command=lambda: self.handle_deny_violation(person_data)
    )
    deny_entry_button.pack(expand=True)
    
    # Report status banner (Red)
    report_banner = tk.Frame(self.main_frame, bg='#dc3545', height=80)
    report_banner.pack(fill='x')
    report_banner.pack_propagate(False)
    
    report_label = tk.Label(
        report_banner,
        text="Report has been generated.",
        font=("Arial", 14, "bold"),
        bg='#dc3545',
        fg='white'
    )
    report_label.pack(pady=(10, 5))
    
    # Parent notification (Students only)
    if person_data['role'].upper() == 'STUDENT':
        parent_label = tk.Label(
            report_banner,
            text="Parents/Guardian has been also notified.",
            font=("Arial", 12),
            bg='#dc3545',
            fg='white'
        )
        parent_label.pack(pady=(0, 10))
    
    # Main content area
    main_container = tk.Frame(self.main_frame, bg='white')
    main_container.pack(expand=True, fill='both', padx=20, pady=20)
    
    # AI-niform logo
    logo_frame = tk.Frame(main_container, bg='white')
    logo_frame.pack(expand=True)
    
    ai_label = tk.Label(
        logo_frame,
        text="AI-",
        font=("Arial", 48, "bold"),
        bg='white',
        fg='#87CEEB'
    )
    ai_label.pack(side='left')
    
    niform_label = tk.Label(
        logo_frame,
        text="niform",
        font=("Arial", 48, "bold"),
        bg='white',
        fg='#333333'
    )
    niform_label.pack(side='left')
    
    # Right side - Information panel
    info_frame = tk.Frame(main_container, bg='#4A90E2', width=400, height=480)
    info_frame.pack(side='right', fill='y')
    info_frame.pack_propagate(False)
    
    # Profile picture
    self.create_compliance_profile_section(info_frame, person_data)
    
    # Information section
    self.create_compliance_info_section(info_frame)
    
    # Guard in-charge section
    self.create_compliance_guard_section(info_frame)

def close_violation_and_restore(self):
    """Close violation interface and restore guard interface"""
    # Enable logout button
    self.enable_logout_button()
    
    # Restore the guard interface
    self.show_guard_interface()

def show_denial_message(self, person_data, reason):
    """Show denial message for 5 seconds"""
    # Clear main content
    for widget in self.main_frame.winfo_children():
        if widget not in [self.status_frame]:
            widget.destroy()
    
    # Create denial header (Turnstile is Closed)
    self.create_compliance_header()
    
    # Create denial content
    self.create_denial_content(person_data, reason)
    
    # Auto-close after 5 seconds
    self.main_frame.after(5000, self.close_compliance_and_restore)

def create_denial_content(self, person_data, reason):
    """Create denial content"""
    # Main container
    main_container = tk.Frame(self.main_frame, bg='white')
    main_container.pack(expand=True, fill='both', padx=20, pady=20)
    
    # Left side - Denial message
    message_frame = tk.Frame(main_container, bg='white')
    message_frame.pack(side='left', fill='both', expand=True, padx=(0, 20))
    
    # Denial message
    denial_label = tk.Label(
        message_frame,
        text=reason,
        font=("Arial", 24, "bold"),
        bg='white',
        fg='#dc3545'
    )
    denial_label.pack(expand=True)
    
    # Right side - Information panel
    info_frame = tk.Frame(main_container, bg='#4A90E2', width=400, height=480)
    info_frame.pack(side='right', fill='y')
    info_frame.pack_propagate(False)
    
    # Profile picture
    self.create_compliance_profile_section(info_frame, person_data)
    
    # Information section
    self.create_compliance_info_section(info_frame)
    
    # Guard in-charge section
    self.create_compliance_guard_section(info_frame)

def close_approval_and_restore(self):
    """Close approval interface and restore guard interface"""
    # Enable logout button
    self.enable_logout_button()
    
    # Restore the guard interface
    self.show_guard_interface()

def close_compliance_and_restore(self):
    """Close compliance interface and restore guard interface"""
    # Enable logout button
    self.enable_logout_button()
    
    # Restore the guard interface
    self.show_guard_interface()

def get_violation_count(self, person_id):
    """Get violation count for a person"""
    try:
        violations_file = "violations.txt"
        if not os.path.exists(violations_file):
            return 0
        
        with open(violations_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line.startswith('#') or not line:
                    continue
                
                parts = line.split(',')
                if len(parts) >= 2:
                    db_id = parts[0]
                    count = int(parts[1])
                    
                    if db_id == person_id:
                        return count
        
        return 0
    except Exception as e:
        print(f"Error getting violation count: {e}")
        return 0

def add_violation(self, person_id):
    """Add a violation for a person"""
    try:
        violations_file = "violations.txt"
        
        # Read existing violations
        violations = {}
        if os.path.exists(violations_file):
            with open(violations_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith('#') or not line:
                        continue
                    
                    parts = line.split(',')
                    if len(parts) >= 2:
                        db_id = parts[0]
                        count = int(parts[1])
                        violations[db_id] = count
        
        # Add or increment violation count
        if person_id in violations:
            violations[person_id] += 1
        else:
            violations[person_id] = 1
        
        # Write back to file
        with open(violations_file, 'w') as f:
            f.write("# Person ID, Violation Count\n")
            for db_id, count in violations.items():
                f.write(f"{db_id},{count}\n")
        
        print(f"Added violation for {person_id}. New count: {violations[person_id]}")
        
    except Exception as e:
        print(f"Error adding violation: {e}")



def show_no_object_splash(self):
    """Show splash screen when no objects are detected"""
    # Stop camera feed
    self.splash_is_running = False
    if self.splash_camera_detector:
        self.splash_camera_detector.cleanup()
    
    # Clear current splash content
    for widget in self.main_frame.winfo_children():
        if widget != self.status_frame:
            widget.destroy()
    
    # Create header (Turnstile is Closed + Guard in-charge)
    self.create_splash_header()
    
    # Create no object splash content
    self.create_no_object_splash_content()
    
    # Auto-close after 5 seconds
    self.main_frame.after(5000, self.close_no_object_splash)
    
    # Bind escape key to close
    self.root.bind('<Escape>', lambda e: self.close_no_object_splash())

def create_no_object_splash_content(self):
    """Create the no object splash screen content"""
    # Main container
    main_container = tk.Frame(self.main_frame, bg='white')
    main_container.pack(expand=True, fill='both', padx=20, pady=20)
    
    # Left side - No detection message
    message_frame = tk.Frame(main_container, bg='#f0f0f0', width=640, height=480)
    message_frame.pack(side='left', padx=(0, 20))
    message_frame.pack_propagate(False)
    
    # No detection icon/message
    no_detection_label = tk.Label(message_frame, 
                                 text="🔍\n\nNo Objects Detected", 
                                 font=("Arial", 24, "bold"), 
                                 bg='#f0f0f0', fg='#666666',
                                 justify='center')
    no_detection_label.pack(expand=True)
    
    # Subtitle
    subtitle_label = tk.Label(message_frame, 
                             text="Please ensure proper positioning\nand lighting for detection", 
                             font=("Arial", 14), 
                             bg='#f0f0f0', fg='#888888',
                             justify='center')
    subtitle_label.pack(pady=(0, 20))
    
    # Right side - Information panel
    info_frame = tk.Frame(main_container, bg='#4A90E2', width=400, height=480)
    info_frame.pack(side='right', fill='y')
    info_frame.pack_propagate(False)
    
    # Profile picture
    self.create_no_object_profile_section(info_frame)
    
    # Information section
    self.create_no_object_info_section(info_frame)
    
    # Status section
    self.create_no_object_status_section(info_frame)

def create_no_object_profile_section(self, parent):
    """Create profile picture section for no object splash"""
    profile_frame = tk.Frame(parent, bg='#4A90E2')
    profile_frame.pack(pady=20)
    
    # Load profile picture for compliance person data
    profile_image = self.load_profile_image_for_compliance()
    if profile_image:
        # Resize to 2x2 inches (approximately 150x150 pixels)
        profile_image = profile_image.resize((150, 150), Image.Resampling.LANCZOS)
        self.no_object_profile_photo = ImageTk.PhotoImage(profile_image)
        
        profile_label = tk.Label(profile_frame, image=self.no_object_profile_photo, bg='#4A90E2')
        profile_label.pack()
    else:
        # Default profile picture
        default_label = tk.Label(profile_frame, text="No Photo", font=("Arial", 16), 
                               bg='#4A90E2', fg='white', width=10, height=6)
        default_label.pack()
    
    # Name and role
    name_label = tk.Label(profile_frame, text=self.compliance_person_data['name'], 
                         font=("Arial", 18, "bold"), bg='#4A90E2', fg='white')
    name_label.pack(pady=(10, 5))
    
    role_label = tk.Label(profile_frame, text=f"({self.compliance_person_data['role']})", 
                         font=("Arial", 14), bg='#4A90E2', fg='white')
    role_label.pack()

def create_no_object_info_section(self, parent):
    """Create information section for no object splash"""
    info_frame = tk.Frame(parent, bg='#4A90E2')
    info_frame.pack(pady=20, fill='x', padx=20)
    
    # Check-in time
    checkin_time = datetime.datetime.now().strftime("%I:%M:%S %p")
    time_label = tk.Label(info_frame, text=f"Time Check-in: {checkin_time}", 
                         font=("Arial", 14), bg='#4A90E2', fg='white')
    time_label.pack(anchor='w')
    
    # Date
    checkin_date = datetime.datetime.now().strftime("%B %d, %Y")
    date_label = tk.Label(info_frame, text=f"Date: {checkin_date}", 
                         font=("Arial", 14), bg='#4A90E2', fg='white')
    date_label.pack(anchor='w', pady=(5, 0))

def create_no_object_status_section(self, parent):
    """Create status section for no object splash"""
    status_frame = tk.Frame(parent, bg='#FF6B35')  # Orange background for warning
    status_frame.pack(pady=20, fill='x', padx=20)
    
    # Status message
    status_label = tk.Label(status_frame, text="⚠ Detection Status", 
                           font=("Arial", 16, "bold"), bg='#FF6B35', fg='white')
    status_label.pack(anchor='w')
    
    # Status details
    details_label = tk.Label(status_frame, text="No objects detected in camera view.\nPlease check positioning and try again.", 
                            font=("Arial", 12), bg='#FF6B35', fg='white',
                            justify='left')
    details_label.pack(anchor='w', pady=(5, 0))

def close_no_object_splash(self):
    """Close the no object splash screen and show student check-in interface"""
    # Unbind escape key
    try:
        self.root.unbind('<Escape>')
    except:
        pass
    
    # Show the student check-in interface (approval interface) instead of returning to guard interface
    if hasattr(self, 'compliance_person_data') and self.compliance_person_data:
        print("No objects detected - showing student check-in interface")
        self.show_approval_interface(self.compliance_person_data)
    else:
        # Fallback to guard interface if no person data available
        self.show_guard_interface()



def main():
    root = tk.Tk()
    app = AINiformLogin(root)
    
    # Window is already locked to 1366x768 in __init__
    
    # Start the application
    root.mainloop()

if __name__ == "__main__":
    main()
