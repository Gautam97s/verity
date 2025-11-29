import os
from dotenv import load_dotenv
load_dotenv()

class Settings:
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./verity.db")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    GROK_API_KEY = os.getenv("GROK_API_KEY")
    LLM_MODEL = os.getenv("LLM_MODEL", "grok-beta")
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")
    TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
    TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
    TWILIO_WHATSAPP_FROM = os.getenv("TWILIO_WHATSAPP_FROM")


settings = Settings()
