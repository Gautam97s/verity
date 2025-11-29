import json
import os
from typing import Dict, Any, Optional
from openai import Client
from config import settings
from .logger import get_logger

logger = get_logger(__name__)

# Initialize Client (OpenAI vs Groq vs xAI)
api_key = settings.OPENAI_API_KEY
base_url = None # Default to OpenAI (https://api.openai.com/v1)

if api_key:
    if api_key.startswith("gsk_"):
        logger.info("Detected Groq API Key. Switching Base URL to Groq.")
        base_url = "https://api.groq.com/openai/v1"
    elif api_key.startswith("xai-"): # Assuming xAI keys might have a prefix, or user sets base_url manually
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
    Generates content using Grok (via OpenAI SDK).
    
    Args:
        prompt: The system/instruction prompt.
        context: The user input/data context.
        model: Optional model override. Defaults to settings.LLM_MODEL.
        
    Returns:
        Parsed JSON dictionary from the LLM response.
    """
    if not client:
        logger.warning("Grok client not initialized (missing API key?)")
        return {"error": "LLM client not initialized"}

    target_model = model or settings.LLM_MODEL
    
    # Auto-fix model if using Groq
    if client and client.base_url.host == "api.groq.com":
        if "gpt" in target_model or "grok" in target_model:
             logger.warning(f"Groq API does not support '{target_model}'. Switching to 'llama3-8b-8192'.")
             target_model = "llama3-8b-8192"
    
    try:
        logger.info(f"Calling LLM model: {target_model}")
        
        # Grok chat completion
        response = client.chat.completions.create(
            model=target_model,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": f"INPUT_DATA:\n{context}"}
            ],
            temperature=0.2, # Low temperature for deterministic JSON
            response_format={"type": "json_object"} # Enforce JSON mode if supported, else prompt handles it
        )
        
        content = response.choices[0].message.content.strip()
        logger.debug(f"Grok response: {content}")
        
        # Clean up markdown code blocks if present (Grok might still wrap in ```json ... ```)
        if content.startswith("```"):
            content = content.strip("`")
            if content.startswith("json"):
                content = content[4:]
        
        return json.loads(content)
        
    except Exception as e:
        logger.error(f"Grok API error: {e}")
        return {"error": str(e)}
