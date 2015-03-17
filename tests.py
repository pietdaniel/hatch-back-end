from flask.ext.testing import TestCase
from neuhatch import app, db
from flask.ext.login import current_user


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

    def test_no_default_authenticated_user(self):
        with app.test_request_context('/oauth'):
            assert current_user.is_anonymous()

    def test_oauth_flow_redirects_to_twitter(self):
        response = self.client.get('/oauth')
        self.assertTrue(
            response.location.startswith("https://api.twitter.com/oauth"))


class SearchTests(HatchTestCase):
    def test_search_page_is_not_accessible_when_logged_out(self):
        app.config['LOGIN_DISABLED'] = False
        response = self.client.get('/search')
        self.assert401(response)
