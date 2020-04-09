"""
User model that represents the user table in the database
and is used by SQLAlchemy to build the table and select and insert
records
"""
from project import db


class User(db.Model):
    """Model for Users"""

    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer,
                   primary_key=True)
    username = db.Column(db.String(64),
                         index=False,
                         unique=True,
                         nullable=False)
    email = db.Column(db.String(80),
                      index=True,
                      unique=True,
                      nullable=False)
    created = db.Column(db.DateTime,
                        index=False,
                        unique=False,
                        nullable=False)
    admin = db.Column(db.Boolean,
                      index=False,
                      unique=False,
                      nullable=False)

    def __init__(self, username, email, created, admin):
        self.username = username
        self.email = email
        self.created = created
        self.admin = admin

    def __repr__(self):
        return f'<User {self.username}>'
