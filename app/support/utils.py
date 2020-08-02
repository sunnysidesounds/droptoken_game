import uuid
from uuid import UUID


def get_uuid():
    return str(uuid.uuid1())


def validate_uuid(uuid):
    try:
        val = UUID(uuid, version=1)
    except ValueError:
        return False
    return True


def generate_board(columns, rows):
    return [[0 for column in range(columns)] for row in range(rows)]


def response_json(success, data, message=None):
    return {
        "response": data,
        "success": success,
        "message": message,
    }