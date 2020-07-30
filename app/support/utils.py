def response_json(success, data, message=None):
    return {
        "response": data,
        "success": success,
        "message": message,
    }