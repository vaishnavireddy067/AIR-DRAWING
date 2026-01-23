# Air Drawing (Virtual Canvas)

Air Drawing is an interactive computer vision project that allows users to draw on a digital canvas using hand gestures in the air. By leveraging **MediaPipe** for hand tracking and **OpenCV** for image processing, it transforms your webcam into a virtual whiteboard.

## 🚀 Features

- **Real-time Hand Tracking**: Accurate detection of hand landmarks using MediaPipe.
- **Gesture-Based Drawing**: Use your index finger to draw smooth lines in various colors.
- **Intelligent Eraser**: Switch to a fist gesture to erase specific parts of your drawing.
- **Dynamic UI**: On-screen buttons for color selection (Red, Green, Blue) and clearing the canvas.
- **Dual Display Mode**: See your drawing overlaid on the live camera feed and a clean white canvas simultaneously.
- **Speech-to-Text Integration**: Real-time captions displayed on-screen as you speak.
- **Save & Export**: Save your masterpiece as a PNG file with a single keypress.

## 🛠️ Tech Stack

- **Python**: Core programming language.
- **OpenCV**: For vision processing and UI rendering.
- **MediaPipe**: For robust hand gesture recognition.
- **SpeechRecognition**: For capturing and displaying real-time speech.
- **NumPy**: For canvas and matrix operations.

## 📋 Prerequisites

Before running the project, ensure you have Python installed and the following libraries:

```bash
pip install opencv-python mediapipe numpy SpeechRecognition PyAudio
```

*Note: `PyAudio` is required for the speech recognition feature. On Windows, you might need to install it via a wheel file if `pip install` fails.*

## 🎮 How to Use

1. **Run the Script**:
   ```bash
   python main.py
   ```
2. **Drawing**: 
   - Hold down the **Left Mouse Button** and move your **Index Finger** in front of the camera to draw.
   - Release the mouse button to stop drawing.
3. **Changing Colors**: 
   - Point your index finger at the **Red**, **Green**, or **Blue** buttons on the top left of the screen.
4. **Erasing**:
   - Make a **Fist** gesture and move it over the area you want to erase.
   - Point at the **Erase** button to clear the entire canvas.
5. **Saving**:
   - Press the **'s'** key to save your drawing as `saved_drawing.png`.
6. **Exiting**:
   - Press the **'q'** key to close the application.

## 🎙️ Speech Captions
The application listens to your microphone and displays what you say as captions at the bottom of the screen. This runs in a separate thread to ensure smooth performance.


