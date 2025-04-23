import httpx
from typing import Dict, List, Optional, Any
import json
from .base import BaseModel, ModelResponse
from prompts.click_value import get_prompt

class OllamaModel(BaseModel):
    """Interface for Ollama models."""
    
    def __init__(self, model_name: str = "llama3", base_url: str = "http://localhost:11434"):
        self.model_name = model_name
        self.base_url = base_url
        self.api_url = f"{base_url}/api/generate"
        # Create client with no timeout
        self.client = httpx.AsyncClient(timeout=None)
    
    async def evaluate_click(
        self, 
        html: str, 
        button_text: str
    ) -> ModelResponse:
        """Determine the monetary value of a click using Ollama model."""
        prompt = get_prompt(html, button_text)
        
        try:
            response = await self.client.post(
                self.api_url,
                json={
                    "model": self.model_name,
                    "prompt": prompt,
                    "stream": False,
                    "format": "json"
                }
            )
            response.raise_for_status()
            result = response.json()
            
            # Parse model output (handle potential format issues)
            try:
                output = json.loads(result["response"])
                
                # Validate and parse fields
                value = self._parse_number(output.get("value"))
                currency = self._parse_currency(output.get("currency"))
                
                return ModelResponse(
                    value=value,
                    currency=currency
                )
            except (json.JSONDecodeError, KeyError):
                # Fallback if the model doesn't return valid JSON
                return ModelResponse()
                
        except (httpx.HTTPError, json.JSONDecodeError) as e:
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