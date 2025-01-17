import json
from flask import request, abort, render_template
from flask_restful import Resource, reqparse
from sqlalchemy.sql import text
from app.support.utils import *
from app.support import constants
from app.support.db import db
from .models import GamesModel, PlayersModel, GamesToPlayersModel, StateType, MovesModel, MoveType

parser = reqparse.RequestParser()
parser.add_argument('start', type=int)
parser.add_argument('until', type=int)


class CreateNewGame(Resource):

    def post(self):
        data = request.get_json(force=True)

        if 'columns' in data and 'rows' in data and 'players' in data:
            game = GameCreator.create_game(data)
            game_primary_key = game[0]
            game_id = game[1]
            if game_primary_key:

                for player_name in data['players']:
                    if GameCreator.player_exists(player_name):
                        # Add to the games to players table
                        GameCreator.create_game_to_player(game_primary_key, GameCreator.get_player_id(player_name))
                    else:
                        # A new user to players table
                        player_primary_key = GameCreator.create_player(player_name)
                        # Then Add to the games to players table
                        GameCreator.create_game_to_player(game_primary_key, player_primary_key)
                return {"gameId": game_id}

            else:
                abort(400, constants.GAME_CREATION_ERROR)

        else:
            abort(400, constants.NO_REQUIRED_GAME_VALUES_ERROR)


class ReturnAllInProgressGames(Resource):
    def get(self):
        games = GamesModel.query.filter_by(state=StateType.INPROGRESS).all()
        games_response = []
        for game in games:
            games_response.append(game.name)
        return {"games": games_response}


class GetStateOfGame(Resource):
    def get(self, game_id):

        if game_id.isdigit():
            where_clause = "where g.id = :id"
        else:
            where_clause = ''
            abort(400, constants.NO_REQUIRED_GAME_STATE_VALUES_ERROR)

        query_text = """select p.name as name, g.state as state, g.winner as winner from games g
        JOIN games_to_players gs ON g.id = gs.game_id
        JOIN players p ON p.id = gs.player_id where g.id = :id""".format(whereClause=where_clause)

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


class GetListOfMovesPlayed(Resource):
    def get(self, game_id):
        args = parser.parse_args()
        start = args['start']
        until = args['until']

        if not game_id.isdigit():
            abort(400, constants.NO_REQUIRED_GAME_STATE_VALUES_ERROR)
        limits = ''

        if start and until:
            limits = "LIMIT {amount}".format(amount=abs(start - until))

        query_text = """select p.name as `player`, m.type, m.board_column as `column` from moves m
        JOIN players p ON p.id = m.player_id WHERE m.game_id = :id {limits}""".format(limits)
        query = text()

        data = db.engine.execute(query, id=game_id).fetchall()
        if not data:
            abort(404, constants.MOVE_NOT_FOUND_ERROR)

        moves_data = [dict(move) for move in db.engine.execute(query, id=game_id).fetchall()]

        return moves_data


class GetMovePlayed(Resource):
    def get(self, game_id, move_number):

        if not game_id.isdigit():
            abort(400, constants.NO_REQUIRED_GAME_STATE_VALUES_ERROR)

        query = text("""select p.name as `player`, m.type, m.board_column as `column` from moves m
        JOIN players p ON p.id = m.player_id WHERE m.game_id = :id and m.board_column = :movenumber""")

        data = db.engine.execute(query, id=game_id, movenumber=move_number).fetchone()
        if not data:
            abort(404, constants.MOVE_NOT_FOUND_ERROR)

        move_data = dict(data)

        return {"type": move_data['type'], "player": move_data['player'], "column": move_data['column']}


class PostAGameMove(Resource):

    def post(self, game_id, player_id):
        # TODO: Break-up this method it is too big
        data = request.get_json(force=True)

        # validate game_id
        if game_id.isdigit():
            if not GameCreator.game_exists(game_id):
                abort(404, constants.NO_GAME_FOUND)
        else:
            abort(400, constants.NO_REQUIRED_GAME_MOVE_ERROR)

        # validate player_id
        if not GameCreator.player_exists(player_id):  # can be primary key or just string player name
            abort(404, constants.NO_PLAYER_FOUND)

        if 'column' in data:

            # Get game board
            game = GameCreator.get_game(game_id)
            game_players = GameCreator.get_players(game_id)

            # Check if Game is already completed
            if game.state is StateType.DONE:
                abort(409, constants.GAME_DONE_ERROR)

            # Check if it's players turn.
            player_name = GameCreator.get_player_name(player_id)
            if player_name != game.active_turn:
                abort(409, constants.PLAYER_NOT_TURN_ERROR)

            # Set next player to play
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
                # find row / column indexes to place token on board
                for i in range(0, len(board_game)):
                    move = board_game[i][current_column]
                    current_row = i
                    if move != 0:
                        current_row = current_row - 1
                        break

                # Check for illegal moves
                if board_game[current_row][current_column] != 0:
                    abort(409, constants.CAN_NOT_MOVE_ERROR)

                board_game[current_row][current_column] = player_id

                # Check if player won after move
                if GameCreator.has_player_won(board_game, player_id):
                    game.state = StateType.DONE
                    next_player = ''
                    winner = player_name

                # Check for draw
                if not GameCreator.is_the_game_a_draw(board_game):
                    game.state = StateType.DONE
                    next_player = ''
                    winner = 'draw'

                # Update the games table
                game.update(game_id, {"state": game.state,
                                      "board": json.dumps(board_game),
                                      "active_turn": next_player,
                                      "winner": winner})

                # Insert move data in to move table
                GameCreator.create_game_move(game_id, player_id, current_column, current_row)

                return {"move": "{gameId}/moves/{move_number}".format(gameId=game_id, move_number=data['column'])}

            else:
                abort(400, constants.OUT_OF_BOUNDS_COLUMN_ERROR)

        else:
            abort(400, constants.NO_REQUIRED_GAME_MOVE_ERROR)


class PlayerQuitsGame(Resource):

    def delete(self, game_id, player_id):

        # validate game_id
        if game_id.isdigit():  # must be primary key or uuid
            if not GameCreator.game_exists(game_id):
                abort(404, constants.NO_GAME_FOUND)
        else:
            abort(400, constants.NO_REQUIRED_GAME_MOVE_ERROR)

        # validate player_id
        if not GameCreator.player_exists(player_id):
            abort(404, constants.NO_PLAYER_FOUND)

        game = GameCreator.get_game(game_id)
        # TODO: Put this in a method
        # check if the player_id can quit
        game_players = GameCreator.get_players(game_id)
        can_delete = False
        for player in game_players:
            if player['player_id'] == player_id:
                can_delete = True
                break
        if not can_delete:
            abort(400, constants.NO_REQUIRED_GAME_MOVE_ERROR)


        # TODO : Check if players is apart of this game to be able to quit

        # Check if Game is already completed
        if game.state is StateType.DONE:
            abort(410, constants.GAME_DONE_ERROR)

        # Update Game to DONE
        # Change this part to accommodate more than k = 2 players to a game
        # Right now since only 2 player, set game to gone, when one player quits.
        game.update(game_id, {"state": StateType.DONE,
                              "board": json.dumps(game.board),
                              "active_turn": "",
                              "winner": ""})

        # Add new move quit row.
        game_moves = MovesModel()
        game_moves.game_id = game_id
        game_moves.player_id = player_id
        game_moves.type = MoveType.QUIT
        game_moves.board_column = -1
        game_moves.board_row = -1
        game_moves.save()

        return {"status": "success"}, 202  # return a 202 reponse


class GameCreator:

    @staticmethod
    def create_game_to_player(game_id, player_id):
        model = GamesToPlayersModel()
        model.game_id = game_id
        model.player_id = player_id
        model.save()
        db.session.flush()
        return model.id

    @staticmethod
    def create_game(data):
        model = GamesModel()
        game_id = GameCreator.generate_unique_game_id()
        model.name = game_id
        model.columns = data['columns']
        model.rows = data['rows']
        model.board = json.dumps(generate_board(data['columns'], data['rows']))
        model.state = StateType.INPROGRESS
        model.winner = ''
        model.active_turn = data['players'][0]
        model.save()
        db.session.flush()
        return (model.id, game_id)

    @staticmethod
    def create_player(player):
        model = PlayersModel()
        model.name = player
        model.save()
        db.session.flush()
        return model.id

    @staticmethod
    def create_game_move(game_id, player_id, column, row):
        game_moves = MovesModel()
        game_moves.game_id = game_id
        game_moves.player_id = player_id
        game_moves.type = MoveType.MOVE
        game_moves.board_column = column + 1
        game_moves.board_row = row + 1
        game_moves.save()

    @staticmethod
    def generate_unique_game_id():
        # try 5 times to generate a unique game id
        # TODO : Revisit, may not need to do this uuid1, has strict uniqueness
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

    @staticmethod
    def get_player_id(player_name):
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
    def is_the_game_a_draw(board):
        is_draw = False
        for i in range(0, len(board)):
            row = board[i]
            if all_same_values(row, 0):  # if there are no more zero's on board. No more open places
                is_draw = True
                break
        return is_draw

    @staticmethod
    def has_player_won(board, player_id):
        has_won = False

        # Check columns
        for i in range(0, len(board)):
            column = get_column(board, i)
            if all_same_values(column, player_id):
                has_won = True
                break

        # Check rows
        for i in range(0, len(board)):
            row = board[i]
            if all_same_values(row, player_id):
                has_won = True
                break

        # Check diagonals (only checking top-left to bottom-right, and top-right to bottom-left)
        for diagnoal in get_diagonals(board):
            if all_same_values(diagnoal, player_id):
                has_won = True
                break

        return has_won



