// Farmer AI - Modern JavaScript

let currentLanguage = 'en';
let abortController = null;
let sessionId = null; // Will be assigned server-side on first response

const translations = {
    en: {
        subtitle: 'Your smart farming companion - Ask about crops, weather, soil & more',
        welcome: '\uD83D\uDC4B Hello! I\'m your farming assistant. Ask me anything about crops, weather, soil health, pest control, irrigation, or farming tips!',
        placeholder: 'Type your question here...',
        sendBtn: 'Send'
    },
    mr: {
        subtitle: '\u0924\u0941\u092e\u091a\u093e \u0938\u094d\u092e\u093e\u0930\u094d\u091f \u0936\u0947\u0924\u0940 \u0938\u0939\u093e\u092f\u094d\u092f\u0915 - \u092a\u093f\u0915\u0947, \u0939\u0935\u093e\u092e\u093e\u0928, \u092e\u093e\u0924\u0940 \u0906\u0923\u093f \u0905\u0927\u093f\u0915 \u092c\u0926\u094d\u0926\u0932 \u0935\u093f\u091a\u093e\u0930\u093e',
        welcome: '\uD83D\uDC4B \u0928\u092e\u0938\u094d\u0915\u093e\u0930! \u092e\u0940 \u0924\u0941\u092e\u091a\u093e \u0936\u0947\u0924\u0940 \u0938\u0939\u093e\u092f\u094d\u092f\u0915 \u0906\u0939\u0947. \u092a\u093f\u0915\u0947, \u0939\u0935\u093e\u092e\u093e\u0928, \u092e\u093e\u0924\u0940 \u0906\u0930\u094b\u0917\u094d\u092f, \u0915\u093f\u0921\u0947 \u0928\u093f\u092f\u0902\u0924\u094d\u0930\u0923, \u0938\u093f\u0902\u091a\u0928 \u0915\u093f\u0902\u0935\u093e \u0936\u0947\u0924\u0940 \u091f\u093f\u092a\u094d\u0938 \u092c\u0926\u094d\u0926\u0932 \u092e\u0932\u093e \u0915\u093e\u0939\u0940\u0939\u0940 \u0935\u093f\u091a\u093e\u0930\u093e!',
        placeholder: '\u0924\u0941\u092e\u091a\u093e \u092a\u094d\u0930\u0936\u094d\u0928 \u092f\u0947\u0925\u0947 \u091f\u093e\u0907\u092a \u0915\u0930\u093e...',
        sendBtn: '\u092a\u093e\u0920\u0935\u093e'
    }
};

document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners();
    focusInput();
});

function setupEventListeners() {
    const input = document.getElementById('userInput');
    const sendBtn = document.querySelector('.send-btn');

    input.addEventListener('keypress', handleKeyPress);
    sendBtn.addEventListener('click', sendMessage);

    input.addEventListener('input', () => {
        input.style.height = 'auto';
        input.style.height = input.scrollHeight + 'px';
    });
}

function setLanguage(lang) {
    if (!translations[lang]) return; // Guard against unknown language codes
    currentLanguage = lang;

    document.getElementById('subtitle').textContent = translations[lang].subtitle;
    document.getElementById('userInput').placeholder = translations[lang].placeholder;
    document.getElementById('sendBtn').textContent = translations[lang].sendBtn;

    document.getElementById('btn-en').classList.toggle('active', lang === 'en');
    document.getElementById('btn-mr').classList.toggle('active', lang === 'mr');

    const container = document.getElementById('chatContainer');
    container.innerHTML = '';
    addMessage(translations[lang].welcome, false);

    focusInput();
}

function escapeHTML(text) {
    // Prevent XSS from AI responses or user input rendered via innerHTML
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function addMessage(text, isUser) {
    const chatContainer = document.getElementById('chatContainer');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user-message' : 'agent-message'}`;

    // Escape HTML first, then apply safe formatting
    const escaped = escapeHTML(text);
    const formattedText = escaped
        .replace(/\n/g, '<br>')
        .replace(/(\d+\.\s)/g, '<br>$1')
        .replace(/^<br>/, '');

    messageDiv.innerHTML = formattedText;
    chatContainer.appendChild(messageDiv);

    setTimeout(() => {
        chatContainer.scrollTo({ top: chatContainer.scrollHeight, behavior: 'smooth' });
    }, 100);
}

function showTyping(show) {
    const indicator = document.getElementById('typingIndicator');
    const stopBtn = document.getElementById('stopBtn');
    indicator.style.display = show ? 'flex' : 'none';
    stopBtn.style.display = show ? 'flex' : 'none';

    if (show) {
        const chatContainer = document.getElementById('chatContainer');
        chatContainer.scrollTo({ top: chatContainer.scrollHeight, behavior: 'smooth' });
    }
}

function stopGeneration() {
    if (abortController) {
        abortController.abort();
        abortController = null;
        showTyping(false);
        addMessage('Response stopped.', false);
    }
}

async function sendMessage() {
    const input = document.getElementById('userInput');
    const message = input.value.trim();

    if (!message) return;

    // Client-side length guard (mirrors server-side validation)
    if (message.length > 1000) {
        addMessage('Your message is too long. Please keep it under 1000 characters.', false);
        return;
    }

    addMessage(message, true);
    input.value = '';
    input.style.height = 'auto';

    showTyping(true);
    abortController = new AbortController();

    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                message: message,
                session_id: sessionId, // null on first request; server assigns one
                language: currentLanguage
            }),
            signal: abortController.signal
        });

        if (!response.ok) {
            const errData = await response.json().catch(() => ({}));
            throw new Error(errData.error || `Server error: ${response.status}`);
        }

        const data = await response.json();

        // Persist server-assigned session ID for subsequent requests
        if (data.session_id) {
            sessionId = data.session_id;
        }

        showTyping(false);
        addMessage(data.response, false);

    } catch (error) {
        showTyping(false);
        if (error.name === 'AbortError') return;
        addMessage('Sorry, I encountered an error. Please try again.', false);
        console.error('Chat error:', error);
    } finally {
        abortController = null;
    }

    focusInput();
}

function handleKeyPress(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
}

function focusInput() {
    if (window.innerWidth > 768) {
        document.getElementById('userInput').focus();
    }
}

if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/static/service-worker.js')
        .then(() => console.log('Service Worker registered'))
        .catch(err => console.error('Service Worker registration failed:', err));
}
