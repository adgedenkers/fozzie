import os
import openai
import logging
from typing import List, Dict, Optional

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Load API key from environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def set_openai_api_key(api_key: str):
    """Set the OpenAI API key dynamically."""
    global OPENAI_API_KEY
    OPENAI_API_KEY = api_key
    logging.info("OpenAI API key set successfully.")

def send_message(
    messages: List[Dict[str, str]],
    model: str = "gpt-4",
    temperature: float = 0.7,
    max_tokens: int = 500,
    top_p: float = 1.0,
    frequency_penalty: float = 0.0,
    presence_penalty: float = 0.0
) -> Optional[str]:
    """Send a message to the OpenAI chat model and return the response."""
    if not OPENAI_API_KEY:
        logging.error("OpenAI API key is not set. Use set_openai_api_key() to configure it.")
        return None

    try:
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty
        )
        return response.choices[0].message.content.strip()
    except openai.OpenAIError as e:
        logging.error(f"OpenAI API request failed: {e}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return None
