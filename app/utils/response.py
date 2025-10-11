def json_response(success, message="", data=None, error=None, details=None, status_code=200):
    """
    Standardized JSON response format for API.

    Args:
        success (bool): Operation success status
        message (str): Human-readable message
        data (dict or list, optional): Returned data payload if success
        error (str, optional): Error message if failure
        details (list, optional): List of detailed error strings
        status_code (int): HTTP status code

    Returns:
        tuple: (response dict, HTTP status code)
    """
    response = {
        "success": success,
        "message": message
    }
    if success:
        if data is not None:
            response["data"] = data
    else:
        response["error"] = error or "An error occurred"
        if details:
            response["details"] = details
    return response, status_code
