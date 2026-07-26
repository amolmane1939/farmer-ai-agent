from flask import Flask, render_template, request, jsonify
import os
import uuid
import logging
from dotenv import load_dotenv
import requests
from openai import OpenAI
from db_manager import KnowledgeDB
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Rate limiting - 30 requests/minute per IP
# storage_uri='memory://' explicitly suppresses the default in-memory warning
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["30 per minute"],
    storage_uri="memory://"
)

def get_groq_client():
    """Lazy initialization of Groq client - re-reads key each time."""
    key = os.environ.get('GROQ_API_KEY')
    if not key:
        return None
    return OpenAI(api_key=key, base_url="https://api.groq.com/openai/v1")


class FarmerAgent:
    def __init__(self):
        try:
            self.knowledge_db = KnowledgeDB()
        except Exception as e:
            logger.error(f"Failed to initialize KnowledgeDB: {e}")
            self.knowledge_db = None
        self.chat_sessions = {}

    def get_weather(self, city):
        try:
            response = requests.get(
                f"https://wttr.in/{city}?format=j1",
                timeout=5
            )
            if response.status_code == 200:
                data = response.json()['current_condition'][0]
                return (
                    f"{data['weatherDesc'][0]['value']}, "
                    f"{data['temp_C']}\u00b0C, "
                    f"Humidity {data['humidity']}%, "
                    f"Wind {data['windspeedKmph']} km/h"
                )
        except Exception as e:
            logger.warning(f"Weather fetch failed for {city}: {e}")
        return None

    def get_response(self, user_message, session_id='default', language='en'):
        msg_lower = user_message.lower().strip()

        # Greetings - keyword-based (more flexible than exact match)
        greeting_words = ['hi', 'hello', 'hey', 'namaste']
        if any(msg_lower.startswith(w) for w in greeting_words):
            return "Namaste! I'm your farming assistant. Ask me about crops, soil, pests, water, or profit. How can I help you today?"

        # Search knowledge database
        db_context = ""
        if self.knowledge_db:
            try:
                results = self.knowledge_db.search(user_message, top_k=2)
                for result in results[:2]:
                    db_context += f"\n\n[Expert Knowledge: {result['answer']}]"
            except Exception as e:
                logger.warning(f"Knowledge DB search failed: {e}")

        # Weather check
        weather_info = ""
        weather_keywords = ['weather', 'temperature', 'rain', 'hava', 'mausam']
        cities = ['pune', 'mumbai', 'delhi', 'bangalore', 'hyderabad',
                  'chennai', 'nagpur', 'nashik']
        if any(w in msg_lower for w in weather_keywords):
            for city in cities:
                if city in msg_lower:
                    weather_data = self.get_weather(city)
                    if weather_data:
                        weather_info = f"\n\n[Current Weather in {city.title()}: {weather_data}]"
                    break

        client = get_groq_client()
        if not client:
            return "Service temporarily unavailable. Please try again."

        # Language instruction in system prompt - not in user message
        language_instruction = ""
        if language == 'mr':
            language_instruction = "\nIMPORTANT: Always respond in Marathi language."

        system_prompt = f"""You are an expert farming advisor helping Indian farmers.

CRITICAL INSTRUCTION:
If [Expert Knowledge] is provided below, YOU MUST USE ONLY THAT INFORMATION.
Do NOT add information from your general knowledge.
Present the expert knowledge in simple, conversational language.

RULES:
1. Use SIMPLE language farmers understand
2. Give PRACTICAL advice with real numbers
3. Mention Indian context (mandis, schemes, seasons)
4. For complex topics, use numbered steps
5. For simple questions, 2-3 sentences
6. Be encouraging and supportive

If [Current Weather] is provided, use that exact data.

Remember: Farmers need clear, actionable advice.{language_instruction}"""

        full_context = user_message + weather_info + db_context

        try:
            if session_id not in self.chat_sessions:
                self.chat_sessions[session_id] = []

            history = self.chat_sessions[session_id][-6:]

            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": system_prompt},
                    *history,
                    {"role": "user", "content": full_context}
                ],
                temperature=0.7,
                max_tokens=1000,
                timeout=30
            )

            answer = response.choices[0].message.content

            self.chat_sessions[session_id].append({"role": "user", "content": user_message})
            self.chat_sessions[session_id].append({"role": "assistant", "content": answer})

            return answer

        except Exception as e:
            logger.error(f"Groq API error for session {session_id}: {e}")
            return "Sorry, I'm having trouble right now. Please ask your question again."


agent = FarmerAgent()


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
@limiter.limit("30 per minute")
def chat():
    data = request.json or {}
    user_message = data.get('message', '').strip()
    language = data.get('language', 'en')

    # Input validation
    if not user_message:
        return jsonify({'error': 'Message cannot be empty'}), 400
    if len(user_message) > 1000:
        return jsonify({'error': 'Message too long. Please keep it under 1000 characters.'}), 400
    if language not in ('en', 'mr'):
        language = 'en'

    # Generate session ID server-side - never trust client-provided IDs
    session_id = data.get('session_id', '')
    if not session_id or not _is_valid_session_id(session_id):
        session_id = str(uuid.uuid4())

    response = agent.get_response(user_message, session_id, language)
    return jsonify({'response': response, 'session_id': session_id})


def _is_valid_session_id(sid):
    """Validate session ID is a proper UUID to prevent injection."""
    try:
        uuid.UUID(str(sid))
        return True
    except ValueError:
        return False


# PythonAnywhere uses WSGI - do NOT run app.run() in production
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
