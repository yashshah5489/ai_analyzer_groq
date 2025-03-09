import os
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logger
logging.basicConfig(
    level=logging.INFO if os.getenv('LOG_LEVEL') != 'DEBUG' else logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# API Keys (store these securely in production)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# Check for critical missing API keys
if not GROQ_API_KEY:
    logger.warning("GROQ_API_KEY is not set. The application will not be able to generate AI responses.")

if not TAVILY_API_KEY:
    logger.warning("TAVILY_API_KEY is not set. News fetching functionality will be disabled.")

# MongoDB configuration
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/finance_assistant")

# Default LLM settings
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "llama3.3-70b")
DEFAULT_TEMPERATURE = float(os.getenv("DEFAULT_TEMPERATURE", "0.7"))
DEFAULT_MAX_TOKENS = int(os.getenv("DEFAULT_MAX_TOKENS", "1024"))

# Currency settings
DEFAULT_CURRENCY = os.getenv("DEFAULT_CURRENCY", "USD")
INDIAN_CURRENCY = os.getenv("INDIAN_CURRENCY", "INR")

# Debug mode
DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")