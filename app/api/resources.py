from flask import request
from flask_restful import Resource, reqparse
from app.support.utils import response_json
from app.support import constants
from app.support.db import db

parser = reqparse.RequestParser()
parser.add_argument('start', type=int)
parser.add_argument('until', type=int)


class Games(Resource):
    def get(self):
        return 'TODO'

    def post(self):
        return 'TODO'


class GameState(Resource):
    def get(self, game_id):
        return 'Game State {0}'.format(game_id)


class GameMoves(Resource):
    def get(self, game_id):
        return 'Game Moves {0}'.format(game_id)

    def post(self):
        return 'TODO'


class GameMove(Resource):
    def get(self, game_id):
        return 'Game Moves {0}'.format(game_id)

    def delete(self, game_id, player_id):
        return 'Game QUITS {0} {1}'.format(game_id, player_id)


# TODO : DO WE NEED MAY NEED TO REMOVE THIS CLASS
class QueryToResponseJSON:

    def __init__(self, query):
        self.query = query

    def get_one(self):
        data = dict(db.engine.execute(self.query).fetchone())
        if data:
            return response_json(True, data, None)
        else:
            return response_json(True, data, constants.NO_DATA)

    def get_all(self):
        data = db.engine.execute(self.query).fetchall()
        data = [dict(r) for r in data]
        if data:
            return response_json(True, data, None)
        else:
            return response_json(True, data, constants.NO_DATA)

    def exists(self):
        data = db.engine.execute(self.query).fetchone()
        return True if data else False
