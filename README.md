# DROP TOKEN GAME SERVICE
***98point6 Drop-Token: At-home interview question for BE engineers***

## Task:
We would like you to implement a backend (REST web-service) that allows playing the game of 9dt,
or 98point6 drop token. This should allow the players to create games, post moves, query moves
and get state of games.


## Rules:
- takes place on a 4x4 grid
- token is dropped along one of the columns
- token goes to the lowest unoccupied row of the board
- player wins when they have 4 tokens next to each other either along a row, column, or diagonal
- If the board is filled, and nobody has won then the game is a draw
- Each player takes a turn, starting with player 1, until the game reaches either win or draw.
- player tries to put a token in a column that is already full, returns error state, and the player must play again until valid move.


## Technical Details
- Flask Python Web Service: https://flask.palletsprojects.com/en/1.1.x/
- MYSQL 8.0.19
- Python 3.8

## Setup
To setup this service, please follow these steps.

### Setup with Docker

***Prerequisites***
- Docker 2.2.0.5

1. Download and install Docker Desktop: https://www.docker.com/products/docker-desktop
2. Pull down from git or unzip the droptoken_game/ service source code.
3. Get to the root directory of the service `cd /path-to-project/droptoken_game/`
4. Build the service: `docker-compose build --no-cache`
5. Launch the service and db containers: `docker-compose up`
6. Once up and running visit any of the endpoint urls in the ***ENDPOINTS*** section.


### Setup Locally

***Prerequisites***
- MYSQL 8.0.19
- Python 3.8
- pip / easy_install

1. Install virtualenv using `pip install virtualenv`
2. Pull down from git or unzip the droptoken_game/ service source code.
3. Get to the root directory of the service `cd /path-to-project/droptoken_game/`
4. Create a new virtual environment `virtualenv venv`
5. Active the new virtual environment `source venv/bin/activate`
6. Install requirements into virtual environment `venv/bin/pip install -r requirements.txt`
    - This will install Flask framework, mysql connector...etc.
7. Login to `mysql -u USER -pPASS` and create a new database `CREATE DATABASE testdb;`
8. Import the test data `mysql -u USER -pPASS testdb < ./sql/droptoken_game_sample_db.sql`
9. Start the application by `venv/bin/python app.py`
10. Once up and running visit any of the endpoint urls in the ***ENDPOINTS*** section.

## Available Endpoints:
These are the current available endpoints for this service.

***Return All In-Progress Endpoints***

`curl -X GET 'http://localhost:5000/drop_token'`

***Create New Game***
```
curl --header "Content-Type: application/json" \
    --request POST \
    --data '{ "players": ["player20", "player21"], "columns": 4, "rows": 4}' \
    http://localhost:5000/drop_token
```

***Get State of Game***

`curl -X GET 'http://localhost:5000/drop_token/13'`

***Get List of Moves Played***

`curl -X GET 'http://localhost:5000/drop_token/1/moves'`

***Post a Game Move***
```
curl --header "Content-Type: application/json" \
    --request POST \
    --data '{"column" : 2}' \
    http://localhost:5000/drop_token/1/1
```

***Get Move Played***

`curl -X GET 'http://localhost:5000/drop_token/1/moves/2'`

***Player Quits Games***

`curl -X DELETE 'http://localhost:5000/drop_token/1/1'`



## Database Schemas

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

***Games To Players Table***
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

***Moves Tables***
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