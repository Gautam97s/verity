import os
from dotenv import load_dotenv
load_dotenv()

class Settings:
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./verity.db")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")

settings = Settings()
