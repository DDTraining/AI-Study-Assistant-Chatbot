from dotenv import load_dotenv
import os

# Load the .env file
load_dotenv()

# Retrieve the API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is missing. Please check your .env file.")
