from flask import Flask
import json
import unittest
from app import db
from app import api
from config import UnitTestConfig


class BasicEndpointsTests(unittest.TestCase):

    """
    Basic endpoint tests
    - test for 200, 202, 400, 404, 409, 410 response
    - test for valid JSON
    """

    def setUp(self):
        app = Flask(__name__)
        app = UnitTestConfig(app).set_config()
        db.init_app(app)
        api.init_app(app)
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_return_all_inprogress_games_200_response(self):
        response = self.app.get('drop_token', follow_redirects=True)
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(BasicEndpointsTests.is_valid_json(data), True)

    def test_create_new_game_200_response(self):
        payload = json.dumps({"players": ["playerTest1", "playerTest2"], "columns": 4, "rows": 4})
        response = self.app.post('drop_token', headers={"Content-Type": "application/json"}, data=payload)
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.is_valid_json(data), True)

    def test_create_new_game_400_response(self):
        payload = json.dumps({})
        response = self.app.post('drop_token', headers={"Content-Type": "application/json"}, data=payload)
        data = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.is_valid_json(data), True)

    def test_get_state_of_game_200_response(self):
        # Dependent On Record 1
        # TODO: Make this record id 1 dynamic
        response = self.app.get('drop_token/1/moves', follow_redirects=True)
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(BasicEndpointsTests.is_valid_json(data), True)

    def test_get_state_of_game_400_response(self):
        response = self.app.get('drop_token/bad_id', follow_redirects=True)
        data = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(BasicEndpointsTests.is_valid_json(data), True)

    def test_get_state_of_game_404_response(self):
        response = self.app.get('drop_token/1000', follow_redirects=True)
        data = response.get_json()
        self.assertEqual(response.status_code, 404)
        self.assertEqual(BasicEndpointsTests.is_valid_json(data), True)

    def test_get_list_of_moved_played_200_response(self):
        response = self.app.get('drop_token/1', follow_redirects=True)
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(BasicEndpointsTests.is_valid_json(data), True)

    def test_get_list_of_moved_played_400_response(self):
        response = self.app.get('drop_token/no_key', follow_redirects=True)
        data = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(BasicEndpointsTests.is_valid_json(data), True)

    def test_get_list_of_moved_played_404_response(self):
        response = self.app.get('drop_token/11000', follow_redirects=True)
        data = response.get_json()
        self.assertEqual(response.status_code, 404)
        self.assertEqual(BasicEndpointsTests.is_valid_json(data), True)

    def test_post_a_game_move_200_response(self):
        # Dependent On Record 1 for game and player
        # TODO: Make this record id 2 / 4 dynamic
        payload = json.dumps({"column": 1})
        response = self.app.post('drop_token/2/4', headers={"Content-Type": "application/json"}, data=payload)
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.is_valid_json(data), True)

    def test_post_a_game_move_400_response(self):
        # Dependent On Record 1 for game and player
        # TODO: Make this record id 2 / 4 dynamic
        payload = json.dumps({"column": 1000})
        response = self.app.post('drop_token/2/4', headers={"Content-Type": "application/json"}, data=payload)
        data = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.is_valid_json(data), True)

    def test_post_a_game_move_404_response(self):
        payload = json.dumps({})
        response = self.app.post('drop_token/200/400', headers={"Content-Type": "application/json"}, data=payload)
        data = response.get_json()
        self.assertEqual(response.status_code, 404)
        self.assertEqual(self.is_valid_json(data), True)

    def test_post_a_game_move_409_response(self):
        payload = json.dumps({"column": 1000})
        response = self.app.post('drop_token/2/4', headers={"Content-Type": "application/json"}, data=payload)
        data = response.get_json()
        self.assertEqual(response.status_code, 409)
        self.assertEqual(self.is_valid_json(data), True)

    def test_get_move_played_200_response(self):
        response = self.app.get('drop_token/1/moves/2', follow_redirects=True)
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(BasicEndpointsTests.is_valid_json(data), True)

    def test_get_move_played_400_response(self):
        response = self.app.get('drop_token/bad_game_id/moves/2', follow_redirects=True)
        data = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(BasicEndpointsTests.is_valid_json(data), True)

    def test_get_move_played_404_response(self):
        response = self.app.get('drop_token/2/moves/10000', follow_redirects=True)
        data = response.get_json()
        self.assertEqual(response.status_code, 404)
        self.assertEqual(BasicEndpointsTests.is_valid_json(data), True)

    def test_player_quits_game_202_response(self):
        response = self.app.delete('drop_token/3/1', follow_redirects=True)
        data = response.get_json()
        self.assertEqual(response.status_code, 202)
        self.assertEqual(BasicEndpointsTests.is_valid_json(data), True)

    def test_player_quits_game_404_response(self):
        response = self.app.delete('drop_token/3000/1', follow_redirects=True)
        data = response.get_json()
        self.assertEqual(response.status_code, 404)
        self.assertEqual(BasicEndpointsTests.is_valid_json(data), True)

    def test_player_quits_game_410_response(self):
        response = self.app.delete('drop_token/1/1', follow_redirects=True)
        data = response.get_json()
        self.assertEqual(response.status_code, 410)
        self.assertEqual(BasicEndpointsTests.is_valid_json(data), True)

    @staticmethod
    def is_valid_json(data):
        try:
            json.dumps(data)
            return True
        except ValueError:
            return False


if __name__ == "__main__":
    unittest.main()