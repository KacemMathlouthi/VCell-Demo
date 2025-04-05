from groq import Groq
import os
import json
from vcelldb.params_model import QueryParams
from dotenv import load_dotenv

load_dotenv()

llm_client = None 

SYSTEM_PROMPT = f"""
You are an assistant for a VCell BioModel explorer that responds only in JSON.
Your job is to extract structured API parameters from user questions about VCell models.

Only return the following keys if relevant:
- bmName
- bmId
- category (one of: all, public, shared, tutorials, educational)
- owner
- savedLow (format: YYYY-MM-DD)
- savedHigh (format: YYYY-MM-DD)
- startRow (int)
- maxRows (int)
- orderBy (one of: date_desc, date_asc, name_desc, name_asc)

Here is the JSON Schema for the parameters:
The JSON object must follow this schema:\n{json.dumps(QueryParams.model_json_schema(), indent=2)}

Respond only with a JSON object. Do not explain anything else.
"""

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


def get_path_params(user_prompt: str):
    """
    This function extracts the path parameters from the user prompt.

    Args:
        user_prompt (str): A Natural Language prompt from the user that will be used to extract path parameters.

    Returns:
        dict: A dictionary containing the extracted path parameters.
    """
    client = get_llm_client()

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system", 
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
                
            ],
            response_format={"type": "json_object"},
        )
        content = QueryParams.model_validate_json(response.choices[0].message.content)
        params = content.model_dump(exclude_none=True)
        return params
    except Exception as e:
        return {"error": f"Failed to extract parameters: {str(e)}"}