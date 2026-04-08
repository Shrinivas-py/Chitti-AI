from google import genai
from config import settings

client = genai.Client(api_key=settings.GEMINI_API_KEY)


def call_gemini(prompt: str, model: str):
    try:
        response = client.models.generate_content(
            model=model,
            contents=prompt
        )
        return response.text

    except Exception as e:
        print("Gemini error:", e)
        return ""