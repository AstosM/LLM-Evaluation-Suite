import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GEMINI_MODEL_NAME = os.getenv(
    "GEMINI_MODEL_NAME",
    "gemini-3.8-flash"
)

if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY is missing. Check your .env file.")