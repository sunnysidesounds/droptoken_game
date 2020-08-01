from flask import Flask
import json
import unittest
from app import db
from app import api
from config import UnitTestConfig


class BasicEndpointsTests(unittest.TestCase):

    """
    Basic endpoint tests
    - test for 200 response
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


    # TODO Add Endpoint tests



if __name__ == "__main__":
    unittest.main()