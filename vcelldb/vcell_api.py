import requests

# VCell API URL
BASE_URL = "https://vcell.cam.uchc.edu/api/v0/biomodel"

# Allowed query parameters
ALLOWED_PARAMS = {
    "bmName", "bmId", "category", "owner", 
    "savedLow", "savedHigh", 
    "startRow", "maxRows", "orderBy"
}

# Valid values for Categories and OrderBy
VALID_CATEGORIES = {"all", "public", "shared", "tutorials", "educational"}
VALID_ORDER_BY = {"date_desc", "date_asc", "name_desc", "name_asc"}

def query_vcell_models(params: dict):
    """
    Query the VCell BioModel API with dynamic GET parameters.

    Args:
        params (dict): A dictionary of query parameters.
        Currently supported parameters include:
            - bmName (str): BioModel Name.
            - bmId (str): BioModel ID.
            - category (str): Category of the BioModel. can be 'all', 'public', 'shared', 'tutorials', or 'educational'.
            - owner (str): Owner of the BioModel.
            - savedLow (str): Start date for the query in YYYY-MM-DD format. 
            - savedHigh (str): End date for the query in YYYY-MM-DD format.
            - startRow (int): The starting row for pagination.
            - maxRows (int): The maximum number of rows to return.
            - orderBy (str): The column to order the results by. Can be 'date_desc', 'date_asc', 'name_desc', 'name_asc'.
    Returns:
        dict: JSON response from the VCell API or error message.
    """
    clean_params = {k: v for k, v in params.items() if k in ALLOWED_PARAMS}

    if "category" in clean_params and clean_params["category"] not in VALID_CATEGORIES:
        clean_params.pop("category")

    if "orderBy" in clean_params and clean_params["orderBy"] not in VALID_ORDER_BY:
        clean_params.pop("orderBy")

    try:
        response = requests.get(BASE_URL, params=clean_params, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": f"API request failed: {str(e)}"}