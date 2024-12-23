import os
from dotenv import load_dotenv

# Load environment variables from config.env
load_dotenv(os.path.join(os.path.dirname(__file__), "config.env"))

EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECIPIENT = os.getenv("EMAIL_RECIPIENT")
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DEFAULT_QUERY = os.getenv("DEFAULT_QUERY", "neuroscience")