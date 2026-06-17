import json
import os
from typing import Dict, Any, Optional
import google.generativeai as genai
from config import settings
from .logger import get_logger

logger = get_logger(__name__)

api_key = settings.GEMINI_API_KEY

if api_key:
    try:
        genai.configure(api_key=api_key)
        logger.info("Configured Google Generative AI (Gemini)")
    except Exception as e:
        logger.error(f"Failed to initialize Gemini client: {e}")
else:
    logger.warning("No GEMINI_API_KEY provided.")

def generate_content(prompt: str, context: str, model: str = None) -> Dict[str, Any]:
    """
    Generates content using Google Gemini.
    
    Args:
        prompt: The system/instruction prompt.
        context: The user input/data context.
        model: Optional model override. Defaults to settings.LLM_MODEL.
        
    Returns:
        Parsed JSON dictionary from the LLM response.
    """
    if not api_key:
        logger.warning("Gemini client not initialized (missing API key?)")
        return {"error": "LLM client not initialized"}

    target_model = model or settings.LLM_MODEL
    
    try:
        logger.info(f"Calling Gemini model: {target_model}")
        
        gemini_model = genai.GenerativeModel(
            target_model,
            system_instruction=prompt,
        )
        
        response = gemini_model.generate_content(
            f"INPUT_DATA:\n{context}",
            generation_config=genai.GenerationConfig(
                temperature=0.2,
                response_mime_type="application/json",
            )
        )
        
        content = response.text.strip()
        logger.debug(f"Gemini response: {content}")
        
        return json.loads(content)
        
    except Exception as e:
        logger.error(f"Gemini API error: {e}")
        return {"error": str(e)}
