// Simple frontend to interact with Flask backend
const messagesDiv = document.getElementById('messages');
const textInput = document.getElementById('textInput');
const sendBtn = document.getElementById('sendBtn');
const micBtn = document.getElementById('micBtn');
const stopMicBtn = document.getElementById('stopMicBtn');
const ttsBtn = document.getElementById('ttsBtn');

let mediaRecorder = null;
let audioChunks = [];
let lastBotText = '';

function appendMessage(who, text) {
  const d = document.createElement('div');
  d.className = 'msg ' + (who === 'user' ? 'user' : 'bot');
  d.textContent = (who === 'user' ? 'User: ' : 'Bot: ') + text;
  messagesDiv.appendChild(d);
  messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

async function sendText(text) {
  appendMessage('user', text);
  const resp = await fetch('/api/message', {
    method: 'POST', headers: {'Content-Type':'application/json'},
    body: JSON.stringify({text})
  });
  const j = await resp.json();
  if (j.error) {
    appendMessage('bot', 'ERROR: ' + j.error);
    return;
  }
  if (j.open_url) {
    appendMessage('bot', j.text + ' (open: ' + j.open_url + ')');
    window.open(j.open_url, '_blank');
  } else {
    appendMessage('bot', j.text || '');
  }
  lastBotText = j.text || '';
}

sendBtn.onclick = () => {
  const t = textInput.value.trim();
  if (!t) return;
  textInput.value = '';
  sendText(t);
};

// Mic recording -> upload to /api/audio and get transcript
micBtn.onclick = async () => {
  if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
    alert('Browser does not support getUserMedia');
    return;
  }
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);
    audioChunks = [];
    mediaRecorder.ondataavailable = e => audioChunks.push(e.data);
    mediaRecorder.onstop = async () => {
      const blob = new Blob(audioChunks, { type: 'audio/webm' });
      const fd = new FormData();
      fd.append('audio', blob, 'rec.webm');
      appendMessage('user', '(voice input)');
      const r = await fetch('/api/audio', { method: 'POST', body: fd });
      const j = await r.json();
      if (j.error) {
        appendMessage('bot', 'ERROR: ' + j.error);
        return;
      }
      if (j.transcript) {
        appendMessage('user', j.transcript);
        sendText(j.transcript);
      }
    };
    mediaRecorder.start();
    micBtn.disabled = true; stopMicBtn.disabled = false;
  } catch (e) {
    alert('Microphone error: ' + e.message);
  }
};

stopMicBtn.onclick = () => {
  if (mediaRecorder && mediaRecorder.state !== 'inactive') {
    mediaRecorder.stop();
    mediaRecorder = null;
  }
  micBtn.disabled = false; stopMicBtn.disabled = true;
};

// Playback using server TTS (if available) or browser TTS
ttsBtn.onclick = async () => {
  if (!lastBotText) return alert('No bot response yet');
  const r = await fetch('/api/tts', { method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify({text: lastBotText}) });
  const j = await r.json();
  if (j.audio_base64) {
    const audio = new Audio('data:audio/mp3;base64,' + j.audio_base64);
    audio.play();
  } else if (j.error) {
    // Fallback to browser speechSynthesis
    const ut = new SpeechSynthesisUtterance(lastBotText);
    window.speechSynthesis.speak(ut);
  }
};

// Support pressing Enter
textInput.addEventListener('keydown', e => { if (e.key === 'Enter') sendBtn.click(); });
