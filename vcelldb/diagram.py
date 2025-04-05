def get_bmkeys(api_response: dict):
    """
    Retrieves the BioModel keys from the API response.

    Args:
        api_response (dict): The response from the VCell API, contains a list of models.

    Returns:
        List[str]: A list of BioModel keys.
    """
    bmkeys = []

    for model in api_response:
        biomodel_id = model.get("bmKey")
        if biomodel_id:
            bmkeys.append(biomodel_id)
    return bmkeys


def get_diagram_urls(api_response: dict):
    """
    Retrieves the diagram URLs of VCell models from the API response.

    Args:
        api_response (dict): The response from the VCell API, contains a list of models.

    Returns:
        List[str]: A list of diagram URLs.
    """
    urls = []
    bmkeys = get_bmkeys(api_response)
    if not bmkeys:
        return urls

    for bmkey in bmkeys:
        if bmkey:
            diagram_url = f"https://vcell.cam.uchc.edu/api/v0/biomodel/{bmkey}/diagram"
            urls.append(diagram_url)
    return urls