import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load API key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

print("API KEY:", api_key)

# Configure API
genai.configure(api_key=api_key)

# List models
try:
    models = genai.list_models()
    print("\nAVAILABLE MODELS:\n")
    
    for m in models:
        print(m.name, "->", m.supported_generation_methods)

except Exception as e:
    print("\nERROR:\n", e)