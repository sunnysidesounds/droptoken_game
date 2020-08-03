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


def get_column(matrix, i):
    return [row[i] for row in matrix]


def get_diagonals(matrix):
    top_left_to_bottom_right = [row[i] for i, row in enumerate(matrix)]
    top_right_to_bottom_left = [row[-i-1] for i, row in enumerate(matrix)]
    return [top_left_to_bottom_right, top_right_to_bottom_left]


def all_same_values(items, match_item):
    return all(x == match_item for x in items)


def generate_board(columns, rows):
    return [[0 for column in range(columns)] for row in range(rows)]