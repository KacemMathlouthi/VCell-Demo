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
