# 🎨 Air Drawing with Real-Time Captions

An AI-powered **Virtual Canvas** that allows users to draw in the air using hand gestures while displaying **real-time speech-to-text captions**. This project combines **Computer Vision**, **Hand Gesture Recognition**, and **Speech Recognition** to create a touch-free interactive drawing experience.

---

## 📌 Features

- ✋ Air drawing using hand gestures
- 🎨 Multiple drawing colors (Red, Green, Blue)
- 🧽 Gesture-based eraser (Fist Gesture)
- 🗑️ Clear canvas option
- 📹 Live webcam feed with virtual canvas
- 🎙️ Real-time Speech-to-Text captions
- 💾 Save drawings as PNG images
- ⚡ Smooth drawing using point tracking (Deque)

---

## 🛠️ Technologies Used

- Python
- OpenCV
- MediaPipe
- NumPy
- SpeechRecognition
- Google Speech Recognition API
- Threading
- Queue

---

## 📂 Project Structure

```
Air-Drawing/
│
├── main.py
├── README.md
└── saved_drawing.png (Generated after saving)
```

---

## ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/yourusername/Air-Drawing.git
```

Move into the project folder

```bash
cd Air-Drawing
```

Install dependencies

```bash
pip install opencv-python mediapipe numpy SpeechRecognition PyAudio
```

> **Note:** If PyAudio installation fails:

Windows

```bash
pip install pipwin
pipwin install pyaudio
```

---

## ▶️ Run the Project

```bash
python main.py
```

---

## 🎮 Controls

| Action | Description |
|---------|-------------|
| Index Finger | Draw on canvas |
| Red Button | Select Red color |
| Green Button | Select Green color |
| Blue Button | Select Blue color |
| Erase Button | Clear entire canvas |
| Fist Gesture | Erase selected area |
| **S** | Save drawing |
| **Q** | Quit application |

---

## 🧠 How It Works

1. Webcam captures live video.
2. MediaPipe detects hand landmarks.
3. The index finger acts as the drawing pointer.
4. Color buttons change the brush color.
5. A fist gesture activates the eraser.
6. Speech Recognition runs in a separate thread.
7. Spoken words are converted into text and displayed as real-time captions.
8. Users can save their drawings using the **S** key.

---

## 📸 Output

The application displays:

- Live webcam feed
- Virtual drawing canvas
- Hand landmark detection
- Real-time speech captions
- Drawing tools and controls

---

## 🚀 Future Enhancements

- Brush size selection
- More gesture controls
- Undo/Redo functionality
- Shape drawing
- OCR integration
- Multi-language speech recognition
- Cloud storage for drawings

