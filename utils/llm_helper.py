from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

llm_client = None


def get_llm_client():
    """
    This function initializes and returns a Groq client instance.
    It checks if the client is already initialized to avoid creating multiple instances unnecessarily.

    Returns:
        Groq: An instance of the Groq client.
    """
    global llm_client
    if llm_client is None:
        llm_client = Groq(api_key=os.environ["LLM_API_KEY"])
    return llm_client


def get_llm_response(prompt: str):
    """
    This function generates a response from the LLM based on the provided prompt.

    Args:
        prompt (str): The prompt to send to the LLM.

    Returns:
        dict: The response from the LLM.
    """
    try:
        client = get_llm_client()
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are an AI assistant helping users explore VCell BioModels."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.4
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"