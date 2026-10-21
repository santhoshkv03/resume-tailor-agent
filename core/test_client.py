import os
from google import genai

def test_gemini():
    api_key = os.environ.get("GEMINI_API_KEY")
    print(f"API Key present: {bool(api_key)}")
    if api_key:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents="Say 'Gemini API is ready for resume tailoring!' in 1 sentence."
        )
        print("Response:", response.text)

if __name__ == "__main__":
    test_gemini()
