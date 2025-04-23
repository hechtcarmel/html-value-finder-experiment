from typing import List
from examples.click_examples import EXAMPLES

def get_prompt(html: str, button_text: str) -> str:
    """Generate a prompt for click value evaluation with multi-shot examples."""
    
    # Create base prompt
    base_prompt = f"""
Your task is to analyze the HTML context and clicked button text to determine if a click has monetary value.

INPUT:
- HTML content surrounding the click
- Text content of the clicked button

OUTPUT: 
A JSON object with the following structure:
{{
  "isValueClick": boolean,   // true if this is a purchase/add to cart/etc. click
  "value": number | null,    // the NUMERIC monetary value if detected (e.g., 149.99), null if not applicable
  "currency": string | null  // the currency code (USD, EUR, GBP, etc.) if detected, null if not applicable
}}

IMPORTANT RULES:
1. Only return true for "isValueClick" if you're highly confident this is a purchase-related action
2. Only include "value" and "currency" if you can determine them with high confidence
3. If uncertain about the value or currency, return null for those fields
4. Return the numeric value without currency symbols
5. Currency should be a standard 3-letter code (USD, EUR, GBP, etc.)
6. For subscription prices, return the value shown (e.g., $9.99/month should return 9.99)
7. Search for the button text in the HTML to determine context for evaluation
8. Look for price information near the button or in relevant containers
9. The "value" field MUST be a number (like 10.99) or null, NEVER a boolean or string
10. The "currency" field should be a 3-letter currency code (e.g., "USD") or null

Examples of CORRECT values:
- value: 149.99 (numeric)
- value: 15 (numeric)
- value: null (when no monetary value is found)
- currency: "USD" (3-letter code)
- currency: null (when no currency is found)

Examples of INCORRECT values:
- value: true (boolean, not numeric)
- value: "149.99" (string, not numeric)
- currency: "$" (symbol, not 3-letter code)
- currency: "dollars" (word, not 3-letter code)

Here are examples of how to analyze different scenarios:
"""

    # Add examples
    for i, example in enumerate(EXAMPLES):
        base_prompt += f"""
EXAMPLE {i+1}:
HTML: {example['html']}
Button Text: {example['button_text']}
Analysis: 
- This {'is' if example['response']['isValueClick'] else 'is not'} a value click
- {'Value: ' + str(example['response']['value']) if example['response']['value'] is not None else 'No clear value found'}
- {'Currency: ' + str(example['response']['currency']) if example['response']['currency'] is not None else 'No clear currency found'}
OUTPUT: {example['response_json']}

"""

    # Add the current request
    base_prompt += f"""
Now analyze this case:
HTML: {html}
Button Text: {button_text}

Respond ONLY with a valid JSON object following the exact format specified above.
Make sure the "value" field is a numeric value or null, never a boolean or string.
Make sure the "currency" field is a 3-letter currency code or null.
"""
    
    return base_prompt 