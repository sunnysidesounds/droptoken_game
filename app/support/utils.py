import uuid


def get_uuid():
    return str(uuid.uuid1())


def generate_board(columns, rows):
    return [[0 for column in range(columns)] for row in range(rows)]


def response_json(success, data, message=None):
    return {
        "response": data,
        "success": success,
        "message": message,
    }