import uvicorn
from fastapi import FastAPI, Request, Form, UploadFile
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
import os
import tempfile

# Importing custom functions
from voice.voice_model import speech_to_text, get_response_from_gemini, text_to_speech
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from retriever.retrieval import Retriever
from utils.model_loader import ModelLoader
from prompt_library.prompt import PROMPT_TEMPLATES

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv()

retriever_obj = Retriever()
model_loader = ModelLoader()

def invoke_chain(query: str):
    retriever = retriever_obj.load_retriever()
    prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATES["product_bot"])
    llm = model_loader.load_llm()

    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    output = chain.invoke(query)
    return output

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """
    Render the chat interface.
    """
    return templates.TemplateResponse("chat.html", {"request": request})

@app.post("/get", response_class=HTMLResponse)
async def chat(msg: str = Form(...)):
    result = invoke_chain(msg)
    print(f"Response: {result}")
    return result

@app.post("/voice-to-response/")
async def voice_to_response(file: UploadFile):
    # Save uploaded file to a temporary location
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio_file:
        audio_path = temp_audio_file.name
        await file.seek(0)
        temp_audio_file.write(await file.read())

    # Step 1: Speech to Text
    user_text = speech_to_text(audio_path)
    print(f"Recognized: {user_text}")

    # Step 2: LangChain Response (invoke_chain instead of Gemini directly)
    bot_response = invoke_chain(user_text)

    # Step 3: Text to Speech
    reply_audio_path = text_to_speech(bot_response)

    # Step 4: Return mp3 file
    return FileResponse(reply_audio_path, media_type="audio/mpeg", filename="reply.mp3")
