import os
import smtplib
from email.mime.text import MIMEText
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import google.generativeai as genai

# ==========================================
# 1. App Configuration & Initialization
# ==========================================
app = FastAPI()

# Mount the static directory for CSS, JS, and Images
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up the HTML templates directory
templates = Jinja2Templates(directory="templates")

# ==========================================
# 2. AI Agent Configuration (Gemini)
# ==========================================
# Fetches your free API key from Render's Environment Variables
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    # Using the current standard free-tier model
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    print("WARNING: GEMINI_API_KEY not found in environment variables.")
    model = None

# ==========================================
# 3. Pydantic Models for API Requests
# ==========================================
class ChatRequest(BaseModel):
    message: str

class RSVPRequest(BaseModel):
    name: str
    attending: bool

# ==========================================
# 4. Helper Function: Send RSVP via Email
# ==========================================
def send_rsvp_email(guest_name: str, is_attending: bool):
    """
    Sends an automated email to you when a guest RSVPs.
    Requires EMAIL_ADDRESS and EMAIL_APP_PASSWORD in Render Environment Variables.
    """
    sender_email = os.environ.get("EMAIL_ADDRESS")
    # For Gmail, this must be an "App Password", not your normal login password.
    app_password = os.environ.get("EMAIL_APP_PASSWORD") 
    
    if not sender_email or not app_password:
        print("Email credentials not configured. Skipping email notification.")
        return

    status = "Joyfully Accepted" if is_attending else "Regretfully Declined"
    
    # Construct the email body
    msg = MIMEText(f"You have a new RSVP!\n\nGuest Name: {guest_name}\nStatus: {status}")
    msg['Subject'] = f"New RSVP: {guest_name} - {status}"
    msg['From'] = sender_email
    msg['To'] = sender_email # Sends the email to yourself
    
    try:
        # Connect to Gmail's secure SMTP server
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(sender_email, app_password)
        server.send_message(msg)
        server.quit()
        print(f"RSVP email sent for {guest_name}.")
    except Exception as e:
        print(f"Failed to send email: {e}")

# ==========================================
# 5. API Endpoints
# ==========================================

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Serves the main frontend HTML page."""
    # Updated syntax for newer versions of FastAPI
    return templates.TemplateResponse(
        request=request, 
        name="index.html"
    )

@app.post("/api/rsvp")
async def submit_rsvp(rsvp: RSVPRequest):
    """Handles guest RSVPs from the frontend."""
    # Send the email notification in the background
    send_rsvp_email(rsvp.name, rsvp.attending)
    
    return {"status": "success", "message": "Thank you! Your RSVP has been received."}

@app.post("/api/chat")
async def ai_agent_chat(chat: ChatRequest):
    """Handles the Virtual Assistant queries using Gemini."""
    if not model:
        return {"reply": "I'm sorry, the virtual assistant is offline right now. Please reach out to us directly!"}

    user_query = chat.message
    
    # The System Prompt: This gives the AI its identity, facts, and rules.
    prompt = f"""
    You are a polite, elegant, and brief AI virtual assistant for Subhranil and Paramita's wedding reception.
    
    Here are the event facts you must know:
    - Event: Reception
    - Hosts: Subhranil and Paramita
    - Date: December 15, 2026
    - Time: 6:30 PM
    - Venue: Agomoni Community Hall
    
    Rules:
    - Answer the guest's question briefly (1-2 sentences maximum).
    - Be warm and welcoming.
    - If a guest asks something outside of these facts (like menu, parking, or dress code), politely inform them that you are just a digital assistant and they should contact Subhranil or Paramita directly for those specific details.
    
    Guest asks: "{user_query}"
    """
    
    try:
        response = model.generate_content(prompt)
        ai_reply = response.text
    except Exception as e:
        print(f"Gemini API Error: {e}")
        ai_reply = "I am having a little trouble connecting to my brain right now! We are so excited to see you on December 15th."
        
    return {"reply": ai_reply}