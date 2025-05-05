"""
TODO MVP v0.1
"""

import os
import time
import json
from typing import Dict, Any, Optional
from openai import OpenAI
from dotenv import load_dotenv

class LLMAdapter:
    """Adapter for interacting with large language models."""
    
    def __init__(self, api_key=None):
        pass
    
    def generate_response(self, prompt, parameters=None):
        """
        Generate a response from the language model.
        
        Args:
            prompt: The input prompt for the language model
            parameters: Optional parameters to customize the generation
            
        Returns:
            Generated text response from the model
        """
        pass 


class OpenRouterClient:
    """
    Client for interacting with OpenRouter-compatible LLM APIs.
    Uses the openai client library to make requests and handles retries.
    """
    
    def __init__(self):
        """
        Initialize the OpenRouter client with API key from environment variables.
        Loads environment variables from .env file if available.
        """
        # Try to load from .env file
        load_dotenv()
        
        # Get API key from environment
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY environment variable is not set")
        
        # Initialize OpenAI client with API key
        self.client = OpenAI(
            api_key=self.api_key,
            base_url="https://openrouter.ai/api/v1"
        )
        
        # Default model
        self.model = "openrouter/llama-3-70b-instruct"
    
    def classify_line(self, text: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Classify a line of text within given context.
        
        Args:
            text: The text to classify
            context: Dictionary of contextual information to help with classification
            
        Returns:
            Dictionary containing:
                - code: The classification code
                - confidence: Confidence score (0.0-1.0)
                - explanation: Explanation for the classification
                
        Raises:
            Exception: If all retry attempts fail
        """
        max_attempts = 3
        
        for attempt in range(1, max_attempts + 1):
            try:
                # Prepare system message to guide model behavior
                system_message = """You are a text classifier that analyzes lines of code/text.
                Return a JSON object with the following fields:
                - code: a short classification code
                - confidence: a value between 0.0 and 1.0 indicating your confidence
                - explanation: a brief explanation of your classification
                
                Format your entire response as valid JSON only, nothing else."""
                
                # Prepare prompt with context
                context_str = json.dumps(context)
                user_prompt = f"Classify this text (context: {context_str}):\n\n{text}"
                
                # Make API request
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_message},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.2,  # Low temperature for more deterministic results
                    response_format={"type": "json_object"},
                    extra_headers={
                        "HTTP-Referer": "http://localhost",   # for OpenRouter free-tier
                        "X-Title": "DialogueCoder-PlanB"
                    }
                )
                
                # Parse response
                response_text = response.choices[0].message.content
                result = json.loads(response_text)
                
                # Ensure all required fields are present
                if not all(key in result for key in ["code", "confidence", "explanation"]):
                    raise ValueError("Response missing required fields")
                
                return result
                
            except Exception as e:
                # If this is the last attempt, re-raise the exception
                if attempt == max_attempts:
                    raise
                
                # Calculate backoff delay: 2^attempt * 100ms
                delay = (2 ** attempt) * 0.1
                time.sleep(delay)
        
        # This should never be reached due to the raise in the except block
        raise RuntimeError("Failed all retry attempts") 