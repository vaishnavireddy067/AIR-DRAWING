# AI Air Drawing & Multimodal Interaction System 🎨🎙️🧠✨

[![GitHub Repository](https://img.shields.io/badge/GitHub-vaishnavireddy067%2FAIR--DRAWING-blue?logo=github)](https://github.com/vaishnavireddy067/AIR-DRAWING)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-Web%20Dashboard-000000?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-5C3EE8?logo=opencv&logoColor=white)](https://opencv.org/)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-Hand%20Tracking-00A98F?logo=google&logoColor=white)](https://developers.google.com/mediapipe)

An AI-powered **Multimodal Interaction System** that turns your webcam into an interactive touch-free virtual whiteboard. Draw in the air using hand gestures, switch colors, erase content, view drawings on a clean dual canvas, and experience real-time speech-to-text captions with an interactive dashboard gallery and analytics.

---

## 🌟 Key Features

### ✋ 1. Hand Gesture Detection (AI / Computer Vision)
- **Air Drawing**: Single index finger up (`☝️`) lets you draw freely in the air.
- **Button Selection**: Two fingers up (`✌️`) allows you to hover and select toolbar options without drawing unwanted lines.
- **Fist Eraser**: Closed fist (`✊`) activates a spatial circular eraser.
- **Dual Live Display**: Live camera feed with 21-point hand skeleton tracking on the left, pure virtual white canvas on the right.

### 🎙️ 2. Real-Time Speech-to-Text Captions
- **Zero-Latency Word-by-Word Streaming**: Spoken words are instantly converted into subtitles with glowing visual audio waveforms.
- **Multi-Language Support**:
  - 🇮🇳 **English (India)**
  - 🇺🇸 **English (US)**
  - 🗣️ **Telugu (తెలుగు)**
  - 🗣️ **Hindi (हिंदी)**

### 🖼️ 3. Saved Drawings Dashboard Gallery
- **One-Click Snapshots**: Press `s` or click **Save & Snapshot** to archive your drawing directly to the dashboard gallery.
- **Voice Caption Pairing**: Every saved drawing is automatically linked with the speech uttered during creation.
- **Artifact Management**: Preview, download high-res PNGs, or delete archived sketches.

### 📊 4. Multimodal Analytics & Interaction History
- Real-time KPI tracking for drawing strokes, gestures processed, and speech count.
- Searchable transcript timeline logging all spoken phrases with timestamps.

### ♿ 5. Accessibility Assistance
- **Large Visual Subtitles**: Hearing assistance mode for clear presentation feedback.
- **High-Contrast Canvas**: Enhanced stroke borders for visual support.
- **Audio Chimes**: Instant auditory feedback on tool switching and save actions.

---

## 🏗️ System Architecture

```
                  ┌──────────────────────────────────────────────────────────┐
                  │          MULTIMODAL AI INTERACTION SYSTEM                │
                  └─────────────────────────┬────────────────────────────────┘
                                            │
        ┌───────────────────┬───────────────┴───────────────┬───────────────────┐
        ▼                   ▼                               ▼                   ▼
 ✋ Hand Gesture       🎙️ Real-time Speech           🖼️ Saved Gallery      📊 Analytics & Logs
 - 1 Finger: Draw      - Word-by-Word Stream         - Canvas Snapshots    - Stroke Counters
 - 2 Fingers: Select   - Multilingual (EN/TE/HI)     - Voice Caption Link  - Speech History Log
 - Fist: Erase         - Glowing Equalizer           - PNG Download        - Accessibility Hub
```

---

## 📂 Project Structure

```
AIR-DRAWING/
│
├── app.py                     # Flask Web Application & REST APIs
├── main.py                    # Standalone Native Desktop OpenCV Application
├── hand_landmarker.task       # MediaPipe Hand Landmark AI Model
├── requirements.txt           # Project Dependencies
├── .gitignore                 # Git ignore configuration
├── README.md                  # Comprehensive Documentation
│
├── templates/
│   └── index.html             # Web Dashboard UI Template
│
├── static/
│   ├── css/
│   │   └── style.css          # Glassmorphism Modern Styling
│   └── js/
│       └── app.js             # Client-side Gesture Tracking & Speech Engine
│
└── saved_drawings/            # Storage Directory for Saved Canvas Artifacts
```

---

## ⚙️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/vaishnavireddy067/AIR-DRAWING.git
cd AIR-DRAWING
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Project

### Option A: Web Application Dashboard (Recommended)
```bash
python app.py
```
Open your browser at: **[http://127.0.0.1:5000](http://127.0.0.1:5000)** (or `http://localhost:5000`)

### Option B: Native Desktop OpenCV Window
```bash
python main.py
```

---

## 🎮 Hand Gestures & Controls

| Action | Gesture / Control | Description |
| :--- | :---: | :--- |
| **Draw** | ☝️ Single Index Finger Up | Smooth freehand drawing on canvas |
| **Select / Hover** | ✌️ Two Fingers (Index + Middle) | Select colors or clear button without drawing |
| **Erase** | ✊ Fist Gesture | Erases the area around your hand |
| **Red Brush** | Top Red Button | Switch to Red ink |
| **Green Brush** | Top Green Button | Switch to Green ink |
| **Blue Brush** | Top Blue Button | Switch to Blue ink |
| **Clear Canvas** | Top CLEAR Button / `c` Key | Clears entire canvas |
| **Save Drawing** | Top SAVE Button / `s` Key | Saves drawing & voice caption to Dashboard Gallery |
| **Quit (Desktop)** | `q` Key | Closes desktop OpenCV window |

---

## 💡 Technologies Used

- **Language**: Python 3.10+
- **Computer Vision**: OpenCV, Google MediaPipe
- **Voice & NLP**: Web Speech API, SpeechRecognition, SoundDevice
- **Web Framework**: Flask, REST API
- **Frontend**: HTML5 Canvas, CSS3 Glassmorphism, Vanilla JavaScript

---

## 👤 Author

- **GitHub**: [@vaishnavireddy067](https://github.com/vaishnavireddy067)
- **Repository**: [vaishnavireddy067/AIR-DRAWING](https://github.com/vaishnavireddy067/AIR-DRAWING)
