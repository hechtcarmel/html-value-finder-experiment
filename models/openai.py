from typing import Dict, List, Optional, Any
import json
from openai import AsyncOpenAI
from .base import BaseModel, ModelResponse
from prompts.click_value import get_prompt

class OpenAIModel(BaseModel):
    """Interface for OpenAI models."""
    
    def __init__(
        self, 
        api_key: str,
        model_name: str = "gpt-4o", 
    ):
        self.model_name = model_name
        # Initialize with higher timeout (10 minutes) to handle large HTML content
        self.client = AsyncOpenAI(api_key=api_key, timeout=600.0)
    
    async def evaluate_click(
        self, 
        html: str, 
        button_text: str
    ) -> ModelResponse:
        """Evaluate click using OpenAI model."""
        prompt = get_prompt(html, button_text)
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model_name,
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": "You analyze HTML and click data to determine if a click has monetary value."},
                    {"role": "user", "content": prompt}
                ]
            )
            
            try:
                output = json.loads(response.choices[0].message.content)
                
                # Validate response format
                is_value_click = self._parse_boolean(output.get("isValueClick", False))
                value = self._parse_number(output.get("value"))
                currency = self._parse_currency(output.get("currency"))
                
                # If it's not a value click, ensure value and currency are None
                if not is_value_click:
                    value = None
                    currency = None
                
                return ModelResponse(
                    is_value_click=is_value_click,
                    value=value,
                    currency=currency
                )
            except (json.JSONDecodeError, KeyError):
                return ModelResponse(is_value_click=False)
                
        except Exception as e:
            print(f"Error calling OpenAI API: {str(e)}")
            return ModelResponse(is_value_click=False)
    
    def _parse_boolean(self, value: Any) -> bool:
        """Parse a boolean value, handling various formats."""
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.lower() == "true"
        return bool(value)
    
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