import unittest

from fastapi.testclient import TestClient

from api.app import app
from api.initializer import init

client = TestClient(app)


class TestInitializer(unittest.TestCase):

    def test_init(self):
        try:
            init(app)
        except Exception:
            self.fail('Should not fail to init database')
