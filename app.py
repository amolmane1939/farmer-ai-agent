from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
import requests
from openai import OpenAI

load_dotenv()

app = Flask(__name__)

# Configure OpenAI (using Groq's OpenAI-compatible API)
GROQ_KEY = os.environ.get('GROQ_API_KEY')
if GROQ_KEY:
    client = OpenAI(
        api_key=GROQ_KEY,
        base_url="https://api.groq.com/openai/v1"
    )
else:
    client = None

class FarmerAgent:
    def __init__(self):
        self.system_prompt = """
You are a helpful farming assistant with access to real-time weather data.

IMPORTANT RULES:
- Give SHORT answers (2-4 sentences)
- Answer ONLY what the farmer asks
- When weather data is provided in [WEATHER DATA] brackets, YOU MUST USE THAT EXACT DATA
- Include ALL details from the weather data: temperature, feels like, humidity, wind speed and direction
- Don't make up weather information - only use what's provided
- Use simple, clear language
- Be direct and accurate

PRIVACY & SECURITY:
- NEVER ask for personal information like phone numbers, addresses, bank details
- NEVER store or remember sensitive personal data
- Focus only on farming advice
- If user shares personal info, remind them not to share sensitive details
"""
        self.chat_sessions = {}
        
        # Offline knowledge base
        self.offline_knowledge = {
            "weather": "Check local weather apps like IMD or Meghdoot for accurate forecasts. Plan your irrigation and sowing based on rainfall predictions.",
            "pune weather": "Pune is in monsoon season with temperatures 28-32°C. Expect moderate rainfall. Good time for Kharif crops like soybean, rice, and maize.",
            "crop": "Popular crops: Rice (monsoon), Wheat (winter), Soybean (Kharif), Cotton (warm weather), Sugarcane (year-round with irrigation).",
            "which crop": "Choose based on: 1) Season (Kharif/Rabi), 2) Soil type, 3) Water availability, 4) Market demand. Tell me your season and I'll suggest specific crops.",
            "soil": "Improve soil: Use organic compost, practice crop rotation, test pH regularly, add green manure, avoid excessive chemicals.",
            "pest": "Pest control: Use neem spray, check crops daily, remove infected plants early, try IPM (Integrated Pest Management), encourage natural predators.",
            "profit": "Increase profit: Sell directly at mandis, join farmer cooperatives, reduce input costs with organic methods, try value-added products.",
            "drought": "Drought management: Use drip irrigation, mulch soil to retain moisture, plant drought-resistant varieties, harvest rainwater.",
            "fertilizer": "Use balanced NPK based on soil test. Organic options: compost, vermicompost, green manure. Apply before rain for better absorption.",
            "irrigation": "Efficient irrigation: Drip system saves 40% water, sprinkler for large fields, check soil moisture before watering."
        }
    
    def get_weather(self, city):
        """Get real-time weather data using free API"""
        try:
            # Using wttr.in - free, no API key needed
            url = f"https://wttr.in/{city}?format=j1"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                current = data['current_condition'][0]
                temp = current['temp_C']
                feels_like = current['FeelsLikeC']
                humidity = current['humidity']
                wind_speed = current['windspeedKmph']
                wind_dir = current['winddir16Point']
                weather_desc = current['weatherDesc'][0]['value']
                
                return f"Current weather in {city}: {weather_desc}, Temperature: {temp}°C (feels like {feels_like}°C), Humidity: {humidity}%, Wind: {wind_speed} km/h {wind_dir}"
            return None
        except:
            return None
    
    def get_offline_response(self, message):
        msg_lower = message.lower()
        
        for keyword, response in self.offline_knowledge.items():
            if keyword in msg_lower:
                return response
        
        return "I can help with: weather forecasts, crop selection, soil health, pest control, irrigation, fertilizers, and profit tips. What would you like to know?"
    
    def get_response(self, user_message, session_id='default'):
        if not client:
            return "🤖 (Offline Mode) " + self.get_offline_response(user_message)
        
        # Check if asking about weather
        msg_lower = user_message.lower()
        weather_keywords = ['weather', 'temperature', 'wind', 'rain', 'humidity', 'forecast', 'hava', 'तापमान']
        if any(keyword in msg_lower for keyword in weather_keywords):
            # Try to extract city name
            cities = ['pune', 'mumbai', 'delhi', 'bangalore', 'hyderabad', 'chennai', 'kolkata', 'ahmedabad', 'nagpur', 'nashik', 'पुणे', 'मुंबई']
            for city in cities:
                if city in msg_lower:
                    city_name = city.replace('पुणे', 'pune').replace('मुंबई', 'mumbai')
                    weather_data = self.get_weather(city_name)
                    if weather_data:
                        user_message = f"{user_message}\n\n[WEATHER DATA - Use this to answer: {weather_data}]"
                    break
        
        try:
            # Get chat history
            if session_id not in self.chat_sessions:
                self.chat_sessions[session_id] = []
            
            history = self.chat_sessions[session_id]
            messages = [
                {"role": "system", "content": self.system_prompt},
                *history,
                {"role": "user", "content": user_message}
            ]
            
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages,
                temperature=0.7,
                max_tokens=150,
            )
            
            answer = response.choices[0].message.content
            
            # Update history
            history.append({"role": "user", "content": user_message})
            history.append({"role": "assistant", "content": answer})
            
            return answer
        except Exception as e:
            return "🤖 (Offline Mode) " + self.get_offline_response(user_message)

agent = FarmerAgent()

# Fallback offline responses
OFFLINE_TIPS = {
    "climate": "For drought: Use drip irrigation, mulch soil. For floods: Ensure drainage, use raised beds.",
    "soil": "Practice crop rotation, use organic compost, get soil tested regularly.",
    "pest": "Use Integrated Pest Management (IPM), neem pesticides, monitor crops regularly.",
    "profit": "Diversify crops, reduce input costs, explore direct-to-consumer sales.",
    "infrastructure": "Join farmer cooperatives for shared storage, check government subsidies."
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    session_id = request.json.get('session_id', 'default')
    language = request.json.get('language', 'en')
    
    # Add language instruction to message
    if language == 'mr':
        user_message = f"[Respond in Marathi language] {user_message}"
    
    response = agent.get_response(user_message, session_id)
    return jsonify({'response': response})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
