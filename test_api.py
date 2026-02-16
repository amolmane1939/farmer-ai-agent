import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.environ.get('GEMINI_API_KEY')
print(f"API Key loaded: {API_KEY[:20]}..." if API_KEY else "No API key found")

genai.configure(api_key=API_KEY)

print("\nTesting API connection...")
try:
    # List available models
    print("\nAvailable models:")
    for model in genai.list_models():
        if 'generateContent' in model.supported_generation_methods:
            print(f"- {model.name}")
    
    # Test with a simple prompt
    print("\nTesting model...")
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content("Say hello")
    print(f"Success! Response: {response.text}")
    
except Exception as e:
    print(f"Error: {e}")
