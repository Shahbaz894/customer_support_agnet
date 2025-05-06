# voice/voice_model.py

import os
import speech_recognition as sr
import google.generativeai as genai
from gtts import gTTS
from dotenv import load_dotenv
import playsound
from pydub import AudioSegment

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
os.environ['GOOGLE_API_KEY'] = GOOGLE_API_KEY

def speech_to_text(audio_file_path):
    r = sr.Recognizer()
    with sr.AudioFile(audio_file_path) as source:
        audio = r.record(source)  # Read the entire audio file
        try:
            text = r.recognize_google(audio, key=GOOGLE_API_KEY)
            print(f"Recognized: {text}")
            return text
        except sr.UnknownValueError:
            return "Sorry, I didn't understand that."
        except sr.RequestError as e:
            return "Could not request results from Google Speech Recognition service."

def get_response_from_gemini(user_text):
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(user_text)
    return response.text

def text_to_speech(text, filename="static/reply.mp3"):
    tts = gTTS(text=text, lang='en')
    tts.save(filename)
    playsound.playsound(filename)  # Optional: To immediately play the speech
    return filename  # Return the file path for response

