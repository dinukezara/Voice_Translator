import os
import logging
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
LOG_LEVEL_STR = os.getenv("LOG_LEVEL", "INFO").upper()
LOG_LEVEL = getattr(logging, LOG_LEVEL_STR, logging.INFO)

# Create logs directory if it doesn't exist
os.makedirs("logs", exist_ok=True)

# Define generic logger configuration
logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/app.log", encoding="utf-8"),
        logging.StreamHandler(sys.stdout)
    ]
)

def get_logger(name: str) -> logging.Logger:
    """Returns a configured logger for the specified module name."""
    return logging.getLogger(name)

# Configuration Variables
DEFAULT_SOURCE: str = os.getenv("DEFAULT_SOURCE", "English")
DEFAULT_TARGET: str = os.getenv("DEFAULT_TARGET", "Spanish")
HISTORY_FILE_PATH: str = os.getenv("HISTORY_FILE_PATH", "data/history.txt")

# Language Mappings
LANGUAGE_MAP = {
    "English": {"stt": "en-US", "translate": "en", "tts": "en"},
    "Spanish": {"stt": "es-ES", "translate": "es", "tts": "es"},
    "French": {"stt": "fr-FR", "translate": "fr", "tts": "fr"},
    "German": {"stt": "de-DE", "translate": "de", "tts": "de"},
    "Hindi": {"stt": "hi-IN", "translate": "hi", "tts": "hi"},
    "Tamil": {"stt": "ta-IN", "translate": "ta", "tts": "ta"},
}

LANGUAGE_CODE_MAP = {
    "en": "English",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "hi": "Hindi",
    "ta": "Tamil",
}

DEFAULT_TARGET = "Spanish"
