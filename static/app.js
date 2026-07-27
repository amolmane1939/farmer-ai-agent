// Farmer AI - Enhanced UI

let currentLanguage = 'en';
let abortController = null;
let sessionId = null;
let isAtBottom = true;

const translations = {
    en: {
        subtitle: 'Your smart farming companion - Ask about crops, weather, soil & more',
        welcome: '\uD83D\uDC4B Hello! I\'m your farming assistant. Ask me anything about crops, weather, soil health, pest control, irrigation, or farming tips!',
        placeholder: 'Type your question here...',
        emptyState: 'Ask me anything about your farm!',
        chips: [
            '\uD83C\uDF31 Best crops for monsoon',
            '\uD83D\uDC1B Pest control tips',
            '\uD83D\uDCA7 Irrigation advice',
            '\uD83C\uDF21\uFE0F Weather in Pune',
            '\uD83D\uDCB0 Crop prices today',
            '\uD83C\uDF31 Soil health tips'
        ]
    },
    mr: {
        subtitle: '\u0924\u0941\u092e\u091a\u093e \u0938\u094d\u092e\u093e\u0930\u094d\u091f \u0936\u0947\u0924\u0940 \u0938\u0939\u093e\u092f\u094d\u092f\u0915',
        welcome: '\uD83D\uDC4B \u0928\u092e\u0938\u094d\u0915\u093e\u0930! \u092e\u0940 \u0924\u0941\u092e\u091a\u093e \u0936\u0947\u0924\u0940 \u0938\u0939\u093e\u092f\u094d\u092f\u0915 \u0906\u0939\u0947. \u092a\u093f\u0915\u0947, \u0939\u0935\u093e\u092e\u093e\u0928, \u092e\u093e\u0924\u0940 \u0906\u0930\u094b\u0917\u094d\u092f \u092c\u0926\u094d\u0926\u0932 \u0935\u093f\u091a\u093e\u0930\u093e!',
        placeholder: '\u0924\u0941\u092e\u091a\u093e \u092a\u094d\u0930\u0936\u094d\u0928 \u092f\u0947\u0925\u0947 \u091f\u093e\u0907\u092a \u0915\u0930\u093e...',
        emptyState: '\u0924\u0941\u092e\u091a\u094d\u092f\u093e \u0936\u0947\u0924\u093e\u092c\u0926\u094d\u0926\u0932 \u0915\u093e\u0939\u0940\u0939\u0940 \u0935\u093f\u091a\u093e\u0930\u093e!',
        chips: [
            '\uD83C\uDF31 \u092a\u093E\u0935\u0938\u093E\u0933\u093E\u0924\u0940\u0932 \u092A\u093F\u0915\u0947',
            '\uD83D\uDC1B \u0915\u093F\u0921\u0947 \u0928\u093F\u092F\u0902\u0924\u094D\u0930\u0923',
            '\uD83D\uDCA7 \u0938\u093F\u0902\u091A\u0928 \u0938\u0932\u094D\u0932\u093E',
            '\uD83C\uDF21\uFE0F \u092A\u0941\u0923\u0947 \u0939\u0935\u093E\u092E\u093E\u0928',
            '\uD83D\uDCB0 \u0906\u091C\u091A\u0947 \u092D\u093E\u0935',
            '\uD83C\uDF31 \u092E\u093E\u0924\u0940 \u0906\u0930\u094B\u0917\u094D\u092F'
        ]
    }
};

// ─── Init ──────────────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners();
    focusInput();
    showEmptyState(true);
});

function setupEventListeners() {
    const input   = document.getElementById('userInput');
    const sendBtn = document.getElementById('sendBtn');
    const chat    = document.getElementById('chatContainer');

    input.addEventListener('keydown', handleKeyDown);
    input.addEventListener('input',   handleInputChange);
    sendBtn.addEventListener('click', sendMessage);

    // Track scroll position to show/hide scroll-to-bottom button
    chat.addEventListener('scroll', () => {
        const threshold = 100;
        isAtBottom = chat.scrollHeight - chat.scrollTop - chat.clientHeight < threshold;
        document.getElementById('scrollBtn').style.display = isAtBottom ? 'none' : 'block';
    });
}

// ─── Language ──────────────────────────────────────────────────────────────
function setLanguage(lang) {
    if (!translations[lang]) return;
    currentLanguage = lang;

    const t = translations[lang];
    document.getElementById('subtitle').textContent      = t.subtitle;
    document.getElementById('userInput').placeholder     = t.placeholder;
    document.getElementById('emptyStateText').textContent = t.emptyState;

    document.getElementById('btn-en').classList.toggle('active', lang === 'en');
    document.getElementById('btn-mr').classList.toggle('active', lang === 'mr');

    // Update chips
    const chips = document.querySelectorAll('.chip');
    chips.forEach((chip, i) => {
        if (t.chips[i]) chip.textContent = t.chips[i];
    });

    clearChat(true); // clear and show welcome in new language
    focusInput();
}

// ─── Empty state ───────────────────────────────────────────────────────────
function showEmptyState(show) {
    const el = document.getElementById('emptyState');
    if (el) el.style.display = show ? 'flex' : 'none';
}

// ─── Clear chat ────────────────────────────────────────────────────────────
function clearChat(silent) {
    const container = document.getElementById('chatContainer');
    // Remove all messages but keep the empty-state div
    Array.from(container.children).forEach(child => {
        if (child.id !== 'emptyState') container.removeChild(child);
    });
    showEmptyState(true);
    if (!silent) return; // just clear
    // Show welcome message in the current language
    addMessage(translations[currentLanguage].welcome, false);
}

// ─── Formatting ───────────────────────────────────────────────────────────
function escapeHTML(text) {
    const d = document.createElement('div');
    d.textContent = text;
    return d.innerHTML;
}

function formatMessage(text) {
    let html = escapeHTML(text);

    // Bold: **text**
    html = html.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
    // Italic: *text*
    html = html.replace(/\*(.+?)\*/g, '<em>$1</em>');
    // Numbered list: lines starting with "1. "
    html = html.replace(/(^|\n)(\d+\.\s)/g, '$1<br>$2');
    // Bullet list: lines starting with "- "
    html = html.replace(/(^|\n)-\s(.+)/g, '$1<br>\u2022 $2');
    // Plain newlines
    html = html.replace(/\n/g, '<br>');
    // Strip leading <br>
    html = html.replace(/^(<br>)+/, '');

    return html;
}

function getTime() {
    return new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

// ─── Add message ───────────────────────────────────────────────────────────
function addMessage(text, isUser) {
    showEmptyState(false);

    const container  = document.getElementById('chatContainer');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user-message' : 'agent-message'}`;

    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.innerHTML = formatMessage(text);
    messageDiv.appendChild(contentDiv);

    // Footer: timestamp + copy button (agent only)
    const footer = document.createElement('div');
    footer.className = 'message-footer';

    const timeSpan = document.createElement('span');
    timeSpan.className = 'message-time';
    timeSpan.textContent = getTime();
    footer.appendChild(timeSpan);

    if (!isUser) {
        const copyBtn = document.createElement('button');
        copyBtn.className = 'copy-btn';
        copyBtn.innerHTML = '\uD83D\uDCCB Copy';
        copyBtn.title = 'Copy to clipboard';
        copyBtn.addEventListener('click', () => copyText(text, copyBtn));
        footer.appendChild(copyBtn);
    }

    messageDiv.appendChild(footer);
    container.appendChild(messageDiv);

    if (isAtBottom) scrollToBottom();
}

// ─── Copy to clipboard ─────────────────────────────────────────────────────
function copyText(text, btn) {
    navigator.clipboard.writeText(text).then(() => {
        btn.innerHTML = '\u2705 Copied!';
        btn.classList.add('copied');
        setTimeout(() => {
            btn.innerHTML = '\uD83D\uDCCB Copy';
            btn.classList.remove('copied');
        }, 2000);
    }).catch(() => {
        // Fallback for older browsers
        const ta = document.createElement('textarea');
        ta.value = text;
        document.body.appendChild(ta);
        ta.select();
        document.execCommand('copy');
        document.body.removeChild(ta);
        btn.innerHTML = '\u2705 Copied!';
        setTimeout(() => { btn.innerHTML = '\uD83D\uDCCB Copy'; }, 2000);
    });
}

// ─── Typing indicator ──────────────────────────────────────────────────────
function showTyping(show) {
    let indicator = document.getElementById('typingIndicator');

    if (show) {
        if (!indicator) {
            indicator = document.createElement('div');
            indicator.id        = 'typingIndicator';
            indicator.className = 'typing-indicator';
            indicator.innerHTML = '<span></span><span></span><span></span>';
            document.getElementById('chatContainer').appendChild(indicator);
        }
        indicator.style.display = 'flex';
        scrollToBottom();
    } else {
        if (indicator) indicator.style.display = 'none';
    }

    const stopBtn = document.getElementById('stopBtn');
    if (stopBtn) stopBtn.style.display = show ? 'flex' : 'none';
}

// ─── Scroll ────────────────────────────────────────────────────────────────
function scrollToBottom() {
    const chat = document.getElementById('chatContainer');
    chat.scrollTo({ top: chat.scrollHeight, behavior: 'smooth' });
    document.getElementById('scrollBtn').style.display = 'none';
    isAtBottom = true;
}

// ─── Stop generation ───────────────────────────────────────────────────────
function stopGeneration() {
    if (abortController) {
        abortController.abort();
        abortController = null;
        showTyping(false);
        addMessage('Response stopped.', false);
    }
}

// ─── Input handling ────────────────────────────────────────────────────────
function handleInputChange() {
    const input   = document.getElementById('userInput');
    const counter = document.getElementById('charCounter');
    const len     = input.value.length;

    // Auto-grow textarea
    input.style.height = 'auto';
    input.style.height = Math.min(input.scrollHeight, 140) + 'px';

    // Character counter
    counter.textContent = `${len} / 1000`;
    counter.classList.remove('warn', 'limit');
    if (len >= 1000) counter.classList.add('limit');
    else if (len >= 800) counter.classList.add('warn');

    // Enable/disable send button
    document.getElementById('sendBtn').disabled = len === 0;
}

function handleKeyDown(event) {
    // Send on Enter (not Shift+Enter)
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
}

// ─── Suggestion chips ──────────────────────────────────────────────────────
function sendChip(btn) {
    const input = document.getElementById('userInput');
    input.value = btn.textContent.replace(/^[\uD800-\uDFFF\u2600-\u27BF\uFE0F\u20E3\uFE0F\s]+/u, '').trim();
    handleInputChange();
    sendMessage();
}

// ─── Send message ──────────────────────────────────────────────────────────
async function sendMessage() {
    const input   = document.getElementById('userInput');
    const message = input.value.trim();

    if (!message) return;

    if (message.length > 1000) {
        addMessage('Your message is too long. Please keep it under 1000 characters.', false);
        return;
    }

    addMessage(message, true);
    input.value = '';
    input.style.height = 'auto';
    handleInputChange();

    // Hide suggestions after first message
    document.getElementById('suggestions').style.display = 'none';

    showTyping(true);
    abortController = new AbortController();

    try {
        const response = await fetch('/chat', {
            method:  'POST',
            headers: { 'Content-Type': 'application/json' },
            body:    JSON.stringify({
                message,
                session_id: sessionId,
                language:   currentLanguage
            }),
            signal: abortController.signal
        });

        if (!response.ok) {
            const errData = await response.json().catch(() => ({}));
            throw new Error(errData.error || `Server error: ${response.status}`);
        }

        const data = await response.json();
        if (data.session_id) sessionId = data.session_id;

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

// ─── Focus ─────────────────────────────────────────────────────────────────
function focusInput() {
    if (window.innerWidth > 768) {
        document.getElementById('userInput').focus();
    }
}

// ─── Service Worker ────────────────────────────────────────────────────────
if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/static/service-worker.js')
        .then(() => console.log('Service Worker registered'))
        .catch(err => console.error('Service Worker registration failed:', err));
}
