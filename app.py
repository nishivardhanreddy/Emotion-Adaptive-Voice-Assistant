import gradio as gr
import whisper
from groq import Groq
from gtts import gTTS
import os
from dotenv import load_dotenv

load_dotenv()

# Load Whisper model
whisper_model = whisper.load_model("small")

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Emotion to color and emoji mapping
emotion_ui = {
    "happy": ("#FFF9C4", "😃"),
    "sad": ("#BBDEFB", "😔"),
    "angry": ("#FFCDD2", "😡"),
    "confused": ("#E1BEE7", "🤔"),
    "fearful": ("#D1C4E9", "😱"),
    "surprised": ("#C8E6C9", "😮"),
    "neutral": ("#F5F5F5", "😐"),
}


def get_emotion_from_text(text):
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {"role": "system", "content": "You are an emotion detection assistant. Respond with only one emotion like: happy, sad, angry, fearful, surprised, confused, or neutral."},
            {"role": "user", "content": text}
        ]
    )
    return response.choices[0].message.content.strip().lower()


def voice_assistant(audio):
    # Step 1: Transcribe
    result = whisper_model.transcribe(audio)
    transcription = result["text"]

    # Step 2: Detect emotion
    emotion = get_emotion_from_text(transcription)
    color, emoji = emotion_ui.get(emotion, ("#FFFFFF", "🤷"))

    # Step 3: Response based on emotion
    responses = {
        "angry": "I'm really sorry you're facing trouble. Let’s sort this out right away.",
        "happy": "I'm so glad to hear that! Let me know how I can help further.",
        "sad": "I’m here for you. Let’s see how I can assist.",
        "confused": "No worries, I’ll try to explain things more clearly.",
        "fearful": "It’s okay to be scared. I’m here to help.",
        "surprised": "Wow, that’s unexpected! Let’s explore more.",
        "neutral": "Got it! How can I assist you today?",
    }
    response = responses.get(emotion, "Got it! How can I assist you today?")

    # Step 4: Generate voice response
    tts = gTTS(text=response)
    tts_path = "response.mp3"
    tts.save(tts_path)

    # Return values
    return (
        transcription,
        f"{emoji} {emotion.capitalize()}",
        response,
        color,
        tts_path
    )


# Gradio Blocks with dynamic background
with gr.Blocks() as demo:
    gr.Markdown("## 🤖 Emotion-Adaptive Voice Assistant")
    audio_input = gr.Audio(type="filepath", label="🎤 Speak Now")
    with gr.Row():
        transcription_output = gr.Textbox(label="📝 Transcription")
        emotion_output = gr.Textbox(label="🧠 Emotion")
    response_output = gr.Textbox(label="💡 Assistant Reply")
    voice_output = gr.Audio(label="🎧 Assistant Voice", interactive=False)
    color_box = gr.HTML()

    def wrapped(audio):
        transcription, emotion, response, color, voice = voice_assistant(audio)
        box_style = f'<div style="background-color:{color}; padding:20px; border-radius:10px">Emotion color applied: {emotion}</div>'
        return transcription, emotion, response, voice, box_style

    audio_input.change(fn=wrapped, inputs=audio_input,
                       outputs=[transcription_output, emotion_output, response_output, voice_output, color_box])

if __name__ == "__main__":
    demo.launch()
