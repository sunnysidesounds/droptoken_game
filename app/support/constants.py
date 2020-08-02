# ------------ General Constants -----------------
APP_NAME = "Drop-Token Game"
APP_FAILURE = "{appName} failed to startup".format(appName=APP_NAME)
NO_DATA = "No data for this request"

# Error Messages
NO_REQUIRED_GAME_VALUES_ERROR = 'Malformed request: Requires `columns`, `rows` and `players` values in request'
GAME_CREATION_ERROR = 'Game could not be created!'
NO_REQUIRED_GAME_STATE_VALUES_ERROR = 'Malformed request: Requires integer based game_id or string based uuid'
NO_GAME_FOUND = 'Game could not be found'
NO_PLAYER_FOUND = 'Player could not be foung'
NO_REQUIRED_GAME_MOVE_ERROR = 'Malformed request: Requires integer based column number'