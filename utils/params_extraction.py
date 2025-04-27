import json
from vcelldb.params_model import QueryParams
from groq import Groq
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

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


def get_path_params(user_prompt: str, settings: dict):
    """
    This function extracts the path parameters from the user prompt.

    Args:
        user_prompt (str): A Natural Language prompt from the user that will be used to extract path parameters.

    Returns:
        dict: A dictionary containing the extracted path parameters.
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
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt},
                ],
                response_format={"type": "json_object"},
            )
            content = QueryParams.model_validate_json(response.choices[0].message.content)
            params = content.model_dump(exclude_none=True)
            return params
        except Exception as e:
            return {"error": f"Failed to extract parameters: {str(e)}"}
        
    elif provider == "ollama":
        model_name = settings.get("model", "llama3.2:1b")
        client = OpenAI(base_url = 'http://localhost:11434/v1', api_key='ollama')
        try:
            response = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt},
                ],
                response_format=QueryParams,
            )
            return response.choices[0].message.parsed
        except Exception as e:
            return f"Error (Ollama): {str(e)}"
    else:
        return "Error: Unknown provider"   
