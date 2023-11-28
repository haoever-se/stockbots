"""Entry point of the testing"""
import unittest
from app.main import app
from app.db import db, Symbol


class SlackTestCase(unittest.TestCase):
    """Testing slack features"""
    def setUp(self):
        """Set up the app for testing"""
        self.app = app.test_client()
        self.app.testing = True

        # Configure a separate, in-memory SQLite database for tests
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

        # Create the database and its tables within the application context
        with app.app_context():
            db.drop_all()
            db.create_all()

    def tearDown(self):
        """Rollback the session after each test to undo changes"""
        with app.app_context():
            db.session.rollback()
            db.session.remove()

    def test_slack_get_all(self):
        """Testing API slack_get_all"""
        response = self.app.post('/slack/getAll')
        # assert that the post request was successful
        self.assertEqual(response.status_code, 200)

    def test_slack_add(self):
        """Testing API slack_add"""
        response = self.app.post('/slack/add', data={'text': 'NVDA'})

        # assert that the response is 201 (Created)
        self.assertEqual(response.status_code, 201, "Response should be 201 (Created)")
        # If symbol was added, check if it's in the database
        with app.app_context():
            symbol = Symbol.query.filter_by(symbol='NVDA').first()
        self.assertIsNotNone(symbol, "Symbol 'NVDA' should be added to the database.")
        self.assertEqual(symbol.symbol, 'NVDA', "The symbol should be 'NVDA'.")

    def test_slack_check(self):
        """Testing API slack_check"""
        response = self.app.post('/slack/check', data={'text': 'IBM'})
        # assert that the post request was successful
        self.assertEqual(response.status_code, 200)
        # Load the response data
        self.assertIn('Message posted to Slack', response.text, "Message should be sent to Slack")


if __name__ == '__main__':
    unittest.main()
