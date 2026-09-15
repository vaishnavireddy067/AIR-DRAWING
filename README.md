# Multimodal AI Suite: Air Drawing, Speech, OCR, TTS & Translation 🎨🎙️📷🔊🌐

[![GitHub Repository](https://img.shields.io/badge/GitHub-vaishnavireddy067%2FAIR--DRAWING-blue?logo=github)](https://github.com/vaishnavireddy067/AIR-DRAWING)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-Web%20Dashboard-000000?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-5C3EE8?logo=opencv&logoColor=white)](https://opencv.org/)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-Hand%20Tracking-00A98F?logo=google&logoColor=white)](https://developers.google.com/mediapipe)
[![Tesseract OCR](https://img.shields.io/badge/Tesseract-AI%20OCR-orange)](https://github.com/naptha/tesseract.js)

A complete **5-in-1 Multimodal AI Interaction System** combining Computer Vision, Hand Gesture Tracking, Real-Time Speech Recognition, Optical Character Recognition (OCR), Text-to-Speech (TTS), Multi-Language Translation, and an interactive Dashboard Gallery.

---

## 🚀 Live Local Web Deployment Link

👉 **[http://127.0.0.1:5000](http://127.0.0.1:5000)** (or `http://localhost:5000`)

---

## 🌟 5 Core Multimodal AI Pillars

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                    MULTIMODAL AI INTERACTION SYSTEM                          │
└───────┬──────────────┬───────────────┬────────────────┬───────────────┬──────┘
        │              │               │                │               │
        ▼              ▼               ▼                ▼               ▼
 ✋ 1. Air Drawing 🎙️ 2. Speech-to-Text 📷 3. AI OCR  🔊 4. TTS Voice  🌐 5. Translation
 - 1 Finger Draw   - Instant Word Stream - Tesseract.js - Natural Speech - Telugu (తెలుగు)
 - 2 Finger Select - Multi-Language    - Canvas Read    - Read Aloud     - Hindi (हिंदी)
 - Fist Erase      - Dynamic Waveform  - Handwritings   - Multilingual   - Spanish, French...
```

### 1. ✋ Air Drawing (Gesture Control)
- **☝️ Single Index Finger Up**: Draw freehand lines, letters, or mathematical symbols on the canvas in the air.
- **✌️ Two Fingers Up (Index + Middle)**: Selection & hover mode over toolbar options.
- **✊ Fist Gesture**: Circular gesture-based eraser.
- **Dual Live Display**: Live camera feed with 21-point hand skeleton tracking on the left, pure virtual white canvas on the right.

### 2. 🎙️ Speech-to-Text (Real-Time Captions)
- **Zero-Latency Word-by-Word Streaming**: Spoken words are instantly converted into subtitles with glowing visual audio waveforms.
- **Multi-Language Support**: English (India), English (US), Telugu (తెలుగు), Hindi (हिंदी).

### 3. 📷 AI OCR (Handwriting & Text Extraction)
- **Tesseract.js Engine**: Instantly extracts handwritten characters and letters drawn on the canvas.
- **Shortcut**: Press **`O`** or click **OCR Read** to scan and copy text.

### 4. 🔊 Text-to-Speech (Natural Voice Readout Engine)
- **Natural Voice Synthesis**: Automatically reads aloud recognized handwritten text or speech transcripts in natural voice.
- **Multilingual TTS**: Pronounces translations in their native accent.

### 5. 🌐 Multi-Language Translation Engine
- **Instant Translation**: Translates recognized text or speech into:
  - 🗣️ **Telugu (తెలుగు)**
  - 🗣️ **Hindi (हिंदी)**
  - 🇪🇸 **Spanish (Español)**
  - 🇫🇷 **French (Français)**
  - 🇩🇪 **German (Deutsch)**
  - 🇯🇵 **Japanese (日本語)**

---

## 🖼️ Saved Gallery Dashboard & Analytics

- **One-Click Snapshots**: Press `s` or click **Save** to store drawings with attached speech captions & OCR transcripts.
- **Interactive Gallery Grid**: Preview, download PNGs, or delete archived sketches.
- **Interaction Analytics**: Real-time metrics for strokes, gestures, voice utterances, and OCR runs.
- **Accessibility Hub**: Large subtitles, high contrast mode, and audio confirmation chimes.

---

## 🎮 Hand Gestures & Controls

| Action | Control / Gesture | Description |
| :--- | :---: | :--- |
| **Draw / Write** | ☝️ Single Index Finger Up | Write letters or draw lines in the air |
| **Select / Hover** | ✌️ Two Fingers Up | Hover over top color & clear buttons |
| **Erase** | ✊ Fist Gesture | Erases the area around your hand |
| **AI OCR Read** | Top OCR Read Button / `o` Key | Extracts text written in the canvas |
| **Clear Canvas** | Top CLEAR Button / `c` Key | Clears entire canvas |
| **Save to Gallery** | Top SAVE Button / `s` Key | Saves snapshot with speech & OCR data |

---

## ⚙️ How to Run

```bash
# 1. Clone the repository
git clone https://github.com/vaishnavireddy067/AIR-DRAWING.git
cd AIR-DRAWING

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run Web App Server
python app.py
```
Open **[http://127.0.0.1:5000](http://127.0.0.1:5000)** in Google Chrome or Microsoft Edge.

---

## 👤 Author

- **GitHub**: [@vaishnavireddy067](https://github.com/vaishnavireddy067)
- **Repository**: [vaishnavireddy067/AIR-DRAWING](https://github.com/vaishnavireddy067/AIR-DRAWING)
