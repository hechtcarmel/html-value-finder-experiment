# Click Value Analyzer

A Python application that analyzes HTML content and button text to determine if a click has monetary value, and extracts the value and currency.

## Features

- Analyzes HTML context around a clicked button
- Determines if a click has monetary value (e.g., "Add to Cart", "Buy Now")
- Extracts the monetary value and currency if present
- Works with multiple LLM providers (Ollama, OpenAI, Anthropic)
- Easy-to-use Gradio web interface

## Requirements

- Python 3.11+
- Conda
- Ollama installed locally (default)
- OpenAI API key (optional)
- Anthropic API key (optional)

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd <repository-directory>
```

2. Create and activate the Conda environment:
```bash
conda env create -f environment.yml
conda activate value-llm
```

3. Set up environment variables by copying the template:
```bash
cp env.example .env
```

4. Edit the `.env` file to configure your LLM providers. By default, it uses Ollama with the llama3 model.

## Usage

1. Start the application:
```bash
python app.py
```

2. Open the web interface in your browser (usually at http://127.0.0.1:7860)

3. Input the following:
   - HTML content of the page
   - Text content of the clicked button
   - Select the LLM provider

4. Click "Analyze" to get the results

## Example Input

HTML:
```html
<div class="product-container">
  <h1>Premium Headphones</h1>
  <div class="price-container">
    <span class="price">$149.99</span>
    <span class="original-price">$199.99</span>
  </div>
  <button class="add-to-cart-btn">Add to Cart</button>
</div>
```

Button Text: `Add to Cart`

## Response Format

```json
{
  "isValueClick": true,
  "value": 149.99,
  "currency": "USD"
}
```

## Switching LLM Providers

The application supports three LLM providers:

1. **Ollama** (default, requires local installation)
2. **OpenAI** (requires API key)
3. **Anthropic** (requires API key)

To use OpenAI or Anthropic, uncomment and set the appropriate API keys in the `.env` file.

## License

MIT 