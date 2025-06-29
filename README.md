# 🎙️ Emotion-Adaptive Voice Assistant

A real-time voice assistant that transcribes speech using Whisper, detects emotion via Groq's LLaMA 3, and responds with an adaptive message and dynamic UI.

## 🚀 Live Demo
👉 [Try it on Hugging Face Spaces](https://huggingface.co/spaces/nishiai/EmotiVoice)

## ✨ Features
- 🧠 Whisper for speech-to-text transcription
- 🎯 Prompt-engineered LLaMA 3 (via Groq) for emotion detection
- 🎨 Gradio UI adapts to emotion (color, emoji, tone)
- 🔊 Voice response via gTTS
- ☁️ Deployed on Hugging Face Spaces

## 🛠️ Tech Stack
- Python, Whisper
- Groq API (LLaMA 3)
- Gradio, gTTS
- Hugging Face Spaces

## 📦 Setup

```bash
pip install -r requirements.txt
python app.py
