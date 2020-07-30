# DROPTOKEN PROJECT GUIDLINES

### Rules:
- takes place on a 4x4 grid
- token is dropped along one of the columns
- token goes to the lowest unoccupied row of the board
- player wins when they have 4 tokens next to each other either along a row, column, or diagonal
- If the board is filled, and nobody has won then the game is a draw
- Each player takes a turn, starting with player 1, until the game reaches either win or draw.
- player tries to put a token in a column that is already full, returns error state, and the player must play again until valid move.


### Requirements

- [ ] Each game is between k = 2 individuals, basic board size is 4x4 (number of columns x number of rows)
- [ ] A player can quit a game at every moment while the game is still in progress. The game will continue as long as there are 2 or more active players and the game is not done. In case only a single player is left, that player is considered the winner.
- [ ] The backend should validate that a move move is valid (it's the player's turn, column is not already full)
- [ ] The backend should identify a winning state.
- [ ] Multiple games may be running at the same time.

### API Requirements

- [ ] GET /drop_token - Return all in-progress games.
- [ ] POST /drop_token - Create a new game.
- [ ] GET /drop_token/{gameId} - Get the state of the game.
- [ ] GET /drop_token/{gameId}/moves- Get (sub) list of the moves played.
    - [ ] Optional Query parameters: GET /drop_token/{gameId}/moves?start=0&until=1.
- [ ] POST /drop_token/{gameId}/{playerId} - Post a move.
- [ ] GET /drop_token/{gameId}/moves/{move_number} - Return the move.
- [ ] DELETE /drop_token/{gameId}/{playerId} - Player quits from game.


