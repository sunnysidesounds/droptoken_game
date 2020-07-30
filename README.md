# DROP TOKEN GAME SERVICE

### Rules:
- takes place on a 4x4 grid
- token is dropped along one of the columns
- token goes to the lowest unoccupied row of the board
- player wins when they have 4 tokens next to each other either along a row, column, or diagonal
- If the board is filled, and nobody has won then the game is a draw
- Each player takes a turn, starting with player 1, until the game reaches either win or draw.
- player tries to put a token in a column that is already full, returns error state, and the player must play again until valid move.

