import json
import os
from typing import Dict, Any, Optional
from openai import Client
from config import settings
from .logger import get_logger

logger = get_logger(__name__)

# Initialize OpenAI client for Grok
# Base URL for xAI: https://api.x.ai/v1
try:
    client = Client(
        api_key=settings.GROK_API_KEY,
        base_url="https://api.x.ai/v1",
    ) if settings.GROK_API_KEY else None
except Exception as e:
    logger.error(f"Failed to initialize Grok client: {e}")
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
        return {}

    target_model = model or settings.LLM_MODEL
    
    try:
        logger.info(f"Calling Grok model: {target_model}")
        
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
