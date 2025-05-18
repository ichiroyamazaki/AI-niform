import cv2
import time
import numpy as np
import logging
import tensorflow as tf
import os
import sys

# Set up logging with a custom format that removes the prefix
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s'  # Only show the message without prefix
)
logger = logging.getLogger(__name__)

# Constants
INPUT_SIZE = 224  # Reduced from 300 to 224 for better performance
CONFIDENCE_THRESHOLD = 0.95  # Adjusted recognition rate
TIMEOUT_SECONDS = 10
TARGET_FPS = 30
FRAME_SKIP_THRESHOLD = 1.0 / TARGET_FPS  # Time threshold for frame skipping
REQUIRED_DETECTIONS = 3  # Number of unique objects needed for early termination
QUICK_DETECTION_TIMEOUT = 3  # Time limit for quick detection in seconds
TRACKING_HISTORY = 5  # Number of frames to keep in tracking history
MOTION_THRESHOLD = 30  # Minimum pixel movement to consider as motion

# Model paths
SAVED_MODEL_PATH = "/Users/ichiroyamazaki/Documents/AIniform/ainiform-model-alpha-v1/converted_savedmodel/model.savedmodel"
KERAS_MODEL_PATH = "/Users/ichiroyamazaki/Documents/AIniform/ainiform-model-alpha-v1/converted_keras/keras_model.h5"
LABELS_PATH = "/Users/ichiroyamazaki/Documents/AIniform/ainiform-model-alpha-v1/converted_savedmodel/labels.txt"

# Custom class names
CLASSES = {
    3: 'ict-gray-polo',
    4: 'ict-pants',
    10: 'ict-skirt'
}

# Custom DepthwiseConv2D layer to handle the 'groups' parameter
class CustomDepthwiseConv2D(tf.keras.layers.DepthwiseConv2D):
    def __init__(self, *args, **kwargs):
        # Remove the 'groups' parameter if it exists
        kwargs.pop('groups', None)
        super().__init__(*args, **kwargs)

# Add tracking state
class ObjectTracker:
    def __init__(self):
        self.history = []
        self.current_box = None
        self.last_detection_time = 0
        self.is_tracking = False
    
    def update(self, new_box, confidence, current_time):
        if new_box is None:
            if self.is_tracking and (current_time - self.last_detection_time) < 1.0:  # Keep tracking for 1 second
                return self.current_box
            self.is_tracking = False
            return None
            
        self.last_detection_time = current_time
        
        if not self.is_tracking:
            self.current_box = new_box
            self.history = [new_box]
            self.is_tracking = True
            return new_box
            
        # Calculate center points
        old_center = ((self.current_box['x1'] + self.current_box['x2']) // 2,
                     (self.current_box['y1'] + self.current_box['y2']) // 2)
        new_center = ((new_box['x1'] + new_box['x2']) // 2,
                     (new_box['y1'] + new_box['y2']) // 2)
        
        # Calculate movement
        dx = new_center[0] - old_center[0]
        dy = new_center[1] - old_center[1]
        
        # Smooth the movement
        if abs(dx) > MOTION_THRESHOLD or abs(dy) > MOTION_THRESHOLD:
            # If movement is too large, use the new box directly
            self.current_box = new_box
        else:
            # Smooth the movement
            self.current_box = {
                'x1': self.current_box['x1'] + dx,
                'y1': self.current_box['y1'] + dy,
                'x2': self.current_box['x2'] + dx,
                'y2': self.current_box['y2'] + dy
            }
        
        # Update history
        self.history.append(self.current_box)
        if len(self.history) > TRACKING_HISTORY:
            self.history.pop(0)
            
        return self.current_box

def load_labels():
    """Load the class labels from the labels.txt file"""
    try:
        with open(LABELS_PATH, 'r') as f:
            labels = [line.strip() for line in f.readlines()]
        return {i: label for i, label in enumerate(labels)}
    except Exception as e:
        logger.error(f'Error loading labels: {str(e)}')
        raise

def load_model():
    """Load the custom model using TensorFlow's SavedModel loader"""
    logger.info('Loading custom model...')
    try:
        # Load the SavedModel with custom objects
        custom_objects = {
            'DepthwiseConv2D': CustomDepthwiseConv2D
        }
        model = tf.keras.models.load_model(KERAS_MODEL_PATH, custom_objects=custom_objects)
        logger.info('Model loaded successfully')
        return model
    except Exception as e:
        logger.error(f'Error loading model: {str(e)}')
        raise

def process_output(detections, frame):
    """Process output from Teachable Machine model"""
    # predictions is already a numpy array
    predictions = detections
    
    # Get the class with highest probability among ICT classes only
    ict_probs = {i: predictions[0][i] for i in CLASSES.keys()}
    if not ict_probs:
        return None, 0.0, None
        
    class_id = max(ict_probs.items(), key=lambda x: x[1])[0]
    confidence = predictions[0][class_id]
    
    if confidence > CONFIDENCE_THRESHOLD and class_id in CLASSES:
        detected_class = CLASSES[class_id]
        print(f"DETECTED: {detected_class}")  # Keep this print for direct output
        # Create bounding box coordinates
        height, width = frame.shape[:2]
        box = {
            'x1': int(width * 0.1),  # 10% from left
            'y1': int(height * 0.1),  # 10% from top
            'x2': int(width * 0.9),  # 90% from left
            'y2': int(height * 0.9)   # 90% from top
        }
        return class_id, confidence, box
    else:
        return None, 0.0, None

def draw_detection(frame, class_name, confidence, box):
    """Draw bounding box and label on the frame"""
    if box is None:
        return frame
        
    # Draw bounding box
    cv2.rectangle(frame, (box['x1'], box['y1']), (box['x2'], box['y2']), (0, 255, 0), 2)
    
    # Prepare label text
    label = f'{class_name}: {confidence:.2f}'
    
    # Get text size for background rectangle
    (text_width, text_height), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
    
    # Draw background rectangle for text
    cv2.rectangle(frame, 
                 (box['x1'], box['y1'] - text_height - 10),
                 (box['x1'] + text_width + 10, box['y1']),
                 (0, 255, 0), -1)
    
    # Draw text
    cv2.putText(frame, label,
                (box['x1'] + 5, box['y1'] - 5),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
    
    return frame

def main():
    # Accept camera index as argument
    if len(sys.argv) > 1:
        camera_index = int(sys.argv[1])
    else:
        camera_index = 1

    # Load labels
    logger.info('Loading labels...')
    try:
        CLASSES = load_labels()
        logger.info('Labels loaded successfully')
        logger.info(f"Number of classes loaded: {len(CLASSES)}")
    except Exception as e:
        logger.error(f'Error loading labels: {str(e)}')
        return

    # Load model
    logger.info('Loading model...')
    try:
        model = load_model()
        logger.info('Model loaded successfully')
    except Exception as e:
        logger.error(f'Error loading model: {str(e)}')
        return

    # Initialize camera with multiple attempts
    logger.info('Initializing camera...')
    cap = None
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        logger.error(f"Failed to open camera {camera_index}")
        return
    
    # Test if we can actually read from the camera
    ret, frame = cap.read()
    logger.info(f"Camera read: ret={ret}, frame is None: {frame is None}")
    if not ret or frame is None:
        logger.error(f"Camera {camera_index} opened but failed to read frame")
        cap.release()
        return
    
    logger.info(f"Successfully opened camera {camera_index}")
    
    # Set camera properties
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, INPUT_SIZE)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, INPUT_SIZE)
    cap.set(cv2.CAP_PROP_FPS, TARGET_FPS)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    
    # Get actual camera properties
    actual_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    actual_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    actual_fps = cap.get(cv2.CAP_PROP_FPS)
    logger.info(f"Camera properties - Width: {actual_width}, Height: {actual_height}, FPS: {actual_fps}")

    window_name = 'Object Detection'
    cv2.namedWindow(window_name, cv2.WINDOW_AUTOSIZE)

    # Initialize variables
    start_time = time.time()
    frame_count = 0
    detection_count = 0
    detected_objects = set()
    last_frame_time = start_time
    frame_buffer = None
    quick_detection_mode = True
    tracker = ObjectTracker()  # Initialize the tracker

    logger.info('Starting main loop...')
    try:
        while True:
            current_time = time.time()
            elapsed_time = current_time - start_time

            if elapsed_time >= TIMEOUT_SECONDS:
                logger.info('10 second timeout reached')
                break

            if quick_detection_mode:
                if elapsed_time >= QUICK_DETECTION_TIMEOUT:
                    logger.info('Quick detection timeout (3 seconds) - continuing normal scan')
                    quick_detection_mode = False

            if current_time - last_frame_time < FRAME_SKIP_THRESHOLD:
                continue

            ret, frame = cap.read()
            if not ret or frame is None:
                logger.error('Failed to capture frame')
                break
            frame_count += 1
            last_frame_time = current_time

            # Prepare input for the model
            if frame_buffer is None:
                frame_buffer = np.empty((INPUT_SIZE, INPUT_SIZE, 3), dtype=np.uint8)
            
            # Fast resize and color conversion
            cv2.resize(frame, (INPUT_SIZE, INPUT_SIZE), dst=frame_buffer, 
                      interpolation=cv2.INTER_NEAREST)
            cv2.cvtColor(frame_buffer, cv2.COLOR_BGR2RGB, dst=frame_buffer)
            
            # Convert to float32 and normalize to [0, 1]
            input_data = frame_buffer.astype(np.float32) / 255.0
            input_data = np.expand_dims(input_data, axis=0)

            # Run inference
            predictions = model.predict(input_data, verbose=0)
            
            # Process predictions
            class_id, confidence, box = process_output(predictions, frame)
            
            # Update tracker
            tracked_box = tracker.update(box, confidence, current_time)
            
            if class_id is not None or tracked_box is not None:
                detection_count += 1
                class_name = CLASSES[class_id] if class_id is not None else "Tracking..."
                
                # Draw detection box and label
                frame = draw_detection(frame, class_name, confidence, tracked_box)
                if class_id is not None:
                    detected_objects.add(class_name)
                    print(f"DETECTED: {class_name}")  # Use print instead of logger for direct output
                    logger.info(f"{class_name} : yes")

            cv2.imshow(window_name, frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                logger.info('User requested quit')
                break

    except Exception as e:
        logger.error(f'Error during execution: {str(e)}')
        import traceback
        logger.error(traceback.format_exc())
    finally:
        # Cleanup and summary
        logger.info('Cleaning up...')
        total_time = time.time() - start_time
        logger.info(f'Processed {frame_count} frames in {total_time:.1f} seconds')
        logger.info(f'Average FPS: {frame_count/total_time:.1f}')
        cap.release()
        cv2.destroyAllWindows()
        logger.info('\nObject Detection Summary:')
        logger.info(f'Total frames processed: {frame_count}')
        logger.info(f'Total detections: {detection_count}')
        logger.info('\nDetected objects:')
        for obj in detected_objects:
            print(f"DETECTED: {obj}")  # Use print instead of logger for direct output
            logger.info(f"{obj} : yes")

if __name__ == '__main__':
    main()
