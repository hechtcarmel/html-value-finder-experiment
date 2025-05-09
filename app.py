import os
import gradio as gr
import asyncio
from dotenv import load_dotenv
from typing import Dict, List, Any, Optional, Tuple
import json

from models import OllamaModel, OpenAIModel, AnthropicModel, ModelResponse
from utils.html_parser import clean_html

# Load environment variables
load_dotenv()

# Initialize models
ollama_model = OllamaModel(model_name=os.getenv("OLLAMA_MODEL", "llama3.2"))

# Initialize OpenAI and Anthropic models if API keys are provided
openai_model = None
anthropic_model = None

if os.getenv("OPENAI_API_KEY"):
    openai_model = OpenAIModel(
        api_key=os.getenv("OPENAI_API_KEY"),
        model_name=os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    )

if os.getenv("ANTHROPIC_API_KEY"):
    anthropic_model = AnthropicModel(
        api_key=os.getenv("ANTHROPIC_API_KEY"),
        model_name=os.getenv("ANTHROPIC_MODEL", "claude-3-opus-20240229")
    )

async def process_click(
    html: str, 
    button_text: str,
    model_choice: str,
    ultra_compact: bool
) -> Tuple[Dict[str, Any], str, str, Optional[str]]:
    """Process click data and determine monetary value."""
    
    # Clean HTML to reduce tokens
    cleaned_html, original_size, new_size = clean_html(html, button_text, ultra_compact)
    
    # Create size reduction message
    reduction_percent = ((original_size - new_size) / original_size) * 100 if original_size > 0 else 0
    size_info = f"Original: {original_size:,} chars | Cleaned: {new_size:,} chars | Reduced by: {reduction_percent:.1f}%"
    
    # Select model based on user choice
    if model_choice == "Ollama":
        model = ollama_model
    elif model_choice == "OpenAI" and openai_model:
        model = openai_model
    elif model_choice == "Anthropic" and anthropic_model:
        model = anthropic_model
    else:
        return {"error": "Selected model is not available. Please check API keys or select Ollama."}, cleaned_html, size_info, None
    
    # Process with the selected model using cleaned HTML
    result = await model.evaluate_click(cleaned_html, button_text)
    
    # Return the raw response as well
    return result.to_dict(), cleaned_html, size_info, result.raw_response

# Set up Gradio interface
with gr.Blocks(title="Click Value Analyzer") as app:
    gr.Markdown("# Click Value Analyzer")
    gr.Markdown("Determine the monetary value of clicked buttons in web pages.")
    
    with gr.Row():
        with gr.Column():
            html_input = gr.Textbox(
                label="HTML Content",
                placeholder="Paste HTML content here...",
                lines=10
            )
            
            button_text_input = gr.Textbox(
                label="Button Text",
                placeholder="e.g., Add to Cart"
            )
            
            with gr.Row():
                # Available models dropdown
                available_models = ["Ollama"]
                if openai_model:
                    available_models.append("OpenAI")
                if anthropic_model:
                    available_models.append("Anthropic")
                    
                model_choice = gr.Dropdown(
                    label="Select Model",
                    choices=available_models,
                    value=available_models[0]
                )
                
                ultra_compact_checkbox = gr.Checkbox(
                    label="Ultra-Compact HTML", 
                    value=True,
                    info="Minimize whitespace and newlines to reduce tokens"
                )
            
            analyze_button = gr.Button("Analyze Click Value")
        
        with gr.Column():
            json_output = gr.JSON(label="Analysis Result")
            
            raw_response_output = gr.Textbox(
                label="Raw LLM Response",
                placeholder="The raw response from the LLM will appear here...",
                lines=8
            )
            
            size_info_output = gr.Textbox(
                label="HTML Size Reduction",
                placeholder="Size reduction info will appear here...",
                interactive=False
            )
            
            gr.Markdown("""
            ### Result Format
            - **value**: The monetary value (if detected with high confidence) or null
            - **currency**: The currency code (if detected with high confidence) or null
            """)
    
    with gr.Row():
        processed_html_output = gr.Textbox(
            label="Processed HTML",
            placeholder="The processed HTML will appear here...",
            lines=10,
            interactive=False
        )
    
    analyze_button.click(
        fn=lambda html, text, model, compact: asyncio.run(process_click(html, text, model, compact)),
        inputs=[html_input, button_text_input, model_choice, ultra_compact_checkbox],
        outputs=[json_output, processed_html_output, size_info_output, raw_response_output]
    )

if __name__ == "__main__":
    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        # Set very high queue timeout to prevent timing out on long-running requests
        max_threads=10,
        share=False,
        quiet=False,
        show_api=True,
        root_path=None,
        ssl_verify=True
    ) 