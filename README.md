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

## TODO's / Ideas To Improve/Extend Service
- TODO: Method size reduction.
    - There are methods mainly in the resource.py where it's body size should be reduced, create methods

- TODO: Refactor the GameCreator class
    - Right now it's a set of static methods. OOify this with maybe a factory design pattern.

- TODO: ORMify complex queries
    - In java you can create nested models with subtypes that are accessble from the parent model.
    - i.e Game would have a subType of moves, can explain more...
    - If we did this, it would ORMify the 2-3 raw join sql queries I used.

- TODO: Add unit tests
     - We have basic integration / endpoint tests, we should write unit tests to test utility functions..etc

- TODO: Add an in-memory database for integration / endpoint tests.
    - Right now we are test CRUD functionality on a MySQL database.
    - Started a config for it in EndpoingTestingConfig

- TODO: Add a basic html GUI page to see the playing board


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

NOTE: If you for some reason when you start and get a db connection error.
You may need to set some environment variables to your local environment. See below

```
export SECRET_KEY='this-is-a-secret'
export MYSQL_USER='test'
export MYSQL_PASSWORD='test'
export MYSQL_HOST='localhost'
export MYSQL_DATABASE='testdb'
```


## Trade-offs/Compromises, Scale, or Performance Issue Considerations
- For high-performance web service using Flask framework might not be the best web framework to service millions of user, like
JIRA. Languages like Java and Frameworks like Spring, Play or any J2EE application/service framework would probably pretty be suited
for specific applications like this. But there has been sites like Obama's 2012 election site and Twilio are both built on this framework and
have handle requests at large scale.
- Using any cloud service, such as AWS or GCP using a load balancer and containerized app clusters should be able to scale and handle each part
of the application.


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
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
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

## Testing / Tests:

### Integration / Endpoint Tests:

##### Testing locally:
1. Currently to run tests you need to have setup the environment locally (See SETUP, locally above)
2. Once setup you can run this command to test all current endpoints:
    -  `venv/bin/python ./app/tests/test_endpoints.py`

##### Testing using Docker:
1. You can current run this bash script locally and it will hit all of the endpoints.
    - ` bash ./scripts/test_endpoints_docker.sh`