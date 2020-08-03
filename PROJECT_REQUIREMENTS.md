# DROPTOKEN PROJECT REQUIREMENTS

### Needed Minimum Requirements

- [X] Each game is between k = 2 individuals, basic board size is 4x4 (number of columns x number of rows)
- [X] A player can quit a game at every moment while the game is still in progress. The game will continue as long as there are 2 or more active players and the game is not done. In case only a single player is left, that player is considered the winner.
- [X] The backend should validate that a move move is valid (it's the player's turn, column is not already full)
- [X] The backend should identify a winning state.
- [X] Multiple games may be running at the same time.

### API Requirements

- [X] GET /drop_token - Return all in-progress games.
- [X] POST /drop_token - Create a new game.
- [X] GET /drop_token/{gameId} - Get the state of the game.
- [X] GET /drop_token/{gameId}/moves- Get (sub) list of the moves played.
    - [ ] Optional Query parameters: GET /drop_token/{gameId}/moves?start=0&until=1.
- [X] POST /drop_token/{gameId}/{playerId} - Post a move.
- [X] GET /drop_token/{gameId}/moves/{move_number} - Return the move.
- [X] DELETE /drop_token/{gameId}/{playerId} - Player quits from game.


