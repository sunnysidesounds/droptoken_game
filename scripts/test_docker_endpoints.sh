# List of Service Endpoints

# ReturnAllInProgressGames endpoint resource
curl -X GET 'http://localhost:5000/drop_token'

# CreateNewGame endpoint resource
curl --header "Content-Type: application/json" \
    --request POST \
    --data '{ "players": ["player20", "player21"], "columns": 4, "rows": 4}' \
    http://localhost:5000/drop_token

# GetStateOfGame endpoint resource
curl -X GET 'http://localhost:5000/drop_token/13'

# GetListOfMovesPlayed endpoint resource
curl -X GET 'http://localhost:5000/drop_token/1/moves'


# PostAGameMove endpoint resource
curl --header "Content-Type: application/json" \
    --request POST \
    --data '{"column" : 2}' \
    http://localhost:5000/drop_token/1/1


# GetMovePlayed endpoint resource
curl -X GET 'http://localhost:5000/drop_token/2/moves/bad_test'
curl -X GET 'http://localhost:5000/drop_token/1/moves/2'

# PlayerQuitsGame endpoint resource
curl -X DELETE 'http://localhost:5000/drop_token/1/1'



