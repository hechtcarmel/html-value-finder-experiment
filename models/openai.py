from typing import Dict, List, Optional, Any
import json
from openai import AsyncOpenAI
from .base import BaseModel, ModelResponse
from prompts.click_value import get_system_prompt, get_user_prompt

class OpenAIModel(BaseModel):
    """Interface for OpenAI models."""
    
    def __init__(
        self, 
        api_key: str,
        model_name: str = "gpt-4o-mini", 
    ):
        self.model_name = model_name
        # Initialize with higher timeout (10 minutes) to handle large HTML content
        self.client = AsyncOpenAI(api_key=api_key, timeout=600.0)
    
    async def evaluate_click(
        self, 
        html: str, 
        button_text: str
    ) -> ModelResponse:
        """Determine the monetary value of a click using OpenAI model."""
        system_prompt = get_system_prompt()
        user_prompt = get_user_prompt(html, button_text)
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model_name,
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            )
            
            try:
                output = json.loads(response.choices[0].message.content)
                
                # Validate and parse fields
                value = self._parse_number(output.get("value"))
                currency = self._parse_currency(output.get("currency"))
                
                return ModelResponse(
                    value=value,
                    currency=currency
                )
            except (json.JSONDecodeError, KeyError):
                return ModelResponse()
                
        except Exception as e:
            print(f"Error calling OpenAI API: {str(e)}")
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