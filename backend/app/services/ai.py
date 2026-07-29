import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel(
    "gemini-3.5-flash"
)

# not using this anymore
def generate_summary(location: str):

    prompt = f"""
    Give me a short travel summary for {location}.

    Requirements:
    - exactly 2 lines
    - mention key attractions
    - mention why people visit
    - concise and easy to read
    """

    response = model.generate_content(prompt)

    return response.text.strip()