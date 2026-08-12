import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file")

try:
    from google import genai
    client = genai.Client(api_key=api_key)
    
    print("🔍 Listing available models...\n")
    for model in client.models.list():
        print(f" - {model.name}")
        if hasattr(model, 'supported_generation_methods'):
            print(f"   Supports: {model.supported_generation_methods}")
except Exception as e:
    print(f"❌ Error: {e}")