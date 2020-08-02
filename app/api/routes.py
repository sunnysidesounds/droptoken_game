from flask import Blueprint
from flask_restful import Api

from .resources import Games, GameState, GameMove, GameMoves

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# GAME ENDPOINTS
api.add_resource(Games, '/', methods=['GET'], endpoint='games_get')
api.add_resource(Games, '/', methods=['POST'], endpoint='games_post')
api.add_resource(GameState, '/<game_id>', methods=['GET'], endpoint='game_state')
api.add_resource(GameMoves, '/<int:game_id>/moves', methods=['GET'], endpoint='game_moves_get')
api.add_resource(GameMoves, '/<int:game_id>/<int:player_id>', methods=['POST'], endpoint='game_moves_post')
api.add_resource(GameMove, '/<int:game_id>/moves/<int:move_number>', methods=['GET'], endpoint='game_move_get')
api.add_resource(GameMove, '/<int:game_id>/<int:player_id>', methods=['DELETE'], endpoint='game_move_delete')
