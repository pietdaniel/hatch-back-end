from flask.ext.testing import TestCase
from neuhatch import app, db


class HatchTestCase(TestCase):
    """Base class for test cases. Uses a SQLite in-memory database."""

    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class OAuthTests(HatchTestCase):
    """Test cases for our application's OAuth flow."""

    def test_oauth_flow_redirects_to_twitter(self):
        response = self.client.get('/oauth')
        self.assertTrue(
            response.location.startswith("https://api.twitter.com/oauth"))
