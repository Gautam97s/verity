import os
from dotenv import load_dotenv
load_dotenv()

class Settings:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{os.path.join(BASE_DIR, 'verity.db')}")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o") # Default to OpenAI model
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")
    TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
    TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
    TWILIO_WHATSAPP_FROM = os.getenv("TWILIO_WHATSAPP_FROM")


settings = Settings()
