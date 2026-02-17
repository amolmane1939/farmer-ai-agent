// Farmer AI - Modern JavaScript

const sessionId = 'session_' + Date.now();
let currentLanguage = 'en';

const translations = {
    en: {
        subtitle: 'Your smart farming companion - Ask about crops, weather, soil & more',
        welcome: '👋 Hello! I\'m your farming assistant. Ask me anything about crops, weather, soil health, pest control, irrigation, or farming tips!',
        placeholder: 'Type your question here...',
        sendBtn: 'Send'
    },
    mr: {
        subtitle: 'तुमचा स्मार्ट शेती सहाय्यक - पिके, हवामान, माती आणि अधिक बद्दल विचारा',
        welcome: '👋 नमस्कार! मी तुमचा शेती सहाय्यक आहे. पिके, हवामान, माती आरोग्य, किडे नियंत्रण, सिंचन किंवा शेती टिप्स बद्दल मला काहीही विचारा!',
        placeholder: 'तुमचा प्रश्न येथे टाइप करा...',
        sendBtn: 'पाठवा'
    }
};

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners();
    focusInput();
});

function setupEventListeners() {
    const input = document.getElementById('userInput');
    const sendBtn = document.querySelector('.send-btn');
    
    input.addEventListener('keypress', handleKeyPress);
    sendBtn.addEventListener('click', sendMessage);
    
    // Auto-resize textarea on mobile
    input.addEventListener('input', () => {
        input.style.height = 'auto';
        input.style.height = input.scrollHeight + 'px';
    });
}

function setLanguage(lang) {
    currentLanguage = lang;
    
    // Update UI
    document.getElementById('subtitle').textContent = translations[lang].subtitle;
    document.getElementById('userInput').placeholder = translations[lang].placeholder;
    document.getElementById('sendBtn').textContent = translations[lang].sendBtn;
    
    // Update buttons
    document.getElementById('btn-en').classList.toggle('active', lang === 'en');
    document.getElementById('btn-mr').classList.toggle('active', lang === 'mr');
    
    // Clear and show new welcome message
    const container = document.getElementById('chatContainer');
    container.innerHTML = '';
    addMessage(translations[lang].welcome, false);
    
    focusInput();
}

function addMessage(text, isUser) {
    const chatContainer = document.getElementById('chatContainer');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user-message' : 'agent-message'}`;
    messageDiv.textContent = text;
    chatContainer.appendChild(messageDiv);
    
    // Smooth scroll to bottom
    setTimeout(() => {
        chatContainer.scrollTo({
            top: chatContainer.scrollHeight,
            behavior: 'smooth'
        });
    }, 100);
}

function showTyping(show) {
    const indicator = document.getElementById('typingIndicator');
    indicator.style.display = show ? 'flex' : 'none';
    
    if (show) {
        const chatContainer = document.getElementById('chatContainer');
        chatContainer.scrollTo({
            top: chatContainer.scrollHeight,
            behavior: 'smooth'
        });
    }
}

async function sendMessage() {
    const input = document.getElementById('userInput');
    const message = input.value.trim();
    
    if (!message) return;
    
    // Add user message
    addMessage(message, true);
    input.value = '';
    input.style.height = 'auto';
    
    // Show typing indicator
    showTyping(true);
    
    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                message: message,
                session_id: sessionId,
                language: currentLanguage
            })
        });
        
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        
        const data = await response.json();
        showTyping(false);
        addMessage(data.response, false);
    } catch (error) {
        showTyping(false);
        addMessage('Sorry, I encountered an error. Please try again.', false);
        console.error('Error:', error);
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
    // Focus input on desktop, but not on mobile to avoid keyboard popup
    if (window.innerWidth > 768) {
        document.getElementById('userInput').focus();
    }
}

// Register Service Worker for PWA
if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/static/service-worker.js')
        .then(() => console.log('Service Worker registered'))
        .catch(err => console.log('Service Worker registration failed', err));
}
