import ollama
from typing import Dict, List, Optional, Any
import json
import asyncio
from .base import BaseModel, ModelResponse
from prompts.click_value import get_system_prompt, get_user_prompt

class OllamaModel(BaseModel):
    """Interface for Ollama models."""
    
    def __init__(self, model_name: str = "llama3.2", base_url: str = "http://localhost:11434"):
        self.model_name = model_name
        self.base_url = base_url
        ollama.base_url = base_url  # Set the base URL directly
    
    async def evaluate_click(
        self, 
        html: str, 
        button_text: str
    ) -> ModelResponse:
        """Determine the monetary value of a click using Ollama model."""
        system_prompt = get_system_prompt()
        user_prompt = get_user_prompt(html, button_text)
        
        try:
            # Use asyncio.to_thread to make synchronous ollama library call non-blocking
            response = await asyncio.to_thread(
                ollama.chat,
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                format="json"
            )
            
            # Parse model output
            try:
                # Extract the content from the response
                response_content = response["message"]["content"]
                output = json.loads(response_content)
                
                # Validate and parse fields
                value = self._parse_number(output.get("value"))
                currency = self._parse_currency(output.get("currency"))
                
                return ModelResponse(
                    value=value,
                    currency=currency,
                    raw_response=response_content
                )
            except (json.JSONDecodeError, KeyError) as e:
                print(f"Error parsing response: {str(e)}")
                # Fallback if the model doesn't return valid JSON
                raw_response = response.get("message", {}).get("content", "") if isinstance(response, dict) else str(response)
                return ModelResponse(raw_response=raw_response)
                
        except Exception as e:
            print(f"Error calling Ollama API: {str(e)}")
            return ModelResponse()
    
    def _parse_number(self, value: Any) -> Optional[float]:
        """Parse a numeric value, handling various formats."""
        if value is None:
            return None
        if isinstance(value, (int, float)):
            return float(value)
        if isinstance(value, str):
            try:
                # Remove commas from numbers like "1,234.56"
                cleaned = value.replace(',', '')
                return float(cleaned)
            except ValueError:
                return None
        return None
    
    def _parse_currency(self, value: Any) -> Optional[str]:
        """Parse a currency code, handling various formats."""
        if value is None:
            return None
        if isinstance(value, str):
            # Currency symbols to codes
            currency_map = {
                "$": "USD",
                "€": "EUR",
                "£": "GBP",
                "¥": "JPY",
                "₹": "INR",
                "dollars": "USD",
                "euros": "EUR",
                "pounds": "GBP",
                "yen": "JPY",
                "rupees": "INR",
                "shekels": "ILS",
            }
            
            # Clean the value
            value = value.strip()
            
            # Check for symbol mapping
            if value in currency_map:
                return currency_map[value]
            
            # Check if it's already a 3-letter code
            if len(value) == 3 and value.isalpha():
                return value.upper()
        
        return None