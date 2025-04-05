def get_diagram_urls(api_response: dict):
    """
    Retrieves the diagram URLs of VCell models from the API response.

    Args:
        api_response (dict): The response from the VCell API, contains a list of models.

    Returns:
        List[str]: A list of diagram URLs.
    """
    urls = []

    for model in api_response:
        biomodel_id = model.get("bmKey")
        if biomodel_id:
            diagram_url = f"https://vcell.cam.uchc.edu/api/v0/biomodel/{biomodel_id}/diagram"
            urls.append(diagram_url)
    return urls