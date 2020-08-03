# DROP TOKEN GAME SERVICE

### Rules:
- takes place on a 4x4 grid
- token is dropped along one of the columns
- token goes to the lowest unoccupied row of the board
- player wins when they have 4 tokens next to each other either along a row, column, or diagonal
- If the board is filled, and nobody has won then the game is a draw
- Each player takes a turn, starting with player 1, until the game reaches either win or draw.
- player tries to put a token in a column that is already full, returns error state, and the player must play again until valid move.


### Technical Details
- Flask Python Web Service: https://flask.palletsprojects.com/en/1.1.x/
- MYSQL 8.0.19
- Python 3.8


### Database Schemas

***Games Table***
```
CREATE TABLE `games` (
     `id` int unsigned NOT NULL AUTO_INCREMENT,
     `name` varchar(255) DEFAULT NULL,
     `columns` int unsigned NOT NULL DEFAULT '0',
     `rows` int unsigned NOT NULL DEFAULT '0',
     `board` json DEFAULT NULL,
     `state` enum('DONE','INPROGRESS') NOT NULL,
     `active_turn` varchar(255) DEFAULT NULL,
     `winner` varchar(255) DEFAULT NULL,
     `last_updated` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
     PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
```

***Players Table***
```
CREATE TABLE `players` (
       `id` int unsigned NOT NULL AUTO_INCREMENT,
       `name` varchar(255) DEFAULT NULL,
       `last_updated` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
       PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
```

*** Games To Players Table***
```
CREATE TABLE `games_to_players` (
       `id` int unsigned NOT NULL AUTO_INCREMENT,
       `game_id` int unsigned NOT NULL,
       `player_id` int unsigned NOT NULL,
       `last_updated` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
       PRIMARY KEY (`id`),
       KEY `game_id_constraint_2` (`game_id`),
       KEY `player_id_constraint_2` (`player_id`),
       CONSTRAINT `game_id_constraint_2` FOREIGN KEY (`game_id`) REFERENCES `games` (`id`),
       CONSTRAINT `player_id_constraint_2` FOREIGN KEY (`player_id`) REFERENCES `players` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
```

*** Moves Tables***
```
CREATE TABLE `moves` (
       `id` int unsigned NOT NULL AUTO_INCREMENT,
       `game_id` int unsigned NOT NULL,
       `player_id` int unsigned NOT NULL,
       `type` enum('MOVE','QUIT') NOT NULL,
       `board_column` int NOT NULL,
       `board_row` int NOT NULL,
       `last_updated` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
       PRIMARY KEY (`id`),
       KEY `game_id_constraint_1` (`game_id`),
       KEY `player_id_constraint_1` (`player_id`),
       CONSTRAINT `game_id_constraint_1` FOREIGN KEY (`game_id`) REFERENCES `games` (`id`),
       CONSTRAINT `player_id_constraint_1` FOREIGN KEY (`player_id`) REFERENCES `players` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
```