import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

MODEL_NAME = "models/gemini-1.5-flash"
TEMPERATURE = 0.3
TOP_P = 0.9