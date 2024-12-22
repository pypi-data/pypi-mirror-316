import pytest
import sys
import os

# Ensure the src directory is in the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from app import create_app  # Adjust the import to match your project structure

@pytest.fixture
def app():
    app = create_app()
    return app

def test_example(app):
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200

import unittest

class TestRoutes(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_home_route(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Historic Data Chart', response.data)

    def test_live_route(self):
        response = self.client.get('/live')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Live Data Chart', response.data)

    def test_onlylive_route(self):
        response = self.client.get('/onlylive')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Only Live Data Chart', response.data)

    def test_404_route(self):
        response = self.client.get('/nonexistent')
        self.assertEqual(response.status_code, 404)

    def test_post_home_route(self):
        response = self.client.post('/')
        self.assertEqual(response.status_code, 400)  # Bad Request

if __name__ == '__main__':
    unittest.main()
