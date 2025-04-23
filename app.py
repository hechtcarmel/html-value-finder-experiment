import os
import gradio as gr
import asyncio
from dotenv import load_dotenv
from typing import Dict, List, Any, Optional
import json

from models import OllamaModel, OpenAIModel, AnthropicModel, ModelResponse

# Load environment variables
load_dotenv()

# Initialize models
ollama_model = OllamaModel(model_name=os.getenv("OLLAMA_MODEL", "llama3"))

# Initialize OpenAI and Anthropic models if API keys are provided
openai_model = None
anthropic_model = None

if os.getenv("OPENAI_API_KEY"):
    openai_model = OpenAIModel(
        api_key=os.getenv("OPENAI_API_KEY"),
        model_name=os.getenv("OPENAI_MODEL", "gpt-4o")
    )

if os.getenv("ANTHROPIC_API_KEY"):
    anthropic_model = AnthropicModel(
        api_key=os.getenv("ANTHROPIC_API_KEY"),
        model_name=os.getenv("ANTHROPIC_MODEL", "claude-3-opus-20240229")
    )

async def process_click(
    html: str, 
    button_text: str,
    model_choice: str
) -> Dict[str, Any]:
    """Process click data and return value assessment."""
    
    # Select model based on user choice
    if model_choice == "Ollama":
        model = ollama_model
    elif model_choice == "OpenAI" and openai_model:
        model = openai_model
    elif model_choice == "Anthropic" and anthropic_model:
        model = anthropic_model
    else:
        return {"error": "Selected model is not available. Please check API keys or select Ollama."}
    
    # Process with the selected model
    result = await model.evaluate_click(html, button_text)
    
    return result.to_dict()

# Set up Gradio interface
with gr.Blocks(title="Click Value Analyzer") as app:
    gr.Markdown("# Click Value Analyzer")
    gr.Markdown("Analyze if a button click has monetary value and determine the amount.")
    
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
            
            analyze_button = gr.Button("Analyze Click")
        
        with gr.Column():
            json_output = gr.JSON(label="Analysis Result")
    
    analyze_button.click(
        fn=lambda html, text, model: asyncio.run(process_click(html, text, model)),
        inputs=[html_input, button_text_input, model_choice],
        outputs=json_output
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
    ) 