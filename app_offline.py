from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

class OfflineFarmerAgent:
    def __init__(self):
        self.knowledge = {
            "weather": ["Check local weather apps", "Monitor rainfall patterns", "Plan irrigation based on forecast"],
            "crop": ["Rice: Good for monsoon", "Wheat: Winter crop", "Soybean: Kharif season", "Cotton: Needs warm weather"],
            "soil": ["Test soil pH regularly", "Add organic compost", "Practice crop rotation", "Use green manure"],
            "pest": ["Use neem spray", "Check crops daily", "Remove infected plants", "Use IPM methods"],
            "profit": ["Sell directly to market", "Join farmer groups", "Reduce input costs", "Try value-added products"],
            "water": ["Use drip irrigation", "Harvest rainwater", "Mulch to retain moisture", "Check for leaks"]
        }
        self.chat_history = {}
    
    def get_response(self, message, session_id='default'):
        msg_lower = message.lower()
        
        # Store history
        if session_id not in self.chat_history:
            self.chat_history[session_id] = []
        self.chat_history[session_id].append(message)
        
        # Match keywords
        for topic, tips in self.knowledge.items():
            if topic in msg_lower:
                return f"{tips[0]}. {tips[1]}."
        
        # Check previous context
        if len(self.chat_history[session_id]) > 1:
            prev = self.chat_history[session_id][-2].lower()
            for topic, tips in self.knowledge.items():
                if topic in prev:
                    return f"For {topic}: {tips[2]}"
        
        return "I can help with: weather, crops, soil, pests, profit, and water management. What do you need help with?"

agent = OfflineFarmerAgent()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    session_id = request.json.get('session_id', 'default')
    response = agent.get_response(user_message, session_id)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
