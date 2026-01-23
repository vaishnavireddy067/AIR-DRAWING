import cv2
import mediapipe as mp
import numpy as np
import speech_recognition as sr
from collections import deque
import threading
import queue
import time

# Initialize Mediapipe Hand detection
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Canvas and drawing variables
canvas = None
current_color = (0, 255, 0)  # Default green color
brush_thickness = 5
eraser_size = 30  # Increased eraser size (default 15)
# Colors and button locations
colors = [(0, 0, 255), (0, 255, 0), (255, 0, 0)]  # Red, Green, Blue
color_names = ["Red", "Green", "Blue"]
color_buttons = [(50, 50), (50, 150), (50, 250)]  # Button positions
erase_button = (50, 350)

# Function to draw buttons on the screen
def draw_buttons(frame):
    for i, color in enumerate(colors):
        # Draw color buttons
        cv2.rectangle(frame, (color_buttons[i][0], color_buttons[i][1]), 
                      (color_buttons[i][0] + 50, color_buttons[i][1] + 50), color, -1)
        # Simplified text rendering for buttons
        cv2.putText(frame, color_names[i], (color_buttons[i][0] + 5, color_buttons[i][1] + 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)  # Thicker, white text
    # Draw erase button
    cv2.rectangle(frame, (erase_button[0], erase_button[1]), 
                  (erase_button[0] + 50, erase_button[1] + 50), (0, 0, 0), -1)
    # Simplified text rendering for erase button
    cv2.putText(frame, "Erase", (erase_button[0] + 5, erase_button[1] + 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)  # Thicker, white text
# Initialize deque for smoothing
points = deque(maxlen=10)

# Mouse click state
drawing = False

def mouse_callback(event, x, y, flags, param):
    global drawing
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False

cv2.namedWindow("Air Drawing", cv2.WINDOW_NORMAL)
cv2.setMouseCallback("Air Drawing", mouse_callback)

# Initialize webcam and speech recognition
cap = cv2.VideoCapture(0)
recognizer = sr.Recognizer()
microphone = sr.Microphone()

# Queue for communication between threads
speech_queue = queue.Queue()

# Function to get real-time captions from speech (this will run in a separate thread)
def speech_recognition_thread():
    while True:
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
            audio = recognizer.listen(source)  # Listen for speech
            try:
                text = recognizer.recognize_google(audio)  # Convert speech to text
                speech_queue.put(text)  # Put the result in the queue
            except sr.UnknownValueError:
                speech_queue.put("")  # If no speech is detected
            except sr.RequestError:
                speech_queue.put("Error with the speech service")  # Handle API errors

# Start the speech recognition thread
speech_thread = threading.Thread(target=speech_recognition_thread, daemon=True)
speech_thread.start()

# Timer variables
caption_duration = 1.5  # Seconds to display each caption
caption_start_time = None
caption_text = ""
caption_display = False

# Function to detect fist gesture
def is_fist(hand_landmarks):
    # To detect a fist, check if the fingers are curled down and palm is closed.
    # Check thumb and other fingers' landmarks to determine if it's a fist.
    if hand_landmarks:
        # Thumb is curled if the tip is below the base
        thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
        thumb_ip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP]
        # Other fingers curled if tips are below the bases
        is_thumb_fist = thumb_tip.y > thumb_ip.y
        other_fingers_fist = True
        for i in range(1, 5):  # Checking the other four fingers
            finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark(i * 4 + 3)]
            finger_pip = hand_landmarks.landmark[mp_hands.HandLandmark(i * 4 + 2)]
            if finger_tip.y < finger_pip.y:
                other_fingers_fist = False
                break
        return is_thumb_fist and other_fingers_fist
    return False

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    h, w, c = frame.shape

    if canvas is None:
        canvas = np.zeros((h, w, 3), dtype=np.uint8)

    # Convert to RGB for Mediapipe
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    # Draw buttons on camera screen
    draw_buttons(frame)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Get index finger tip coordinates
            x_tip = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * w)
            y_tip = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * h)

            # Check button selection
            for i, button in enumerate(color_buttons):
                if button[0] < x_tip < button[0] + 50 and button[1] < y_tip < button[1] + 50:
                    current_color = colors[i]

            # Check erase button
            if erase_button[0] < x_tip < erase_button[0] + 50 and erase_button[1] < y_tip < erase_button[1] + 50:
                canvas = np.zeros((h, w, 3), dtype=np.uint8)

            # If fist gesture is detected, erase part of the drawing (increased eraser size)
            if is_fist(hand_landmarks):
                # Draw a small black circle around the eraser area
                cv2.circle(frame, (x_tip, y_tip), eraser_size, (0, 0, 0), 2)  # Circle around the eraser
                cv2.circle(canvas, (x_tip, y_tip), eraser_size, (0, 0, 0), -1)  # Erase part of the drawing

            # Add point to deque only if drawing is enabled (mouse held down)
            if drawing:
                points.append((x_tip, y_tip))
            else:
                points.append(None)

            # Draw lines using deque for smoother rendering
            if len(points) > 1:
                for i in range(1, len(points)):
                    if points[i - 1] is None or points[i] is None:
                        continue
                    cv2.line(canvas, points[i - 1], points[i], current_color, brush_thickness)

    # Create a white canvas to display the drawing
    white_canvas = np.ones_like(frame) * 255
    white_canvas = cv2.addWeighted(white_canvas, 0.5, canvas, 0.5, 0)

    # Overlay drawing on both camera screen and canvas screen
    frame_with_drawing = cv2.addWeighted(frame, 0.7, canvas, 0.3, 0)
    white_canvas_with_drawing = cv2.addWeighted(white_canvas, 0.7, canvas, 0.3, 0)

    # Combine both frames (camera feed and drawing canvas) side by side
    combined_frame = np.hstack((frame_with_drawing, white_canvas_with_drawing))

    # Resize the output screen to make it slightly smaller
    combined_frame_resized = cv2.resize(combined_frame, (int(w * 2.0), int(h * 0.9)))

    # Check the speech queue for new text
    if not speech_queue.empty():
        caption_text = speech_queue.get()
        caption_start_time = time.time()  # Start the timer
        caption_display = True

    # Display the caption with a black background
    if caption_display:
        elapsed_time = time.time() - caption_start_time
        if elapsed_time < caption_duration:
            # Draw a black rectangle for the caption background
            cv2.rectangle(combined_frame_resized, (0, combined_frame_resized.shape[0] - 50),
                          (combined_frame_resized.shape[1], combined_frame_resized.shape[0]),
                          (0, 0, 0), -1)  # Black background
            # Draw the caption text
            cv2.putText(combined_frame_resized, caption_text, 
                        (combined_frame_resized.shape[1] // 2 - len(caption_text) * 7, 
                         combined_frame_resized.shape[0] - 10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        else:
            caption_display = False  # Stop displaying caption after the duration
    # Display the combined screen with both camera and canvas
    cv2.imshow("Air Drawing", combined_frame_resized)
    # Save image when 's' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('s'):
        filename = 'saved_drawing.png'
        cv2.imwrite(filename, white_canvas_with_drawing)
        print(f"Drawing saved as {filename}")
    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()