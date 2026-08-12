// --- Envelope & Butterfly Reveal ---
function openInvitation() {
    const envelope = document.getElementById('envelope-layer');
    const content = document.getElementById('invitation-layer');
    const butterflies = document.getElementById('butterfly-container');
    
    envelope.style.transform = 'translateY(-100vh)';
    envelope.style.opacity = '0';
    
    setTimeout(() => {
        envelope.style.display = 'none';
        content.style.opacity = '1';
        content.style.transform = 'translateY(0)';
        butterflies.style.opacity = '1'; // Release the butterflies!
    }, 1000);
}

// --- Interactive Butterflies ---
const bugs = document.querySelectorAll('.butterfly');
bugs.forEach(bug => {
    // Works for both mobile tapping and desktop clicking
    bug.addEventListener('touchstart', scatter);
    bug.addEventListener('click', scatter);
});

function scatter(e) {
    // Move to a random new location on the screen when touched
    const randomTop = Math.floor(Math.random() * 80) + 10;
    const randomLeft = Math.floor(Math.random() * 80) + 10;
    e.target.style.top = randomTop + '%';
    e.target.style.left = randomLeft + '%';
}

// --- Backend Integrations ---
async function sendRSVP() {
    const name = document.getElementById('guestName').value;
    const attending = document.getElementById('isAttending').value === 'true';

    if (!name) return;
    document.getElementById('rsvp-status').innerText = "Sending...";

    try {
        const response = await fetch('/api/rsvp', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, attending })
        });
        const result = await response.json();
        document.getElementById('rsvp-status').innerText = result.message;
    } catch (error) {
        document.getElementById('rsvp-status').innerText = "Network error. Please try again.";
    }
}

// Keep the askAI() function from previous code exactly as it was
