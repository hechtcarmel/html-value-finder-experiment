from typing import Dict, List, Optional, Any
import json
import re
from anthropic import AsyncAnthropic
from .base import BaseModel, ModelResponse
from prompts.click_value import get_system_prompt, get_user_prompt

class AnthropicModel(BaseModel):
    """Interface for Anthropic Claude models."""
    
    def __init__(
        self, 
        api_key: str,
        model_name: str = "claude-3-opus-20240229", 
    ):
        self.model_name = model_name
        self.client = AsyncAnthropic(api_key=api_key)
    
    async def evaluate_click(
        self, 
        html: str, 
        button_text: str
    ) -> ModelResponse:
        """Determine the monetary value of a click using Anthropic Claude model."""
        system_prompt = get_system_prompt()
        user_prompt = get_user_prompt(html, button_text)
        
        try:
            response = await self.client.messages.create(
                model=self.model_name,
                messages=[
                    {"role": "user", "content": user_prompt}
                ],
                system=system_prompt
            )
            
            try:
                # Extract content from the response
                content = response.content[0].text
                
                # Try to find JSON in the response
                json_match = re.search(r'```json\s*(.*?)\s*```', content, re.DOTALL)
                if json_match:
                    json_str = json_match.group(1)
                else:
                    # If no JSON block found, try to parse the entire content
                    json_str = content
                
                output = json.loads(json_str)
                
                # Validate and parse fields
                value = self._parse_number(output.get("value"))
                currency = self._parse_currency(output.get("currency"))
                
                return ModelResponse(
                    value=value,
                    currency=currency,
                    raw_response=content
                )
            except (json.JSONDecodeError, KeyError, AttributeError) as e:
                print(f"Error parsing response: {str(e)}")
                raw_response = response.content[0].text if hasattr(response, 'content') and response.content else str(response)
                return ModelResponse(raw_response=raw_response)
                
        except Exception as e:
            print(f"Error calling Anthropic API: {str(e)}")
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