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
    // Format the response nicely for your email
    const attending = document.getElementById('isAttending').value === 'true' ? 'Joyfully Accept' : 'Regretfully Decline';

    if (!name) {
        document.getElementById('rsvp-status').innerText = "Please enter your name.";
        return;
    }

    document.getElementById('rsvp-status').innerText = "Sending...";

    // PASTE YOUR FORMSPREE URL BELOW
    const formspreeURL = "https://formspree.io/f/YOUR_UNIQUE_ID_HERE"; 

    try {
        const response = await fetch(formspreeURL, {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ "Guest Name": name, "RSVP Status": attending })
        });

        if (response.ok) {
            document.getElementById('rsvp-status').innerText = "Thank you! Your RSVP has been received.";
        } else {
            document.getElementById('rsvp-status').innerText = "Oops! There was a problem submitting your RSVP.";
        }
    } catch (error) {
        document.getElementById('rsvp-status').innerText = "Network error. Please try again.";
    }
}
