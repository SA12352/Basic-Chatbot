import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
import random
from gtts import gTTS
import speech_recognition as sr

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("API Key not found! Please add GEMINI_API_KEY to your .env file.")
    st.stop()

# Configure Gemini API
genai.configure(api_key=api_key)
model = genai.GenerativeModel("models/gemini-1.5-flash")

# Streamlit UI
st.set_page_config(page_title="My Chatbot")
st.title(" My Chatbot with Full Voice")
st.write("Type or Speak, I'll reply in text and voice. Use `/help` for commands.")

# Store chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Fun commands data
jokes = [
    "Why don't skeletons fight each other? They don't have the guts!",
    "I told my computer I needed a break, and it froze.",
    "Why was the math book sad? Because it had too many problems."
]
facts = [
    "Honey never spoils. Archaeologists have found 3000-year-old honey that's still edible!",
    "Bananas are berries, but strawberries are not.",
    "Sharks existed before trees."
]

# Function to capture voice input
def get_voice_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎙 Listening... Speak now!")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        st.success(f" You said: {text}")
        return text
    except sr.UnknownValueError:
        st.error("Sorry, I couldn't understand your voice.")
    except sr.RequestError:
        st.error("Speech recognition service is not available.")
    return None

# Display past messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Buttons for input type
col1, col2 = st.columns(2)
with col1:
    if st.button("🎤 Speak to Chatbot"):
        spoken_text = get_voice_input()
        if spoken_text:
            user_input = spoken_text
        else:
            user_input = None
    else:
        user_input = None

with col2:
    text_input = st.chat_input("Type your message here...")
    if text_input:
        user_input = text_input

# Handle user input
if user_input:
    # Special Commands
    if user_input.lower() == "/joke":
        bot_reply = random.choice(jokes)
    elif user_input.lower() == "/fact":
        bot_reply = random.choice(facts)
    elif user_input.lower() == "/help":
        bot_reply = "**Available Commands:**\n`/joke` - Random joke\n`/fact` - Random fact\n`/clear` - Clear chat"
    elif user_input.lower() == "/clear":
        st.session_state.messages = []
        st.experimental_rerun()
    else:
        st.chat_message("user").markdown(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})
        try:
            conversation_text = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])
            response = model.generate_content(conversation_text)
            bot_reply = response.text
        except Exception as e:
            bot_reply = f"Error: {e}"

    # Display bot reply
    with st.chat_message("assistant"):
        st.markdown(bot_reply)
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})

    # Voice Output
    try:
        tts = gTTS(bot_reply, lang='en')
        audio_path = "bot_reply.mp3"
        tts.save(audio_path)
        st.audio(audio_path, format="audio/mp3")
    except Exception as e:
        st.warning(f"Voice output failed: {e}")





