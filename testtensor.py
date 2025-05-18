import cv2
import time
import numpy as np
import logging
import tensorflow as tf
import os

# Set up logging with a custom format that removes the prefix
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s'  # Only show the message without prefix
)
logger = logging.getLogger(__name__)

# Constants
INPUT_SIZE = 224  # Reduced from 300 to 224 for better performance
CONFIDENCE_THRESHOLD = 0.1  # Lowered threshold to catch more detections
TIMEOUT_SECONDS = 10
TARGET_FPS = 30
FRAME_SKIP_THRESHOLD = 1.0 / TARGET_FPS  # Time threshold for frame skipping
REQUIRED_DETECTIONS = 3  # Number of unique objects needed for early termination
QUICK_DETECTION_TIMEOUT = 3  # Time limit for quick detection in seconds

# Model paths
SAVED_MODEL_PATH = "/Users/ichiroyamazaki/Documents/AIniform/ainiform-model-alpha-v1/converted_savedmodel/model.savedmodel"
KERAS_MODEL_PATH = "/Users/ichiroyamazaki/Documents/AIniform/ainiform-model-alpha-v1/converted_keras/keras_model.h5"
LABELS_PATH = "/Users/ichiroyamazaki/Documents/AIniform/ainiform-model-alpha-v1/converted_savedmodel/labels.txt"

# Custom class names
CLASSES = {
    0: 'pe-shirt',
    1: 'pe-pants',
    2: 'nstp-shirt',
    3: 'ict-gray-polo',
    4: 'ict-pants',
    5: 'house-hawks',
    6: 'house-cats',
    7: 'house-bulls',
    8: 'house-bears',
    9: 'house-wolves',
    10: 'ict-skirt',
    11: 'bstm-blazer',
    12: 'bstm-gray-skirt',
    13: 'bstm-gray-pants',
    14: 'bstm-yellow-necktie',
    15: 'bstm-pin',
    16: 'bstm-white-blouse',
    17: 'bstm-yellow-scarf',
    18: 'bstm-beret'
}

# Custom DepthwiseConv2D layer to handle the 'groups' parameter
class CustomDepthwiseConv2D(tf.keras.layers.DepthwiseConv2D):
    def __init__(self, *args, **kwargs):
        # Remove the 'groups' parameter if it exists
        kwargs.pop('groups', None)
        super().__init__(*args, **kwargs)

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

def process_output(detections):
    """Process output from Teachable Machine model"""
    # predictions is already a numpy array
    predictions = detections
    logger.info(f"Model output shape: {predictions.shape}")
    
    # Print all class probabilities
    logger.info("All class probabilities:")
    for i, prob in enumerate(predictions[0]):
        if i in CLASSES:
            logger.info(f"{CLASSES[i]}: {prob:.4f}")
    
    # Get the class with highest probability
    class_id = np.argmax(predictions[0])
    confidence = predictions[0][class_id]
    
    logger.info(f"Detected class ID: {class_id}")
    logger.info(f"Confidence: {confidence:.4f}")
    
    if confidence > CONFIDENCE_THRESHOLD and class_id in CLASSES:
        logger.info(f"Detected {CLASSES[class_id]} with confidence {confidence:.4f}")
        return class_id, confidence
    else:
        logger.info("No confident detection found")
        return None, 0.0

def main():
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
    
    # Try to use camera index 1 specifically
    camera_index = 1
    logger.info(f"Attempting to use camera {camera_index}...")
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
            logger.info(f"Camera read: ret={ret}, frame is None: {frame is None}")
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
            
            logger.info(f"Input data shape: {input_data.shape}")
            logger.info(f"Input data range: [{input_data.min()}, {input_data.max()}]")

            # Run inference
            predictions = model.predict(input_data, verbose=0)
            
            # Process predictions
            class_id, confidence = process_output(predictions)
            
            if class_id is not None:
                detection_count += 1
                class_name = CLASSES[class_id]
                
                # Draw text on frame
                label = f'{class_name}: {confidence:.2f}'
                cv2.putText(frame, label, (10, 30),
                          cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                detected_objects.add(class_name)

            logger.info("Displaying frame in window")
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
            logger.info(f'{obj} - yes')

if __name__ == '__main__':
    main()
