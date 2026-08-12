import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file")

try:
    from google import genai
    client = genai.Client(api_key=api_key)
    
    # ✅ Use a model from the list that you saw
    response = client.models.generate_content(
        model="gemini-flash-latest",  # This is from your list!
        contents="Say 'Hello Project VIGIL!' in exactly 3 words."
    )
    print(" Gemini connection successful!")
    print(f" Response: {response.text}")
except Exception as e:
    print(f" Error: {e}")