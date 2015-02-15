from neuhatch import db
from sqlalchemy.dialects.postgresql import JSON

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String())
    access_token = db.Column(db.String())
    access_token_secret = db.Column(db.String())

    def __init__(self, username, access_token, access_token_secret):
        self.username = username
        self.access_token = access_token
        self.access_token_secret = access_token_secret

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def serialize(self):
        return {
                "id": self.id,
                "username" : self.username
                }


    def __repr__(self):
        return '<id {}>.<username {}>'.format(self.id, self.username)


