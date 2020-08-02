import json
from flask import request, abort
from flask_restful import Resource, reqparse
from sqlalchemy.sql import text
from app.support.utils import *
from app.support import constants
from app.support.db import db
from .models import GamesModel, PlayersModel, GamesToPlayersModel, StateType, MovesModel, MoveType

parser = reqparse.RequestParser()
parser.add_argument('start', type=int)
parser.add_argument('until', type=int)


class Games(Resource):
    def get(self):
        games = GamesModel.query.filter_by(state=StateType.INPROGRESS).all()
        games_response = []
        for game in games:
            games_response.append(game.name)
        return {"games": games_response}

    def post(self):
        data = request.get_json(force=True)

        # TODO: Look at more validation, model level

        if 'columns' in data and 'rows' in data and 'players' in data:
            game = self.create_game(data)
            game_primary_key = game[0]
            game_id = game[1]
            if game_primary_key:

                for player_name in data['players']:
                    if Games.player_exists(player_name):
                        # Add to the games to players table
                        self.create_game_to_player(game_primary_key, self.get_player_id(player_name))
                    else:
                        # A new user to players table
                        player_primary_key = self.create_player(player_name)
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
        model.winner = ''
        model.active_turn = data['players'][0] #set first player in list to active user
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

    @staticmethod
    def player_exists(player_name):
        # Check for name and id
        player = PlayersModel.query.filter_by(name=player_name).first()
        if player:
            return True
        else:
            player = PlayersModel.query.filter_by(id=player_name).first()
            if player:
                return True
        return False

    @staticmethod
    def game_exists(game_id):
        # Check for name and id
        game = GamesModel.query.filter_by(name=game_id).first()
        if game:
            return True
        else:
            game = GamesModel.query.filter_by(id=game_id).first()
            if game:
                return True
        return False

    def get_player_id(self, player_name):
        player = PlayersModel.query.filter_by(name=player_name).first()
        return player.id

    @staticmethod
    def get_player_name(player_id):
        player = PlayersModel.query.filter_by(id=player_id).first()
        return player.name

    @staticmethod
    def get_game(game_id):
        # Check for name and id
        game = GamesModel.query.filter_by(name=game_id).first()
        if game:
            return game
        else:
            game = GamesModel.query.filter_by(id=game_id).first()
            if game:
                return game
        return None

    @staticmethod
    def get_players(game_id):
        query = text("""select p.name as player_name, p.id as player_id from games g
        JOIN games_to_players gs ON g.id = gs.game_id
        JOIN players p ON p.id = gs.player_id WHERE g.id = :id""")
        return [dict(player) for player in db.engine.execute(query, id=game_id).fetchall()]

    @staticmethod
    def has_player_won(board):
        has_won = False

        # Check columns
        for i in range(0, len(board)):
            column = get_column(board, i)
            if all_same_values(column):
                has_won = True
                break

        # Check rows
        for i in range(0, len(board)):
            row = board[i]
            if all_same_values(row):
                has_won = True
                break

        # Check diagonals
        for diagnoal in get_diagonals(board):
            if all_same_values(diagnoal):
                has_won = True
                break

        return has_won


class GameState(Resource):
    def get(self, game_id):

        # Able to pass in game name (uuid) or primary key
        if game_id.isdigit():
            where_clause = "where g.id = :id"
        elif validate_uuid(game_id):
            where_clause = "where g.name = :id"
        else:
            where_clause = ''
            abort(400, constants.NO_REQUIRED_GAME_STATE_VALUES_ERROR)


        query_text = """select p.name as name, g.state as state, g.winner as winner from games g
        JOIN games_to_players gs ON g.id = gs.game_id
        JOIN players p ON p.id = gs.player_id {whereClause}""".format(whereClause=where_clause)

        query = text(query_text)
        player_states = [dict(player) for player in db.engine.execute(query, id=game_id).fetchall()]

        if len(player_states) == 0:
            abort(404, constants.NO_GAME_FOUND)

        player_names = []
        winners = None

        for state in player_states:
            player_names.append(state['name'])
            if not state['winner']:
                winners = state['winner']

        game_state = player_states[0]['state']
        results = {"players": player_names, 'state': game_state}

        if game_state == StateType.DONE:
            if winners == 'draw':
                results['winner'] = 'null'
            else:
                results['winner'] = winners

        return results


class GameMoves(Resource):
    def get(self, game_id):
        return 'Game Moves {0}'.format(game_id)


class GameMove(Resource):
    def get(self, game_id):
        return 'Game Moves {0}'.format(game_id)

    def post(self, game_id, player_id):
        data = request.get_json(force=True)

        # validate game_id
        if game_id.isdigit() or validate_uuid(game_id):  # must be primary key or uuid
            if not Games.game_exists(game_id):
                abort(404, constants.NO_GAME_FOUND)
        else:
            abort(400, constants.NO_REQUIRED_GAME_MOVE_ERROR)

        # validate player_id
        if not Games.player_exists(player_id):  # can be primary key or just string player name
            abort(404, constants.NO_PLAYER_FOUND)

        #TODO Check state of game

        if 'column' in data:

            # Get game board
            game = Games.get_game(game_id)
            game_players = Games.get_players(game_id)

            # Check if it's players turn.
            player_name = Games.get_player_name(player_id)
            if player_name != game.active_turn:
                abort(409, constants.PLAYER_NOT_TURN_ERROR)

            next_player = None
            winner = ''
            for player in game_players:
                if player['player_name'] != game.active_turn:
                    next_player = player['player_name']

            game_column = game.columns - 1
            current_column = data['column'] - 1

            if current_column <= game_column:
                board_game = json.loads(game.board)
                current_row = 0

                for i in range(0, len(board_game)):
                    move = board_game[i][current_column]
                    current_row = i
                    if move != 0:
                        current_row = current_row - 1
                        break

                # TODO : Check for illegal moves

                board_game[current_row][current_column] = player_id

                if Games.has_player_won(board_game):
                    game.state = StateType.DONE
                    next_player = ''
                    winner = player_name

                game.update(game_id, {"state": game.state,
                                      "board": json.dumps(board_game),
                                      "active_turn": next_player,
                                      "winner": winner})

                # Insert move data in to move table
                game_moves = MovesModel()
                game_moves.game_id = game_id
                game_moves.player_id = player_id
                game_moves.type = MoveType.MOVE
                game_moves.board_column = current_column
                game_moves.board_row = current_row
                game_moves.save()

                return {"move": "{gameId}/moves/{move_number}".format(gameId=game_id, move_number=data['column'])}

            else:
                abort(400, constants.OUT_OF_BOUNDS_COLUMN_ERROR)

        else:
            abort(400, constants.NO_REQUIRED_GAME_MOVE_ERROR)




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
