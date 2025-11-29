import sys
import os

# Add the backend directory to sys.path so that absolute imports (e.g. 'from config import settings')
# work even when running from the project root (e.g. 'uvicorn backend.main:app').
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)
