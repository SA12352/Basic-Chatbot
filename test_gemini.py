import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load API key from .env file
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ API Key not found! Please add it to your .env file.")
    exit()

# Configure Gemini
genai.configure(api_key=api_key)

try:
    # Use updated model name
    model = genai.GenerativeModel("models/gemini-1.5-flash")
    prompt = "Hello Gemini! Can you say hi in one short sentence?"
    response = model.generate_content(prompt)
    print("✅ Gemini replied:", response.text)
except Exception as e:
    print("❌ Error:", e)

