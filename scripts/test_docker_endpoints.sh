
#
curl -X GET 'http://localhost:5000/drop_token'

#
curl --header "Content-Type: application/json" \
    --request POST \
    --data '{ "players": ["player1", "player2"], "columns": 4, "rows": 4}' \
    http://localhost:5000/drop_token/

curl --header "Content-Type: application/json" \
    --request POST \
    --data '{ "players": ["player3", "player4"], "columns": 4, "rows": 4}' \
    http://localhost:5000/drop_token/

curl --header "Content-Type: application/json" \
    --request POST \
    --data '{ "players": ["player5", "player6"], "columns": 4, "rows": 4}' \
    http://localhost:5000/drop_token/

`curl --header "Content-Type: application/json" \
    --request POST \
    --data '{ "players": ["player1", "player7"], "columns": 4, "rows": 4}' \
    http://localhost:5000/drop_token/`

#
curl -X GET 'http://localhost:5000/drop_token/13'

curl -X GET 'http://localhost:5000/drop_token/c52b16e0-d3b7-11ea-879a-8c85904e8d06'


curl --header "Content-Type: application/json" \
    --request POST \
    --data '{"column" : 2}' \
    http://localhost:5000/drop_token/18/1

curl -X GET 'http://localhost:5000/drop_token/19/moves/3'



