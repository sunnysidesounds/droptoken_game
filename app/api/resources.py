import json
from flask import request, abort
from flask_restful import Resource, reqparse
from app.support.utils import *
from app.support import constants
from app.support.db import db
from .models import GamesModel, PlayersModel, GamesToPlayersModel, StateType

parser = reqparse.RequestParser()
parser.add_argument('start', type=int)
parser.add_argument('until', type=int)


class Games(Resource):
    def get(self):
        return 'TODO'

    def post(self):
        data = request.get_json(force=True)

        if 'columns' in data and 'rows' in data and 'players' in data:
            game = self.create_game(data)
            game_primary_key = game[0]
            game_id = game[1]
            if game_primary_key:

                for player in data['players']:
                    if self.player_exists(player):
                        # Add to the games to players table
                        self.create_game_to_player(game_primary_key, player)
                    else:
                        # A new user to players table
                        player_primary_key = self.create_player(player)
                        # Then Add to the games to players table
                        self.create_game_to_player(game_primary_key, player_primary_key)
                return {"gameId": game_id}

            else:
                abort(400, constants.GAME_CREATION_ERROR)

        else:
            abort(400, constants.NO_REQUIRED_GAME_VALUES_ERROR)

    def create_game_to_player(self, game_id, player_id):
        model = GamesToPlayersModel()
        model.game_id = game_id
        model.player_id = player_id
        model.save()

        db.session.flush()
        return model.id

    def create_game(self, data):
        model = GamesModel()
        game_id = self.generate_unique_game_id()
        model.name = game_id
        model.columns = data['columns']
        model.rows = data['rows']
        model.board = json.dumps(generate_board(data['columns'], data['rows']))
        model.state = StateType.INPROGRESS
        model.winner_id = 0
        model.save()

        db.session.flush()
        return (model.id, game_id)

    def create_player(self, player):
        model = PlayersModel()
        model.name = player
        model.save()
        db.session.flush()
        return model.id



    def generate_unique_game_id(self):
        # try 5 times to generate a unique game id
        # TODO : Revisit, may not need this to be unique as we have primary keys
        for i in range(0, 5):
            game_id = get_uuid()
            game_id_exist = GamesModel.query.filter_by(id=game_id).first()
            if not game_id_exist:
                return game_id
        return None

    def player_exists(self, player_id):
        player_id = PlayersModel.query.filter_by(id=player_id).first()
        if player_id:
            return True
        return False













        #games_model.save()


        print(data)
        return 'TODO'



"""
    def post(self):
        args = parser.parse_args()
        user_id = args['id']
        data = request.get_json(force=True)
        if user_id:
            query = PROJECT_QUERY + "WHERE id = {userId}".format(userId=user_id)
            user_json = QueryToResponseJSON(query).get_one()['response']
            user_model = UserModel()
            user_model.update(user_id, {"username": data['username'] if 'username' in data else user_json['username'],
                                        "first_name": data['first_name'] if 'first_name' in data else user_json['first_name'],
                                        "last_name": data['last_name'] if 'last_name' in data else user_json['last_name'],
                                        "email": data['email'] if 'email' in data else user_json['email']})

            return response_json(True, data, None)
        else:
            if "username" not in data:
                return response_json(True, data, constants.NO_USERNAME)
            if "first_name" not in data:
                return response_json(True, data, constants.NO_FIRST_NAME)
            if "last_name" not in data:
                return response_json(True, data, constants.NO_LAST_NAME)
            if "email" not in data:
                return response_json(True, data, constants.NO_EMAIL)

            if not self.is_username_exist(data['username']):
                user_model = UserModel(
                    username=data['username'],
                    first_name=data['first_name'],
                    last_name=data['last_name'],
                    email=data['email'],
                )
                user_model.save()
                return response_json(True, data, None)
            else:
                return response_json(True, data, constants.NO_USERNAME)

"""





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
