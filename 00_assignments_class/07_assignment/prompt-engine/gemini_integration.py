import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

def setup_gemini():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return False
    genai.configure(api_key=api_key)
    return True

def enhance_prompt_with_gemini(use_case_id, answers, base_prompt):
    if not setup_gemini():
        return None
    try:
        system_prompt = """You are an expert prompt engineer. Your task is to enhance 
        and improve the given prompt to make it more effective for AI tools."""

        user_prompt = f"""
        Use case: {use_case_id}

        User provided:
        {', '.join([f"{k}: {v}" for k, v in answers.items()])}

        Base prompt:
        {base_prompt}

        Please enhance this prompt to make it more effective. Return only the enhanced prompt.
        """

        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(user_prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Gemini enhancement failed: {e}")
        return None