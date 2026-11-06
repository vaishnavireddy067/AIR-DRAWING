import cv2
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import sounddevice as sd
import speech_recognition as sr
from collections import deque
import threading
import queue
import time
import os

# -------------------------------------------------------------
# 1. Mediapipe Hand Landmarker Initialization
# -------------------------------------------------------------
MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hand_landmarker.task")

base_options = python.BaseOptions(model_asset_path=MODEL_PATH)
options = vision.HandLandmarkerOptions(
    base_options=base_options,
    num_hands=1,
    min_hand_detection_confidence=0.6,
    min_hand_presence_confidence=0.6,
    min_tracking_confidence=0.6
)
detector = vision.HandLandmarker.create_from_options(options)

# Hand skeleton connections for visualization
HAND_CONNECTIONS = [
    (0, 1), (1, 2), (2, 3), (3, 4),        # Thumb
    (0, 5), (5, 6), (6, 7), (7, 8),        # Index finger
    (5, 9), (9, 10), (10, 11), (11, 12),   # Middle finger
    (9, 13), (13, 14), (14, 15), (15, 16), # Ring finger
    (13, 17), (17, 18), (18, 19), (19, 20),# Pinky
    (0, 17)                                # Palm base
]

# -------------------------------------------------------------
# 2. Canvas & Drawing State Variables
# -------------------------------------------------------------
canvas = None
brush_thickness = 6
eraser_size = 35

# Available Colors (BGR format): Red, Green, Blue
colors = [
    (0, 0, 255),    # Red
    (0, 255, 0),    # Green
    (255, 0, 0)     # Blue
]
color_names = ["Red", "Green", "Blue"]
current_color = colors[1]  # Default Green

# Header UI Button rectangles [x1, y1, x2, y2]
btn_w, btn_h = 100, 50
btn_margin = 15
btn_y1 = 15
btn_y2 = btn_y1 + btn_h

button_boxes = [
    (btn_margin, btn_y1, btn_margin + btn_w, btn_y2),                             # Red
    (btn_margin * 2 + btn_w, btn_y1, btn_margin * 2 + btn_w * 2, btn_y2),        # Green
    (btn_margin * 3 + btn_w * 2, btn_y1, btn_margin * 3 + btn_w * 3, btn_y2),    # Blue
    (btn_margin * 4 + btn_w * 3, btn_y1, btn_margin * 4 + btn_w * 4, btn_y2)     # Clear / Erase All
]

# Track points for smooth line rendering
points = deque(maxlen=20)
prev_point = None

# -------------------------------------------------------------
# 3. Speech Recognition Background Thread (SoundDevice + SR)
# -------------------------------------------------------------
speech_queue = queue.Queue()
caption_text = "Say something to see live speech captions..."
caption_start_time = time.time()
caption_duration = 5.0  # Display captions for 5 seconds

def speech_worker():
    recognizer = sr.Recognizer()
    SAMPLE_RATE = 16000
    CHUNK_DURATION = 3.5  # seconds
    CHUNK_SIZE = int(SAMPLE_RATE * CHUNK_DURATION)

    while True:
        try:
            # Record audio chunk directly using sounddevice
            audio_np = sd.rec(CHUNK_SIZE, samplerate=SAMPLE_RATE, channels=1, dtype='int16')
            sd.wait()
            
            # Check sound energy to ignore complete silence
            energy = np.abs(audio_np).mean()
            if energy > 120:
                audio_bytes = audio_np.tobytes()
                audio_data = sr.AudioData(audio_bytes, SAMPLE_RATE, 2)
                try:
                    text = recognizer.recognize_google(audio_data)
                    if text and text.strip():
                        speech_queue.put(text.strip())
                except sr.UnknownValueError:
                    pass
                except sr.RequestError:
                    pass
            else:
                time.sleep(0.1)
        except Exception:
            time.sleep(0.5)

# Start background speech recognition
speech_thread = threading.Thread(target=speech_worker, daemon=True)
speech_thread.start()

# -------------------------------------------------------------
# 4. Gesture Detection Helper Functions
# -------------------------------------------------------------
def get_finger_states(landmarks):
    """
    Returns boolean states: (index_up, middle_up, ring_up, pinky_up, is_fist)
    """
    # Index finger
    index_up = landmarks[8].y < landmarks[6].y
    # Middle finger
    middle_up = landmarks[12].y < landmarks[10].y
    # Ring finger
    ring_up = landmarks[16].y < landmarks[14].y
    # Pinky finger
    pinky_up = landmarks[20].y < landmarks[18].y

    # Fist condition: all 4 fingers folded down
    is_fist = (landmarks[8].y > landmarks[6].y and
               landmarks[12].y > landmarks[10].y and
               landmarks[16].y > landmarks[14].y and
               landmarks[20].y > landmarks[18].y)

    return index_up, middle_up, ring_up, pinky_up, is_fist

def draw_custom_landmarks(frame, landmarks, w, h):
    """Draws skeleton and landmarks on the camera frame."""
    coords = []
    for lm in landmarks:
        cx, cy = int(lm.x * w), int(lm.y * h)
        coords.append((cx, cy))

    # Draw connection lines
    for p1, p2 in HAND_CONNECTIONS:
        cv2.line(frame, coords[p1], coords[p2], (245, 117, 66), 2)

    # Draw landmark joints
    for cx, cy in coords:
        cv2.circle(frame, (cx, cy), 4, (80, 227, 194), -1)

# -------------------------------------------------------------
# 5. UI Drawing Functions
# -------------------------------------------------------------
def draw_buttons(frame, active_color):
    """Renders top tool buttons (Red, Green, Blue, Clear)."""
    for i in range(3):
        x1, y1, x2, y2 = button_boxes[i]
        col = colors[i]
        # Highlight active color button with thicker border
        is_active = (col == active_color)
        cv2.rectangle(frame, (x1, y1), (x2, y2), col, -1)
        if is_active:
            cv2.rectangle(frame, (x1 - 3, y1 - 3), (x2 + 3, y2 + 3), (255, 255, 255), 3)
        else:
            cv2.rectangle(frame, (x1, y1), (x2, y2), (200, 200, 200), 2)
            
        cv2.putText(frame, color_names[i], (x1 + 18, y1 + 32),
                    cv2.FONT_HERSHEY_DUPLEX, 0.7, (255, 255, 255), 2)

    # Clear All Button
    cx1, cy1, cx2, cy2 = button_boxes[3]
    cv2.rectangle(frame, (cx1, cy1), (cx2, cy2), (50, 50, 50), -1)
    cv2.rectangle(frame, (cx1, cy1), (cx2, cy2), (200, 200, 200), 2)
    cv2.putText(frame, "CLEAR", (cx1 + 14, cy1 + 32),
                cv2.FONT_HERSHEY_DUPLEX, 0.65, (255, 255, 255), 2)

# -------------------------------------------------------------
# 6. Main Video Capture & Interaction Loop
# -------------------------------------------------------------
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

print("=" * 60)
print("  AI AIR DRAWING & LIVE SPEECH CAPTIONS")
print("=" * 60)
print("Controls:")
print("  - Index Finger Only : Draw on canvas")
print("  - Two Fingers (Index + Middle) : Select / Hover over top buttons")
print("  - Fist Gesture : Gesture Eraser")
print("  - 's' key : Save drawing to 'saved_drawing.png'")
print("  - 'c' key : Clear canvas")
print("  - 'q' key : Quit")
print("=" * 60)

cv2.namedWindow("AI Air Drawing & Speech Canvas", cv2.WINDOW_NORMAL)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Flip horizontally for natural mirror feel
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    # Initialize drawing canvas matching camera resolution
    if canvas is None:
        canvas = np.zeros((h, w, 3), dtype=np.uint8)

    # Convert BGR frame to RGB for MediaPipe Hand Landmarker
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
    detection_result = detector.detect(mp_image)

    # Mode indicator status string
    current_mode = "Standby"

    if detection_result.hand_landmarks:
        for hand_lms in detection_result.hand_landmarks:
            draw_custom_landmarks(frame, hand_lms, w, h)

            index_up, middle_up, ring_up, pinky_up, is_fist_state = get_finger_states(hand_lms)

            # Index fingertip position
            x_tip = int(hand_lms[8].x * w)
            y_tip = int(hand_lms[8].y * h)

            # Hand center position (Wrist / MCP average)
            x_wrist = int(hand_lms[0].x * w)
            y_wrist = int(hand_lms[0].y * h)

            # ---------------------------------------------
            # Case 1: Fist Gesture -> Erase local drawing
            # ---------------------------------------------
            if is_fist_state:
                current_mode = "Eraser Mode (Fist)"
                prev_point = None
                points.clear()
                # Erase on canvas
                cv2.circle(canvas, (x_tip, y_tip), eraser_size, (0, 0, 0), -1)
                # Visual eraser indicator circle on camera feed
                cv2.circle(frame, (x_tip, y_tip), eraser_size, (0, 0, 255), 2)

            # ---------------------------------------------
            # Case 2: Two Fingers UP -> Selection / Hover Mode
            # ---------------------------------------------
            elif index_up and middle_up:
                current_mode = "Selection Mode"
                prev_point = None
                points.clear()
                
                # Visual cursor indicator for selection
                cv2.circle(frame, (x_tip, y_tip), 12, (255, 255, 255), 2)
                cv2.circle(frame, (x_tip, y_tip), 6, current_color, -1)

                # Check if hover inside button area
                if y_tip < btn_y2 + 10:
                    for i in range(3):
                        x1, y1, x2, y2 = button_boxes[i]
                        if x1 <= x_tip <= x2 and y1 <= y_tip <= y2:
                            current_color = colors[i]
                    
                    # Check Clear Button
                    cx1, cy1, cx2, cy2 = button_boxes[3]
                    if cx1 <= x_tip <= cx2 and cy1 <= y_tip <= cy2:
                        canvas = np.zeros((h, w, 3), dtype=np.uint8)

            # ---------------------------------------------
            # Case 3: Only Index Finger UP -> Drawing Mode
            # ---------------------------------------------
            elif index_up and not middle_up and not ring_up and not pinky_up:
                current_mode = "Drawing Mode"
                cv2.circle(frame, (x_tip, y_tip), 8, current_color, -1)

                if prev_point is None:
                    prev_point = (x_tip, y_tip)

                # Draw smooth stroke connecting previous and current points
                cv2.line(canvas, prev_point, (x_tip, y_tip), current_color, brush_thickness)
                prev_point = (x_tip, y_tip)
            else:
                prev_point = None
    else:
        prev_point = None

    # Draw header buttons and active status on camera feed
    draw_buttons(frame, current_color)

    # Mode Badge on Camera Feed
    cv2.rectangle(frame, (15, h - 45), (260, h - 15), (0, 0, 0), -1)
    cv2.putText(frame, f"Mode: {current_mode}", (25, h - 25),
                cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 255), 2)

    # -------------------------------------------------------------
    # 7. Create White Virtual Drawing Canvas
    # -------------------------------------------------------------
    # Invert drawing for crisp display on pure white canvas
    white_canvas = np.full((h, w, 3), 255, dtype=np.uint8)
    
    # Extract drawing mask from canvas
    gray_canvas = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(gray_canvas, 10, 255, cv2.THRESH_BINARY)
    mask_inv = cv2.bitwise_not(mask)

    # Apply mask on white background
    white_bg = cv2.bitwise_and(white_canvas, white_canvas, mask=mask_inv)
    white_canvas_with_drawing = cv2.add(white_bg, canvas)

    # Add header title to virtual canvas screen
    cv2.rectangle(white_canvas_with_drawing, (0, 0), (w, 55), (240, 240, 240), -1)
    cv2.line(white_canvas_with_drawing, (0, 55), (w, 55), (210, 210, 210), 2)
    cv2.putText(white_canvas_with_drawing, "AI VIRTUAL CANVAS", (20, 36),
                cv2.FONT_HERSHEY_DUPLEX, 0.8, (50, 50, 50), 2)

    # Camera feed with subtle drawing overlay
    frame_with_drawing = cv2.addWeighted(frame, 0.8, canvas, 0.6, 0)

    # -------------------------------------------------------------
    # 8. Side-by-Side Dual Screen Display
    # -------------------------------------------------------------
    combined_view = np.hstack((frame_with_drawing, white_canvas_with_drawing))
    total_w = combined_view.shape[1]
    total_h = combined_view.shape[0]

    # -------------------------------------------------------------
    # 9. Real-Time Speech Captions Overlay
    # -------------------------------------------------------------
    if not speech_queue.empty():
        caption_text = speech_queue.get()
        caption_start_time = time.time()

    # Draw bottom caption banner across both screens
    banner_height = 55
    cv2.rectangle(combined_view, (0, total_h - banner_height), (total_w, total_h), (25, 25, 25), -1)
    cv2.line(combined_view, (0, total_h - banner_height), (total_w, total_h - banner_height), (0, 215, 255), 2)

    # Speech Icon / Indicator
    cv2.circle(combined_view, (35, total_h - 27), 10, (0, 255, 0), -1)
    cv2.putText(combined_view, "LIVE SPEECH:", (55, total_h - 20),
                cv2.FONT_HERSHEY_DUPLEX, 0.6, (0, 215, 255), 1)

    # Display dynamic caption text
    cv2.putText(combined_view, f'"{caption_text}"', (200, total_h - 20),
                cv2.FONT_HERSHEY_DUPLEX, 0.65, (255, 255, 255), 1)

    # Show Final Combined Air Drawing Window
    cv2.imshow("AI Air Drawing & Speech Canvas", combined_view)

    # -------------------------------------------------------------
    # 10. Keyboard Controls
    # -------------------------------------------------------------
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('s'):
        filename = "saved_drawing.png"
        cv2.imwrite(filename, white_canvas_with_drawing)
        print(f"[SUCCESS] Drawing saved successfully as '{filename}'!")
    elif key == ord('c'):
        canvas = np.zeros((h, w, 3), dtype=np.uint8)
        print("[INFO] Canvas cleared.")

cap.release()
cv2.destroyAllWindows()
