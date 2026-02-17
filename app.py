from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
import requests
from openai import OpenAI
from db_manager import KnowledgeDB

load_dotenv()
app = Flask(__name__)

GROQ_KEY = os.environ.get('GROQ_API_KEY')
client = OpenAI(api_key=GROQ_KEY, base_url="https://api.groq.com/openai/v1") if GROQ_KEY else None

class FarmerAgent:
    def __init__(self):
        try:
            self.knowledge_db = KnowledgeDB()
        except:
            self.knowledge_db = None
        self.chat_sessions = {}
    
    def get_weather(self, city):
        try:
            response = requests.get(f"https://wttr.in/{city}?format=j1", timeout=5)
            if response.status_code == 200:
                data = response.json()['current_condition'][0]
                return f"{data['weatherDesc'][0]['value']}, {data['temp_C']}°C, Humidity {data['humidity']}%, Wind {data['windspeedKmph']} km/h"
        except:
            pass
        return None
    
    def get_response(self, user_message, session_id='default', language='en'):
        msg_lower = user_message.lower().strip()
        
        # Greetings
        if msg_lower in ['hi', 'hello', 'hey', 'namaste', 'hi!', 'hello!']:
            return "Namaste! I'm your farming assistant. Ask me about crops, soil, pests, water, or profit. How can I help you today?"
        
        # Search knowledge database - use top 2 results
        db_context = ""
        if self.knowledge_db:
            results = self.knowledge_db.search(user_message, top_k=2)
            if results:  # Always use if found
                # Combine top results
                for result in results[:2]:
                    db_context += f"\n\n[Expert Knowledge: {result['answer']}]"
        
        # Weather check
        weather_info = ""
        if any(w in msg_lower for w in ['weather', 'temperature', 'rain', 'hava', 'mausam']):
            for city in ['pune', 'mumbai', 'delhi', 'bangalore', 'hyderabad', 'chennai', 'nagpur', 'nashik']:
                if city in msg_lower:
                    weather_data = self.get_weather(city)
                    if weather_data:
                        weather_info = f"\n\n[Current Weather in {city.title()}: {weather_data}]"
                    break
        
        if not client:
            return "Service temporarily unavailable. Please try again."
        
        # Enhanced system prompt for farmers
        system_prompt = """You are an expert farming advisor helping Indian farmers. 

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

Remember: Farmers need clear, actionable advice."""
        
        # Build full context
        full_context = user_message + weather_info + db_context
        
        try:
            if session_id not in self.chat_sessions:
                self.chat_sessions[session_id] = []
            
            # Keep last 3 exchanges for context
            history = self.chat_sessions[session_id][-6:]
            
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": system_prompt},
                    *history,
                    {"role": "user", "content": full_context}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            answer = response.choices[0].message.content
            
            # Update history with original message (not full context)
            self.chat_sessions[session_id].append({"role": "user", "content": user_message})
            self.chat_sessions[session_id].append({"role": "assistant", "content": answer})
            
            return answer
        except Exception as e:
            return "Sorry, I'm having trouble right now. Please ask your question again."

agent = FarmerAgent()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    session_id = request.json.get('session_id', 'default')
    language = request.json.get('language', 'en')
    
    if language == 'mr':
        user_message = f"[IMPORTANT: Respond in Marathi language] {user_message}"
    
    response = agent.get_response(user_message, session_id, language)
    return jsonify({'response': response})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
