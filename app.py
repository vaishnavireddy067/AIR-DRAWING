import os
import json
import base64
import time
import socket
import webbrowser
import threading
import urllib.parse
import urllib.request
from datetime import datetime
from flask import Flask, render_template, jsonify, send_file, request, send_from_directory

app = Flask(__name__)

# Base directory for saved files (Vercel uses /tmp for write operations)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

if os.environ.get('VERCEL') or os.environ.get('AWS_LAMBDA_FUNCTION_NAME') or not os.access(BASE_DIR, os.W_OK):
    SAVED_DIR = os.path.join("/tmp", "saved_drawings")
    META_FILE = os.path.join("/tmp", "drawings_meta.json")
    ANALYTICS_FILE = os.path.join("/tmp", "analytics.json")
else:
    SAVED_DIR = os.path.join(BASE_DIR, "saved_drawings")
    META_FILE = os.path.join(BASE_DIR, "drawings_meta.json")
    ANALYTICS_FILE = os.path.join(BASE_DIR, "analytics.json")

os.makedirs(SAVED_DIR, exist_ok=True)

# Helper functions for metadata
def load_meta():
    if os.path.exists(META_FILE):
        try:
            with open(META_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_meta(data):
    try:
        with open(META_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
    except Exception:
        pass

def load_analytics():
    if os.path.exists(ANALYTICS_FILE):
        try:
            with open(ANALYTICS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "total_strokes": 0,
        "total_drawings_saved": 0,
        "total_speech_segments": 0,
        "total_gestures_detected": 0,
        "total_ocr_runs": 0,
        "total_translations": 0,
        "speech_transcripts": []
    }

def save_analytics(data):
    try:
        with open(ANALYTICS_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
    except Exception:
        pass

def find_free_port():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 0))
    port = s.getsockname()[1]
    s.close()
    return port

# -------------------------------------------------------------
# Routes
# -------------------------------------------------------------
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/health')
def health():
    return jsonify({
        "status": "online",
        "app": "Multimodal AI Interaction System",
        "features": ["Air Drawing", "Speech-to-Text", "Auto-Shape Beautifier", "Voice AI Generator", "AI OCR", "TTS", "Translation"]
    })

# Serve saved drawings
@app.route('/saved_drawings/<path:filename>')
def get_saved_file(filename):
    return send_from_directory(SAVED_DIR, filename)

# API: Get all saved drawings
@app.route('/api/drawings', methods=['GET'])
def get_drawings():
    meta = load_meta()
    return jsonify(meta)

# API: Save a new drawing from canvas
@app.route('/api/save_drawing', methods=['POST'])
def save_drawing():
    try:
        data = request.get_json()
        image_b64 = data.get('image', '')
        caption = data.get('caption', '').strip()
        ocr_text = data.get('ocr_text', '').strip()
        color = data.get('color', '#00e676')

        if not image_b64:
            return jsonify({"error": "No image data provided"}), 400

        if 'base64,' in image_b64:
            image_b64 = image_b64.split('base64,')[1]

        image_bytes = base64.b64decode(image_b64)
        
        timestamp_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"drawing_{timestamp_id}.png"
        filepath = os.path.join(SAVED_DIR, filename)

        with open(filepath, 'wb') as f:
            f.write(image_bytes)

        drawing_item = {
            "id": timestamp_id,
            "filename": filename,
            "url": f"/saved_drawings/{filename}",
            "caption": caption or "No speech caption recorded",
            "ocr_text": ocr_text or "No OCR text extracted",
            "color": color,
            "created_at": datetime.now().strftime("%d %b %Y, %I:%M:%S %p"),
            "timestamp": time.time()
        }

        meta = load_meta()
        meta.insert(0, drawing_item)
        save_meta(meta)

        analytics = load_analytics()
        analytics["total_drawings_saved"] = len(meta)
        save_analytics(analytics)

        return jsonify({"success": True, "drawing": drawing_item})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# API: Delete saved drawing
@app.route('/api/drawing/<draw_id>', methods=['DELETE'])
def delete_drawing(draw_id):
    meta = load_meta()
    item_to_delete = None
    for item in meta:
        if item.get('id') == draw_id:
            item_to_delete = item
            break

    if item_to_delete:
        meta.remove(item_to_delete)
        save_meta(meta)
        filepath = os.path.join(SAVED_DIR, item_to_delete.get('filename', ''))
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
            except Exception:
                pass
        
        analytics = load_analytics()
        analytics["total_drawings_saved"] = len(meta)
        save_analytics(analytics)

        return jsonify({"success": True})
    return jsonify({"error": "Drawing not found"}), 404

# API: Translation Engine
@app.route('/api/translate', methods=['POST'])
def translate_text():
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        source_lang = data.get('source_lang', 'en')
        target_lang = data.get('target_lang', 'te')

        if not text:
            return jsonify({"translated_text": ""})

        encoded_query = urllib.parse.quote(text)
        url = f"https://api.mymemory.translated.net/get?q={encoded_query}&langpair={source_lang}|{target_lang}"
        
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        with urllib.request.urlopen(req, timeout=5) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            translated_text = res_data.get('responseData', {}).get('translatedText', text)

        analytics = load_analytics()
        analytics["total_translations"] = analytics.get("total_translations", 0) + 1
        save_analytics(analytics)

        return jsonify({
            "success": True,
            "original_text": text,
            "translated_text": translated_text,
            "source_lang": source_lang,
            "target_lang": target_lang
        })
    except Exception as e:
        return jsonify({"error": str(e), "translated_text": text}), 500

# API: Log Speech Transcript
@app.route('/api/log_speech', methods=['POST'])
def log_speech():
    try:
        data = request.get_json()
        transcript = data.get('transcript', '').strip()
        lang = data.get('lang', 'en-IN')
        if transcript:
            analytics = load_analytics()
            analytics["total_speech_segments"] += 1
            analytics["speech_transcripts"].insert(0, {
                "transcript": transcript,
                "lang": lang,
                "time": datetime.now().strftime("%I:%M:%S %p")
            })
            analytics["speech_transcripts"] = analytics["speech_transcripts"][:100]
            save_analytics(analytics)
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# API: Get Multimodal Analytics
@app.route('/api/analytics', methods=['GET'])
def get_analytics():
    analytics = load_analytics()
    meta = load_meta()
    analytics["total_drawings_saved"] = len(meta)
    return jsonify(analytics)

# API: Update action stats
@app.route('/api/update_stats', methods=['POST'])
def update_stats():
    try:
        data = request.get_json()
        strokes = data.get('strokes', 0)
        gestures = data.get('gestures', 0)
        ocr_runs = data.get('ocr_runs', 0)
        analytics = load_analytics()
        analytics["total_strokes"] += strokes
        analytics["total_gestures_detected"] += gestures
        analytics["total_ocr_runs"] = analytics.get("total_ocr_runs", 0) + ocr_runs
        save_analytics(analytics)
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = 5000
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('127.0.0.1', port))
        s.close()
    except Exception:
        port = find_free_port()

    print("==================================================")
    print("  Multimodal AI Interaction System (Vercel Ready)")
    print(f"  --> http://127.0.0.1:{port}")
    print("==================================================")
    
    app.run(host='0.0.0.0', port=port, debug=False)
