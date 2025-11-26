import cv2
import numpy as np
import time
from ultralytics import YOLO
import argparse

class YOLOCameraDetection:
    def __init__(self, model_path='best.pt', camera_id=0, confidence_threshold=0.5):
        """
        Initialize YOLO Camera Detection
        
        Args:
            model_path (str): Path to YOLO model file
            camera_id (int): Camera device ID (usually 1 for default camera)
            confidence_threshold (float): Minimum confidence for detection
        """
        self.model_path = model_path
        self.camera_id = camera_id
        self.confidence_threshold = confidence_threshold
        self.cap = None
        self.model = None
        
    def load_model(self):
        """Load YOLO model"""
        try:
            print(f"Loading YOLO model from {self.model_path}...")
            self.model = YOLO(self.model_path)
            print("Model loaded successfully!")
            return True
        except Exception as e:
            print(f"Error loading model: {e}")
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
            
            return detections
        except Exception as e:
            print(f"Error during detection: {e}")
            return []
    
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
    
    def add_info_panel(self, frame, fps, detection_count):
        """Add information panel to frame"""
        # Create info panel background
        cv2.rectangle(frame, (10, 10), (300, 80), (0, 0, 0), -1)
        cv2.rectangle(frame, (10, 10), (300, 80), (255, 255, 255), 2)
        
        # Add text information
        cv2.putText(frame, f"FPS: {fps:.1f}", (20, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(frame, f"Detections: {detection_count}", (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        return frame
    
    def run_detection(self):
        """Main detection loop"""
        if not self.load_model():
            return
        
        if not self.initialize_camera():
            return
        
        print("Starting YOLO camera detection...")
        print("Press 'q' to quit, 's' to save screenshot")
        
        frame_count = 0
        start_time = time.time()
        
        try:
            while True:
                # Capture frame
                ret, frame = self.cap.read()
                if not ret:
                    print("Error: Could not read frame")
                    break
                
                # Calculate FPS
                frame_count += 1
                if frame_count % 30 == 0:
                    current_time = time.time()
                    fps = 30 / (current_time - start_time)
                    start_time = current_time
                else:
                    fps = 0
                
                # Perform object detection
                detections = self.detect_objects(frame)
                
                # Draw detections
                frame = self.draw_detections(frame, detections)
                
                # Add info panel
                frame = self.add_info_panel(frame, fps, len(detections))
                
                # Display frame
                cv2.imshow('YOLO Camera Detection', frame)
                
                # Handle key presses
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    print("Quitting...")
                    break
                elif key == ord('s'):
                    # Save screenshot
                    timestamp = time.strftime("%Y%m%d_%H%M%S")
                    filename = f"yolo_detection_{timestamp}.jpg"
                    cv2.imwrite(filename, frame)
                    print(f"Screenshot saved as {filename}")
                
        except KeyboardInterrupt:
            print("\nInterrupted by user")
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean up resources"""
        if self.cap is not None:
            self.cap.release()
        cv2.destroyAllWindows()
        print("Cleanup completed")

def main():
    parser = argparse.ArgumentParser(description='YOLO Camera Object Detection')
    parser.add_argument('--model', type=str, default='best.pt', 
                       help='Path to YOLO model file (default: best.pt - your custom model)')
    parser.add_argument('--camera', type=int, default=0, 
                       help='Camera device ID (default: 1)')
    parser.add_argument('--confidence', type=float, default=0.5, 
                       help='Confidence threshold (default: 0.5)')
    
    args = parser.parse_args()
    
    # Create and run detection
    detector = YOLOCameraDetection(
        model_path=args.model,
        camera_id=args.camera,
        confidence_threshold=args.confidence
    )
    
    detector.run_detection()

if __name__ == "__main__":
    main()
