from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

GROQ_KEY = os.environ.get('GROQ_API_KEY')
print(f"Groq API Key loaded: {GROQ_KEY[:20]}..." if GROQ_KEY else "No key found")

try:
    client = Groq(api_key=GROQ_KEY)
    
    print("\nTesting Groq API...")
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Say hello in one sentence"}
        ],
        max_tokens=50,
    )
    
    print(f"Success! Response: {response.choices[0].message.content}")
    print(f"\nSpeed: {response.usage.total_tokens} tokens")
    
except Exception as e:
    print(f"Error: {e}")
