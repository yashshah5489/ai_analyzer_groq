import os
from groq import Groq
from dotenv import load_dotenv
# Load environment variables from .env file (if available)
load_dotenv()
import dotenv
# print(dotenv.find_dotenv())
import os



from dotenv import load_dotenv
import os

# load_dotenv(dotenv_path="C:\Users\yashs\Desktop\AI_Financial_Analyzer_Groq\.env")  # Replace with actual path

api_key = os.getenv("GROQ_API_KEY")
print(f"Explicit API Key: {api_key}")

# print(os.environ)  # Print all environment variables
# print(f"GROQ_API_KEY: {os.getenv('GROQ_API_KEY')}")

# Get API key from environment
api_key = os.environ.get("GROQ_API_KEY")
client = Groq(
    # This is the default and can be omitted
    api_key=api_key,
)
print(api_key)
models = client.models.list()

print(models)