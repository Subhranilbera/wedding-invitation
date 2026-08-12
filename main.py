import os
import httpx
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import google.generativeai as genai

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-pro')
else:
    model = None

class ChatRequest(BaseModel):
    message: str

class RSVPRequest(BaseModel):
    name: str
    attending: bool

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

@app.post("/api/rsvp")
async def submit_rsvp(rsvp: RSVPRequest):
    status = "Joyfully Accepted 🥳" if rsvp.attending else "Regretfully Declined 😔"
    message = f"💌 *New Wedding RSVP!*\n\n*Guest:* {rsvp.name}\n*Status:* {status}"
    
    if TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}
        async with httpx.AsyncClient() as client:
            await client.post(url, json=payload)
            
    return {"status": "success", "message": "Thank you! Your RSVP has been received."}

@app.post("/api/chat")
async def ai_agent_chat(chat: ChatRequest):
    if not model:
        return {"reply": "I'm currently offline. Please reach out to us directly!"}

    # Giving the AI all the exact details from your physical card
    prompt = f"""
    You are an AI assistant for Subhranil and Paramita's wedding reception. 
    Facts:
    - Hosts: Subhranil (Son of Mr. Rabindranath Bera & Mrs. Pali Bera) & Paramita (Daughter of Mr. Swapan Garai & Mrs. Bandana Garai).
    - Date: Tuesday Evening, December 15, 2026.
    - Venue: Agamoni Community Hall, Parnashree, Kolkata-700060.
    - Contact: 8420546425 or 6290580265.
    
    Rule: Answer briefly, warmly, and elegantly. If asked something not in the facts, provide the contact numbers.
    Guest says: "{chat.message}"
    """
    try:
        response = model.generate_content(prompt)
        return {"reply": response.text}
    except:
        return {"reply": "I am having trouble connecting! Please contact 8420546425 for assistance."}