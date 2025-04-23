from abc import ABC, abstractmethod
from typing import Dict, Optional, Union, List, Any
import json

class ModelResponse:
    """Structured response from LLM models."""
    
    def __init__(
        self, 
        value: Optional[float] = None, 
        currency: Optional[str] = None
    ):
        self.value = self._validate_value(value)
        self.currency = self._validate_currency(currency)
    
    def _validate_value(self, value: Any) -> Optional[float]:
        """Validate that value is a number or None."""
        if value is None:
            return None
        try:
            # Convert to float if it's a number
            if isinstance(value, (int, float)):
                return float(value)
            # Try to convert string to float
            if isinstance(value, str) and value.replace('.', '', 1).isdigit():
                return float(value)
            # Not a valid number, return None
            return None
        except (ValueError, TypeError):
            return None
    
    def _validate_currency(self, currency: Any) -> Optional[str]:
        """Validate that currency is a 3-letter code or None."""
        if currency is None:
            return None
        if isinstance(currency, str):
            # Check if it's a likely currency code (3 letters)
            if len(currency) == 3 and currency.isalpha():
                return currency.upper()
            # Handle some common currency symbols
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
            if currency in currency_map:
                return currency_map[currency]
        # Invalid format, return None
        return None
    
    def to_json(self) -> str:
        """Convert response to JSON string."""
        return json.dumps({
            "value": self.value,
            "currency": self.currency
        })
    
    def to_dict(self) -> Dict:
        """Convert response to dictionary."""
        return {
            "value": self.value,
            "currency": self.currency
        }

class BaseModel(ABC):
    """Base class for all LLM models."""
    
    @abstractmethod
    async def evaluate_click(
        self, 
        html: str, 
        button_text: str
    ) -> ModelResponse:
        """Determine the monetary value of a click."""
        pass 