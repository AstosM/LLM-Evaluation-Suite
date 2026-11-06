import time

from google import genai
from app.config import GOOGLE_API_KEY, GEMINI_MODEL_NAME

client = genai.Client(api_key=GOOGLE_API_KEY)


def generate_response(prompt: str) -> str:
    if not prompt.strip():
        raise ValueError("Prompt cannot be empty.")

    for attempt in range(3):
        try:
            response = client.interactions.create(
                model=GEMINI_MODEL_NAME,
                input=prompt
            )

            if not response.output_text:
                raise RuntimeError("Gemini returned an empty response.")

            return response.output_text

        except Exception as error:
            status = str(
                getattr(error, "code", "")
                or getattr(error, "status_code", "")
            )

            if status not in {"429", "500", "502", "503", "504"}:
                raise

            if attempt == 2:
                raise

            wait_time = 2 ** (attempt + 1)

            print(
                f"Gemini returned {status}. Retrying in {wait_time} seconds...",
                flush=True
            )

            time.sleep(wait_time)

    raise RuntimeError("Gemini request failed after retries.")