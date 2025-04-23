from typing import List
from examples.click_examples import EXAMPLES
import json

def get_system_prompt() -> str:
    """Generate the system prompt for click value evaluation."""
    
    system_prompt = """Your task is to analyze the HTML context and clicked button text to determine the monetary value of a click (For example - how much money the item costs).
Focus on finding the price most closely associated with the clicked button.

OUTPUT: 
A JSON object with the following structure:
{
  "value": number | null,        // the NUMERIC monetary value if detected with high confidence (e.g., 149.99), null if uncertain
  "currency": string | null      // the currency code (USD, EUR, GBP, etc.) if detected with high confidence, null if uncertain
}

IMPORTANT RULES:

1. If there are multiple prices on the page, consider the context and structure of the page to determine the price.
2. Consider the context: if the button is inside a product card, the price in that card is relevant. If it's a checkout button, the total price is relevant.
3. Only include specific "value" and "currency" if you can determine them to be the price that the clicked button is associated with.
4. If very uncertain about the value or currency, return null for those fields.
5. Return the numeric value without currency symbols.
6. Currency should be a standard 3-letter code (USD, EUR, GBP, etc.).
7. The "value" field MUST be a number (like 10.99) or null, NEVER a boolean or string.
8. The "currency" field should be a 3-letter currency code (e.g., "USD") or null.

Examples of CORRECT values:
- value: 149.99 (numeric)
- value: null (when monetary value can't be determined)
- currency: "USD" (3-letter code)
- currency: null (when currency can't be determined)

Examples of INCORRECT values:
- value: true (boolean, not numeric)
- value: "149.99" (string, not numeric)
- currency: "$" (symbol, not 3-letter code)
- currency: "dollars" (word, not 3-letter code)

Here are examples of how to analyze different SIMPLE scenarios:
"""

    # Add examples
    for i, example in enumerate(EXAMPLES):
        # Create a simplified response that excludes isValueClick
        modified_response = {
            "value": example['response']['value'],
            "currency": example['response']['currency']
        }
        
        system_prompt += f"""
EXAMPLE {i+1}:
HTML: {example['html']}
Button Text: {example['button_text']}
Analysis: 
- {'Value: ' + str(example['response']['value']) if example['response']['value'] is not None else 'Value is uncertain'}
- {'Currency: ' + str(example['response']['currency']) if example['response']['currency'] is not None else 'Currency is uncertain'}
OUTPUT: {json.dumps(modified_response)}

"""
    
    return system_prompt

def get_user_prompt(html: str, button_text: str) -> str:
    """Generate the user prompt with the current case to analyze."""
    
    return f"""HTML: {html}
Button Text: {button_text}

Respond ONLY with a valid JSON object following the exact format specified in the system prompt.
Focus on the price closest to the button text element in the HTML structure.
Make sure the "value" field is a numeric value or null, never a boolean or string.
Make sure the "currency" field is a 3-letter currency code or null."""

def get_prompt(html: str, button_text: str) -> str:
    """Legacy function that combines system and user prompts for backward compatibility."""
    return get_system_prompt() + "\n\nNow analyze this case:\n" + get_user_prompt(html, button_text)