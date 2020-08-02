from flask import Blueprint
from flask_restful import Api

from .resources import ReturnAllInProgressGames, GetStateOfGame, PostAGameMove, GetListOfMovesPlayed, GetMovePlayed, \
    CreateNewGame, PlayerQuitsGame

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# GAME ENDPOINTS
api.add_resource(ReturnAllInProgressGames, '', methods=['GET'], endpoint='return_all_inprogress_games')
api.add_resource(CreateNewGame, '', methods=['POST'], endpoint='create_new_game')
api.add_resource(GetStateOfGame, '/<game_id>', methods=['GET'], endpoint='get_state_of_game')
api.add_resource(GetListOfMovesPlayed, '/<game_id>/moves', methods=['GET'], endpoint='get_list_of_moves_played')
api.add_resource(PostAGameMove, '/<game_id>/<player_id>', methods=['POST'], endpoint='post_a_game_move')
api.add_resource(GetMovePlayed, '/<game_id>/moves/<int:move_number>', methods=['GET'], endpoint='get_move_played')
api.add_resource(PlayerQuitsGame, '/<game_id>/<player_id>', methods=['DELETE'], endpoint='player_quits_game')
