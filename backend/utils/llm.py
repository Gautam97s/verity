import json
import os
from typing import Dict, Any, Optional
from openai import Client
import google.generativeai as genai
from config import settings
from .logger import get_logger

logger = get_logger(__name__)

# Initialize Gemini
if settings.GEMINI_API_KEY:
    genai.configure(api_key=settings.GEMINI_API_KEY)

# Initialize Client (OpenAI vs xAI)
api_key = settings.OPENAI_API_KEY
base_url = None # Default to OpenAI (https://api.openai.com/v1)

if api_key:
    if api_key.startswith("xai-"): # Assuming xAI keys might have a prefix, or user sets base_url manually
        logger.info("Detected xAI Key (assumed). Switching Base URL to xAI.")
        base_url = "https://api.x.ai/v1"

try:
    client = Client(
        api_key=api_key,
        base_url=base_url,
        timeout=30.0, # Standard timeout
    ) if api_key else None
except Exception as e:
    logger.error(f"Failed to initialize LLM client: {e}")
    client = None

def generate_content(prompt: str, context: str, model: str = None) -> Dict[str, Any]:
    """
    Generates content using Gemini or OpenAI.
    """
    # 1. Try Gemini first if configured
    if settings.GEMINI_API_KEY:
        try:
            model_name = "gemini-2.0-flash" # Available model
            logger.info(f"Calling Gemini model: {model_name}")
            
            gemini_model = genai.GenerativeModel(model_name)
            
            full_prompt = f"{prompt}\n\nINPUT_DATA:\n{context}"
            
            response = gemini_model.generate_content(
                full_prompt
            )
            
            content = response.text.strip()
            logger.debug(f"Gemini response: {content}")
            
            # Clean up markdown code blocks if present
            if content.startswith("```"):
                content = content.strip("`")
                if content.startswith("json"):
                    content = content[4:]
            
            return json.loads(content)
            
        except Exception as e:
            logger.error(f"Gemini API error: {e}")
            return {"error": str(e)}

    # 2. Fallback to OpenAI
    if not client:
        logger.warning("LLM client not initialized (missing API key?)")
        return {"error": "LLM client not initialized"}

    target_model = model or settings.LLM_MODEL
    
    try:
        logger.info(f"Calling LLM model: {target_model}")
        
        # Chat completion
        response = client.chat.completions.create(
            model=target_model,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": f"INPUT_DATA:\n{context}"}
            ],
            temperature=0.2, # Low temperature for deterministic JSON
            # response_format={"type": "json_object"} # Enforce JSON mode if supported, else prompt handles it
        )
        
        content = response.choices[0].message.content.strip()
        logger.debug(f"LLM response: {content}")
        
        # Clean up markdown code blocks if present
        if content.startswith("```"):
            content = content.strip("`")
            if content.startswith("json"):
                content = content[4:]
        
        return json.loads(content)
        
    except Exception as e:
        logger.error(f"LLM API error: {e}")
        return {"error": str(e)}
