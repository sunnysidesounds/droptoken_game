

curl -X GET 'http://localhost:5000/drop_token'

curl --header "Content-Type: application/json" \
    --request POST \
    --data '{ "players": ["player1", "player2"], "columns": 4, "rows": 4}' \
    http://localhost:5000/drop_toke/


