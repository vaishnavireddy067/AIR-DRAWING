/**
 * Multimodal AI Interaction System (5-in-1 Suite)
 * 1. ✋ Hand Gesture Detection (Air Drawing & Selection)
 * 2. 🎙️ Real-time Speech-to-Text Streaming
 * 3. 📷 AI OCR (Handwriting & Canvas Text Extraction via Tesseract.js)
 * 4. 🔊 Text-to-Speech (Natural Voice Readout Engine)
 * 5. 🌐 Multi-Language Translation (Telugu, Hindi, Spanish, etc.)
 */

// DOM Elements
const videoElement = document.getElementById('webcamVideo');
const cameraCanvas = document.getElementById('cameraCanvas');
const drawingCanvas = document.getElementById('drawingCanvas');
const camCtx = cameraCanvas.getContext('2d');
const drawCtx = drawingCanvas.getContext('2d');

const modeText = document.getElementById('modeText');
const camStatus = document.getElementById('camStatus');
const captionText = document.getElementById('captionText');
const speechLang = document.getElementById('speechLang');
const micWave = document.getElementById('micWave');
const clearBtn = document.getElementById('clearBtn');
const saveBtn = document.getElementById('saveBtn');
const colorButtons = document.querySelectorAll('.color-btn');

const navTabs = document.querySelectorAll('.nav-tab');
const tabContents = document.querySelectorAll('.tab-content');
const galleryGrid = document.getElementById('galleryGrid');
const emptyGalleryState = document.getElementById('emptyGalleryState');
const galleryCountBadge = document.getElementById('galleryCountBadge');
const refreshGalleryBtn = document.getElementById('refreshGalleryBtn');
const toastNotification = document.getElementById('toastNotification');
const toastMessage = document.getElementById('toastMessage');

// OCR, TTS & Translation DOM Elements
const ocrQuickBtn = document.getElementById('ocrQuickBtn');
const canvasOcrBtn = document.getElementById('canvasOcrBtn');
const canvasSpeakBtn = document.getElementById('canvasSpeakBtn');
const runOcrMainBtn = document.getElementById('runOcrMainBtn');
const ocrExtractedText = document.getElementById('ocrExtractedText');
const speakOcrBtn = document.getElementById('speakOcrBtn');
const copyOcrBtn = document.getElementById('copyOcrBtn');
const ocrStatusChip = document.getElementById('ocrStatusChip');

const targetLangSelect = document.getElementById('targetLangSelect');
const translatedTextOutput = document.getElementById('translatedTextOutput');
const translateActionBtn = document.getElementById('translateActionBtn');
const speakTranslationBtn = document.getElementById('speakTranslationBtn');

// Analytics DOM Elements
const statStrokes = document.getElementById('statStrokes');
const statDrawings = document.getElementById('statDrawings');
const statSpeechCount = document.getElementById('statSpeechCount');
const statOcrRuns = document.getElementById('statOcrRuns');
const transcriptList = document.getElementById('transcriptList');

// Accessibility DOM Elements
const largeCaptionToggle = document.getElementById('largeCaptionToggle');
const highContrastToggle = document.getElementById('highContrastToggle');
const audioChimeToggle = document.getElementById('audioChimeToggle');

// Drawing & Tracking State
let currentColor = '#00e676';
let brushThickness = 6;
let eraserRadius = 35;
let prevPoint = null;
let currentMode = 'Standby';

let sessionStrokes = 0;
let sessionGestures = 0;
let sessionOcrRuns = 0;
let currentActiveCaption = '';
let lastExtractedOcr = '';

// Hand Skeleton Connections
const HAND_CONNECTIONS = [
    [0, 1], [1, 2], [2, 3], [3, 4],        // Thumb
    [0, 5], [5, 6], [6, 7], [7, 8],        // Index
    [5, 9], [9, 10], [10, 11], [11, 12],   // Middle
    [9, 13], [13, 14], [14, 15], [15, 16], // Ring
    [13, 17], [17, 18], [18, 19], [19, 20],// Pinky
    [0, 17]                                // Palm
];

const virtualButtons = [
    { name: 'Red', color: '#ff3366', x1: 0.05, y1: 0.03, x2: 0.25, y2: 0.14 },
    { name: 'Green', color: '#00e676', x1: 0.28, y1: 0.03, x2: 0.48, y2: 0.14 },
    { name: 'Blue', color: '#2979ff', x1: 0.51, y1: 0.03, x2: 0.71, y2: 0.14 },
    { name: 'Clear', color: '#f87171', x1: 0.74, y1: 0.03, x2: 0.95, y2: 0.14 }
];

function resizeCanvases() {
    const width = 640;
    const height = 480;
    cameraCanvas.width = width;
    cameraCanvas.height = height;
    drawingCanvas.width = width;
    drawingCanvas.height = height;

    drawCtx.fillStyle = '#ffffff';
    drawCtx.fillRect(0, 0, width, height);
}
resizeCanvases();

// -------------------------------------------------------------
// 1. Tab Navigation & Notifications
// -------------------------------------------------------------
navTabs.forEach(tab => {
    tab.addEventListener('click', () => {
        const targetTab = tab.getAttribute('data-tab');
        navTabs.forEach(t => t.classList.remove('active'));
        tabContents.forEach(c => c.classList.remove('active'));

        tab.classList.add('active');
        document.getElementById(targetTab).classList.add('active');

        if (targetTab === 'galleryTab') loadGallery();
        if (targetTab === 'analyticsTab') loadAnalytics();
    });
});

function playChime(freq = 440, type = 'sine') {
    if (!audioChimeToggle || !audioChimeToggle.checked) return;
    try {
        const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.type = type;
        osc.frequency.value = freq;
        gain.gain.setValueAtTime(0.1, audioCtx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.15);
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        osc.start();
        osc.stop(audioCtx.currentTime + 0.15);
    } catch (e) {}
}

function showToast(msg) {
    if (!toastNotification) return;
    toastMessage.textContent = msg;
    toastNotification.classList.add('show');
    setTimeout(() => {
        toastNotification.classList.remove('show');
    }, 3000);
}

// -------------------------------------------------------------
// 2. Color & Drawing Controls
// -------------------------------------------------------------
colorButtons.forEach(btn => {
    btn.addEventListener('click', () => {
        colorButtons.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        currentColor = btn.getAttribute('data-color');
        playChime(600);
    });
});

function setColor(hex) {
    currentColor = hex;
    colorButtons.forEach(btn => {
        if (btn.getAttribute('data-color') === hex) {
            btn.classList.add('active');
        } else {
            btn.classList.remove('active');
        }
    });
    playChime(600);
}

function clearCanvas() {
    drawCtx.fillStyle = '#ffffff';
    drawCtx.fillRect(0, 0, drawingCanvas.width, drawingCanvas.height);
    playChime(300, 'triangle');
    showToast('Canvas Cleared!');
}
clearBtn.addEventListener('click', clearCanvas);

// -------------------------------------------------------------
// 3. AI OCR Recognition (Tesseract.js)
// -------------------------------------------------------------
async function runOCR() {
    try {
        if (ocrStatusChip) {
            ocrStatusChip.innerHTML = '<i class="fa-solid fa-circle-notch fa-spin"></i> Processing OCR...';
            ocrStatusChip.style.color = '#eab308';
        }
        showToast('Running AI OCR on Canvas...');

        // Convert drawing canvas to image
        const imgData = drawingCanvas.toDataURL('image/png');

        if (typeof Tesseract !== 'undefined') {
            const worker = await Tesseract.createWorker('eng');
            const ret = await worker.recognize(imgData);
            const text = ret.data.text.trim();
            await worker.terminate();

            lastExtractedOcr = text || 'No clear text detected';
            if (ocrExtractedText) ocrExtractedText.value = lastExtractedOcr;

            if (ocrStatusChip) {
                ocrStatusChip.innerHTML = '<i class="fa-solid fa-check"></i> OCR Success';
                ocrStatusChip.style.color = '#34d399';
            }

            sessionOcrRuns++;
            playChime(750);
            showToast(`OCR Detected: "${lastExtractedOcr.slice(0, 25)}..."`);

            // Auto-translate if text found
            if (text) {
                translateText(text);
            }
        } else {
            showToast('OCR engine loading, please try again.');
        }
    } catch (err) {
        console.error('OCR Error:', err);
        if (ocrStatusChip) {
            ocrStatusChip.innerHTML = '<i class="fa-solid fa-triangle-exclamation"></i> OCR Error';
            ocrStatusChip.style.color = '#f87171';
        }
        showToast('OCR failed to parse text');
    }
}

if (ocrQuickBtn) ocrQuickBtn.addEventListener('click', runOCR);
if (canvasOcrBtn) canvasOcrBtn.addEventListener('click', runOCR);
if (runOcrMainBtn) runOcrMainBtn.addEventListener('click', runOCR);

// -------------------------------------------------------------
// 4. Text-to-Speech (TTS Voice Readout Engine)
// -------------------------------------------------------------
function speakText(text, lang = 'en-US') {
    if (!text || !text.trim()) {
        showToast('No text available to read aloud');
        return;
    }

    if ('speechSynthesis' in window) {
        window.speechSynthesis.cancel(); // Stop ongoing speech

        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = lang;
        utterance.rate = 0.95;
        utterance.pitch = 1.0;

        // Pick matching natural voice if available
        const voices = window.speechSynthesis.getVoices();
        const matchedVoice = voices.find(v => v.lang.startsWith(lang.slice(0, 2)));
        if (matchedVoice) utterance.voice = matchedVoice;

        utterance.onstart = () => {
            showToast(`🔊 Speaking: "${text.slice(0, 25)}..."`);
        };

        window.speechSynthesis.speak(utterance);
    } else {
        showToast('Speech Synthesis (TTS) not supported in this browser');
    }
}

if (speakOcrBtn) {
    speakOcrBtn.addEventListener('click', () => {
        const text = ocrExtractedText ? ocrExtractedText.value : lastExtractedOcr;
        speakText(text, 'en-US');
    });
}

if (canvasSpeakBtn) {
    canvasSpeakBtn.addEventListener('click', () => {
        const text = lastExtractedOcr || currentActiveCaption || 'Air Drawing Canvas';
        speakText(text, 'en-US');
    });
}

if (copyOcrBtn) {
    copyOcrBtn.addEventListener('click', () => {
        const text = ocrExtractedText ? ocrExtractedText.value : '';
        if (text) {
            navigator.clipboard.writeText(text);
            showToast('Text copied to clipboard!');
        }
    });
}

// -------------------------------------------------------------
// 5. Multi-Language Translation Engine
// -------------------------------------------------------------
async function translateText(sourceText) {
    const text = sourceText || (ocrExtractedText ? ocrExtractedText.value : '');
    const targetLang = targetLangSelect ? targetLangSelect.value : 'te';

    if (!text || !text.trim()) {
        showToast('Please extract or enter text to translate');
        return;
    }

    try {
        if (translatedTextOutput) translatedTextOutput.value = 'Translating...';

        const res = await fetch('/api/translate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: text, source_lang: 'en', target_lang: targetLang })
        });

        const data = await res.json();
        if (data.translated_text && translatedTextOutput) {
            translatedTextOutput.value = data.translated_text;
            showToast('Translation completed!');
        }
    } catch (err) {
        console.error('Translation error:', err);
        if (translatedTextOutput) translatedTextOutput.value = 'Translation service unavailable';
    }
}

if (translateActionBtn) {
    translateActionBtn.addEventListener('click', () => translateText());
}

if (speakTranslationBtn) {
    speakTranslationBtn.addEventListener('click', () => {
        const text = translatedTextOutput ? translatedTextOutput.value : '';
        const targetLang = targetLangSelect ? targetLangSelect.value : 'te';
        const langMap = { 'te': 'te-IN', 'hi': 'hi-IN', 'es': 'es-ES', 'fr': 'fr-FR', 'de': 'de-DE', 'ja': 'ja-JP', 'en': 'en-US' };
        speakText(text, langMap[targetLang] || 'en-US');
    });
}

// -------------------------------------------------------------
// 6. Save Drawing & Gallery Dashboard
// -------------------------------------------------------------
async function saveDrawingToDashboard() {
    try {
        const imageB64 = drawingCanvas.toDataURL('image/png');
        const caption = currentActiveCaption || 'Multimodal Air Sketch';
        const ocr = lastExtractedOcr || 'Not run';

        const response = await fetch('/api/save_drawing', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                image: imageB64,
                caption: caption,
                ocr_text: ocr,
                color: currentColor
            })
        });

        const result = await response.json();
        if (result.success) {
            playChime(800);
            showToast('Drawing saved to Dashboard Gallery!');
            updateGalleryCount();
        } else {
            showToast('Failed to save drawing');
        }
    } catch (err) {
        console.error('Save error:', err);
        showToast('Error saving drawing');
    }
}
saveBtn.addEventListener('click', saveDrawingToDashboard);

window.addEventListener('keydown', (e) => {
    if (e.key === 's' || e.key === 'S') saveDrawingToDashboard();
    if (e.key === 'c' || e.key === 'C') clearCanvas();
    if (e.key === 'o' || e.key === 'O') runOCR();
});

async function loadGallery() {
    try {
        const response = await fetch('/api/drawings');
        const drawings = await response.json();

        galleryCountBadge.textContent = drawings.length;

        if (drawings.length === 0) {
            emptyGalleryState.style.display = 'block';
            galleryGrid.innerHTML = '';
            return;
        }

        emptyGalleryState.style.display = 'none';
        galleryGrid.innerHTML = drawings.map(item => `
            <div class="gallery-card">
                <img src="${item.url}" alt="Air Drawing" class="gallery-thumb" />
                <div class="gallery-info">
                    <div class="gallery-time">
                        <i class="fa-solid fa-clock"></i> ${item.created_at}
                    </div>
                    <div class="gallery-caption">
                        <i class="fa-solid fa-microphone"></i> <b>Speech:</b> "${item.caption}"
                    </div>
                    ${item.ocr_text && item.ocr_text !== 'No OCR text extracted' ? `
                    <div class="gallery-caption" style="border-left-color: #c084fc;">
                        <i class="fa-solid fa-font"></i> <b>OCR:</b> "${item.ocr_text}"
                    </div>` : ''}
                    <div class="gallery-actions">
                        <a href="${item.url}" download="${item.filename}" class="card-action-btn btn-download">
                            <i class="fa-solid fa-download"></i> Download
                        </a>
                        <button onclick="deleteDrawing('${item.id}')" class="card-action-btn btn-delete">
                            <i class="fa-solid fa-trash"></i> Delete
                        </button>
                    </div>
                </div>
            </div>
        `).join('');
    } catch (err) {
        console.error('Gallery load error:', err);
    }
}

async function updateGalleryCount() {
    try {
        const response = await fetch('/api/drawings');
        const drawings = await response.json();
        galleryCountBadge.textContent = drawings.length;
    } catch (e) {}
}
updateGalleryCount();

if (refreshGalleryBtn) refreshGalleryBtn.addEventListener('click', loadGallery);

window.deleteDrawing = async function(id) {
    if (!confirm('Are you sure you want to delete this drawing?')) return;
    try {
        const res = await fetch(`/api/drawing/${id}`, { method: 'DELETE' });
        const result = await res.json();
        if (result.success) {
            showToast('Drawing removed from dashboard');
            loadGallery();
        }
    } catch (e) {
        showToast('Error deleting drawing');
    }
};

// -------------------------------------------------------------
// 7. Analytics Sync
// -------------------------------------------------------------
async function loadAnalytics() {
    try {
        const response = await fetch('/api/analytics');
        const data = await response.json();

        statStrokes.textContent = data.total_strokes || 0;
        statDrawings.textContent = data.total_drawings_saved || 0;
        statSpeechCount.textContent = data.total_speech_segments || 0;
        statOcrRuns.textContent = (data.total_ocr_runs || 0) + (data.total_translations || 0);

        if (data.speech_transcripts && data.speech_transcripts.length > 0) {
            transcriptList.innerHTML = data.speech_transcripts.map(t => `
                <div class="transcript-item">
                    <span class="transcript-text"><i class="fa-solid fa-comment-dots" style="color:#38bdf8; margin-right:8px;"></i> "${t.transcript}"</span>
                    <div class="transcript-meta">
                        <span class="chip">${t.lang}</span>
                        <span>${t.time}</span>
                    </div>
                </div>
            `).join('');
        } else {
            transcriptList.innerHTML = '<p style="color:#64748b; padding:10px;">No speech transcripts logged yet.</p>';
        }
    } catch (err) {
        console.error('Analytics load error:', err);
    }
}

setInterval(() => {
    if (sessionStrokes > 0 || sessionGestures > 0 || sessionOcrRuns > 0) {
        fetch('/api/update_stats', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ strokes: sessionStrokes, gestures: sessionGestures, ocr_runs: sessionOcrRuns })
        }).catch(() => {});
        sessionStrokes = 0;
        sessionGestures = 0;
        sessionOcrRuns = 0;
    }
}, 5000);

// -------------------------------------------------------------
// 8. Gesture Detection Helper
// -------------------------------------------------------------
function analyzeHand(landmarks) {
    const indexUp = landmarks[8].y < landmarks[6].y;
    const middleUp = landmarks[12].y < landmarks[10].y;
    const ringUp = landmarks[16].y < landmarks[14].y;
    const pinkyUp = landmarks[20].y < landmarks[18].y;

    const isFist = (landmarks[8].y > landmarks[6].y &&
                    landmarks[12].y > landmarks[10].y &&
                    landmarks[16].y > landmarks[14].y &&
                    landmarks[20].y > landmarks[18].y);

    return { indexUp, middleUp, ringUp, pinkyUp, isFist };
}

// -------------------------------------------------------------
// 9. MediaPipe Hands Setup
// -------------------------------------------------------------
const hands = new Hands({
    locateFile: (file) => `https://cdn.jsdelivr.net/npm/@mediapipe/hands/${file}`
});

hands.setOptions({
    maxNumHands: 1,
    modelComplexity: 1,
    minDetectionConfidence: 0.65,
    minTrackingConfidence: 0.65
});

hands.onResults(onResults);

function drawLandmarksOnCamera(landmarks, w, h) {
    camCtx.strokeStyle = 'rgba(99, 102, 241, 0.8)';
    camCtx.lineWidth = 3;
    for (const [p1, p2] of HAND_CONNECTIONS) {
        const x1 = (1 - landmarks[p1].x) * w;
        const y1 = landmarks[p1].y * h;
        const x2 = (1 - landmarks[p2].x) * w;
        const y2 = landmarks[p2].y * h;

        camCtx.beginPath();
        camCtx.moveTo(x1, y1);
        camCtx.lineTo(x2, y2);
        camCtx.stroke();
    }

    for (const lm of landmarks) {
        const cx = (1 - lm.x) * w;
        const cy = lm.y * h;
        camCtx.fillStyle = '#00e676';
        camCtx.beginPath();
        camCtx.arc(cx, cy, 4, 0, 2 * Math.PI);
        camCtx.fill();
    }
}

function drawVirtualButtonsOnCamera(w, h) {
    for (const btn of virtualButtons) {
        const bx1 = btn.x1 * w;
        const by1 = btn.y1 * h;
        const bw = (btn.x2 - btn.x1) * w;
        const bh = (btn.y2 - btn.y1) * h;

        camCtx.fillStyle = btn.color === currentColor ? btn.color : 'rgba(30, 41, 59, 0.75)';
        camCtx.strokeStyle = btn.color;
        camCtx.lineWidth = 2;
        camCtx.beginPath();
        camCtx.roundRect(bx1, by1, bw, bh, 8);
        camCtx.fill();
        camCtx.stroke();

        camCtx.fillStyle = '#ffffff';
        camCtx.font = 'bold 14px Outfit, sans-serif';
        camCtx.textAlign = 'center';
        camCtx.textBaseline = 'middle';
        camCtx.fillText(btn.name, bx1 + bw / 2, by1 + bh / 2);
    }
}

function onResults(results) {
    const w = cameraCanvas.width;
    const h = cameraCanvas.height;

    camCtx.save();
    camCtx.clearRect(0, 0, w, h);
    camCtx.translate(w, 0);
    camCtx.scale(-1, 1);
    camCtx.drawImage(results.image, 0, 0, w, h);
    camCtx.restore();

    drawVirtualButtonsOnCamera(w, h);

    if (results.multiHandLandmarks && results.multiHandLandmarks.length > 0) {
        const landmarks = results.multiHandLandmarks[0];
        drawLandmarksOnCamera(landmarks, w, h);

        const gesture = analyzeHand(landmarks);
        sessionGestures++;

        const indexXNorm = 1 - landmarks[8].x;
        const indexYNorm = landmarks[8].y;
        const xTip = indexXNorm * w;
        const yTip = indexYNorm * h;

        // Case 1: Fist Gesture -> Eraser
        if (gesture.isFist) {
            currentMode = 'Eraser Mode (Fist)';
            prevPoint = null;

            camCtx.strokeStyle = '#ef4444';
            camCtx.lineWidth = 3;
            camCtx.beginPath();
            camCtx.arc(xTip, yTip, eraserRadius, 0, 2 * Math.PI);
            camCtx.stroke();

            drawCtx.fillStyle = '#ffffff';
            drawCtx.beginPath();
            drawCtx.arc(xTip, yTip, eraserRadius, 0, 2 * Math.PI);
            drawCtx.fill();
        }
        // Case 2: Two Fingers Up -> Selection / Hover
        else if (gesture.indexUp && gesture.middleUp) {
            currentMode = 'Selection Mode (Hover)';
            prevPoint = null;

            camCtx.fillStyle = currentColor;
            camCtx.strokeStyle = '#ffffff';
            camCtx.lineWidth = 3;
            camCtx.beginPath();
            camCtx.arc(xTip, yTip, 10, 0, 2 * Math.PI);
            camCtx.fill();
            camCtx.stroke();

            for (const btn of virtualButtons) {
                if (indexXNorm >= btn.x1 && indexXNorm <= btn.x2 &&
                    indexYNorm >= btn.y1 && indexYNorm <= btn.y2) {
                    if (btn.name === 'Clear') {
                        clearCanvas();
                    } else {
                        setColor(btn.color);
                    }
                }
            }
        }
        // Case 3: Only Index Finger Up -> Drawing / Writing
        else if (gesture.indexUp && !gesture.middleUp && !gesture.ringUp && !gesture.pinkyUp) {
            currentMode = 'Drawing / Writing Mode';
            sessionStrokes++;

            camCtx.fillStyle = currentColor;
            camCtx.beginPath();
            camCtx.arc(xTip, yTip, 8, 0, 2 * Math.PI);
            camCtx.fill();

            if (prevPoint) {
                drawCtx.strokeStyle = currentColor;
                drawCtx.lineWidth = brushThickness;
                drawCtx.lineCap = 'round';
                drawCtx.lineJoin = 'round';
                drawCtx.beginPath();
                drawCtx.moveTo(prevPoint.x, prevPoint.y);
                drawCtx.lineTo(xTip, yTip);
                drawCtx.stroke();
            }
            prevPoint = { x: xTip, y: yTip };
        } else {
            currentMode = 'Standby';
            prevPoint = null;
        }
    } else {
        currentMode = 'No Hand Detected';
        prevPoint = null;
    }

    modeText.textContent = currentMode;
}

// -------------------------------------------------------------
// 10. Start Webcam Loop
// -------------------------------------------------------------
const camera = new Camera(videoElement, {
    onFrame: async () => {
        await hands.send({ image: videoElement });
    },
    width: 640,
    height: 480
});

camera.start().then(() => {
    camStatus.innerHTML = '<span class="pulse-dot"></span> Camera Active';
    camStatus.className = 'chip live-chip';
}).catch(err => {
    console.error('Camera Error:', err);
    camStatus.innerHTML = '<i class="fa-solid fa-triangle-exclamation"></i> Cam Blocked';
    camStatus.className = 'chip';
});

// -------------------------------------------------------------
// 11. Ultra-Fast Web Speech Recognition
// -------------------------------------------------------------
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

if (SpeechRecognition) {
    let recognition = new SpeechRecognition();
    let isRecognizing = false;
    let selectedLang = speechLang ? speechLang.value : 'en-IN';

    function initRecognition() {
        recognition = new SpeechRecognition();
        recognition.continuous = true;
        recognition.interimResults = true;
        recognition.maxAlternatives = 1;
        recognition.lang = selectedLang;

        recognition.onstart = () => {
            isRecognizing = true;
            if (micWave) micWave.style.opacity = '1';
        };

        let lastFinalTranscript = '';

        recognition.onresult = (event) => {
            let interimTranscript = '';
            let currentFinal = '';

            for (let i = event.resultIndex; i < event.results.length; ++i) {
                const transcript = event.results[i][0].transcript;
                if (event.results[i].isFinal) {
                    currentFinal += transcript + ' ';
                } else {
                    interimTranscript += transcript;
                }
            }

            if (currentFinal) {
                const trimmedFinal = currentFinal.trim();
                lastFinalTranscript = (lastFinalTranscript + ' ' + trimmedFinal).slice(-150).trim();
                currentActiveCaption = trimmedFinal;

                fetch('/api/log_speech', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ transcript: trimmedFinal, lang: selectedLang })
                }).catch(() => {});
            }

            if (lastFinalTranscript || interimTranscript) {
                captionText.innerHTML = `
                    <span class="caption-final">${lastFinalTranscript ? '"' + lastFinalTranscript : ''}</span>
                    <span class="caption-interim">${interimTranscript ? (lastFinalTranscript ? ' ' : '"') + interimTranscript + '...' : (lastFinalTranscript ? '"' : '')}</span>
                `;
            }
        };

        recognition.onerror = (event) => {
            if (event.error !== 'no-speech') {
                console.warn('Speech notice:', event.error);
            }
        };

        recognition.onend = () => {
            isRecognizing = false;
            setTimeout(() => {
                if (!isRecognizing) {
                    try { recognition.start(); } catch (e) {}
                }
            }, 100);
        };

        try { recognition.start(); } catch (e) {}
    }

    initRecognition();

    if (speechLang) {
        speechLang.addEventListener('change', () => {
            selectedLang = speechLang.value;
            try { recognition.stop(); } catch (e) {}
            setTimeout(initRecognition, 200);
        });
    }
} else {
    captionText.innerHTML = '<span class="caption-interim">Web Speech API not supported. Please use Chrome or Edge.</span>';
}

// -------------------------------------------------------------
// 12. Accessibility Features Toggles
// -------------------------------------------------------------
if (largeCaptionToggle) {
    largeCaptionToggle.addEventListener('change', (e) => {
        if (e.target.checked) {
            captionText.classList.add('large-caption');
        } else {
            captionText.classList.remove('large-caption');
        }
    });
}

if (highContrastToggle) {
    highContrastToggle.addEventListener('change', (e) => {
        brushThickness = e.target.checked ? 12 : 6;
    });
}
