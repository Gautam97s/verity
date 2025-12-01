import os
from dotenv import load_dotenv
load_dotenv()

class Settings:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{os.path.join(BASE_DIR, 'verity.db')}")
    # API Key Logic
    _openai_key = os.getenv("OPENAI_API_KEY")
    _grok_key = os.getenv("GROK_API_KEY")
    
    if _openai_key and _openai_key.strip():
        OPENAI_API_KEY = _openai_key
        LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o")
    elif _grok_key and _grok_key.strip():
        OPENAI_API_KEY = _grok_key
        LLM_MODEL = os.getenv("LLM_MODEL")
        if not LLM_MODEL:
             LLM_MODEL = "llama3-70b-8192" # Default for Groq
        elif "gpt" in LLM_MODEL.lower():
             raise ValueError(f"Invalid LLM_MODEL '{LLM_MODEL}' for Groq API. Please use a supported model (e.g., llama3-70b-8192).")
    else:
        OPENAI_API_KEY = None
        LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o")

    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")
    TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
    TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
    TWILIO_WHATSAPP_FROM = os.getenv("TWILIO_WHATSAPP_FROM")
    
    SECRET_KEY = os.getenv("SECRET_KEY")
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY must be set in environment variables (check .env file)")


settings = Settings()
