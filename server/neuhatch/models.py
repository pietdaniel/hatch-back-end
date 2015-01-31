from neuhatch import db
from sqlalchemy.dialects.postgresql import JSON

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String())

    def __init__(self, username):
        self.username = username

    def __repr__(self):
        return '<id {}>.'.format(self.id)


