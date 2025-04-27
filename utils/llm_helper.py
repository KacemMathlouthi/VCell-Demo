from groq import Groq
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

llm_client = None

# LLM Agnostic Code
def get_llm_response(prompt: str, settings: dict):
    """
    This function generates a response from the LLM based on the provided prompt.

    Args:
        prompt (str): The prompt to send to the LLM.
        settings (dict): contains the llm provider to use (groq/ollama) and the config.
    Returns:
        dict: The response from the LLM.
    """
    provider = settings.get("provider", "groq")

    if provider == "groq":
        api_key = settings.get("api_key", os.getenv("LLM_API_KEY"))
        model_name = settings.get("model", "llama-3.3-70b-versatile")
        client = Groq(api_key=api_key)

        try:
            response = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": "You are an AI assistant helping users explore VCell BioModels."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.4,
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error (Groq): {str(e)}"
    
    elif provider == "ollama":
        model_name = settings.get("model", "llama3.2:1b")
        client = OpenAI(base_url = 'http://localhost:11434/v1', api_key='ollama')
        try:
            response = client.chat.completions.create(
            model="llama2",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Who won the world series in 2020?"},
                {"role": "assistant", "content": "The LA Dodgers won in 2020."},
                {"role": "user", "content": "Where was it played?"}
            ]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error (Ollama): {str(e)}"
    else:
        return "Error: Unknown provider"    
