import google.generativeai as genai
from config import Config


class AIService:
    @staticmethod
    def ask_gemini(text):
        if not Config.GEMINI_API_KEY:
            return "Gemini API key is missing. Please check your .env file."

        try:
            genai.configure(api_key=Config.GEMINI_API_KEY)

            model = genai.GenerativeModel(Config.GEMINI_MODEL)
            response = model.generate_content(text)

            if not response:
                return "No response received from Gemini."

            response_text = getattr(response, "text", "").strip()

            if not response_text:
                return "Gemini returned an empty response."

            response_text = response_text.replace("*", "")
            formatted_response = response_text.replace(". ", ".\n")

            return formatted_response

        except Exception as e:
            print(f"[ERROR] Gemini failed: {e}")
            return "Sorry, I could not get a response from Gemini right now."