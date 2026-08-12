// --- Envelope Interaction ---
function openInvitation() {
    const envelope = document.getElementById('envelope-layer');
    const content = document.getElementById('invitation-layer');
    
    // Slide up and fade out the envelope
    envelope.style.transform = 'translateY(-100vh)';
    envelope.style.opacity = '0';
    
    // Fade in and slide up the content
    setTimeout(() => {
        envelope.style.display = 'none';
        content.style.opacity = '1';
        content.style.transform = 'translateY(0)';
    }, 1000);
}

// --- Countdown Logic ---
const targetDate = new Date("Dec 15, 2026 18:30:00").getTime();

setInterval(function() {
    const now = new Date().getTime();
    const distance = targetDate - now;

    document.getElementById("days").innerText = Math.floor(distance / (1000 * 60 * 60 * 24));
    document.getElementById("hours").innerText = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    document.getElementById("mins").innerText = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
    document.getElementById("secs").innerText = Math.floor((distance % (1000 * 60)) / 1000);
}, 1000);

// --- Backend Integrations ---
async function sendRSVP() {
    const name = document.getElementById('guestName').value;
    const attending = document.getElementById('isAttending').value === 'true';

    if (!name) {
        document.getElementById('rsvp-status').innerText = "Please enter your name.";
        return;
    }

    const response = await fetch('/api/rsvp', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, attending })
    });

    const result = await response.json();
    document.getElementById('rsvp-status').innerText = result.message;
}

async function askAI() {
    const message = document.getElementById('chatInput').value;
    const responseBox = document.getElementById('chat-response');
    
    if (!message) return;

    responseBox.innerText = "Thinking...";

    const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message })
    });

    const result = await response.json();
    responseBox.innerText = result.reply;
}