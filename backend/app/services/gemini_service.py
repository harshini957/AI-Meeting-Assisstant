from google import genai
from app.core.config import settings
import json
import re

client = genai.Client(api_key=settings.GEMINI_API_KEY)

def generate_action_items(transcript: str):

    prompt = f"""
    Extract structured action items from this transcript.
    Return ONLY a JSON array.

    Transcript:
    {transcript}
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    text_output = response.text.strip()

    # Clean markdown fences
    text_output = re.sub(r"```json|```", "", text_output).strip()

    try:
        json_start = text_output.find("[")
        json_end = text_output.rfind("]") + 1

        clean_json = text_output[json_start:json_end]

        return json.loads(clean_json)

    except Exception as e:
        print("RAW LLM OUTPUT:", text_output)
        raise e