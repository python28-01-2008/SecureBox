from . import db
from flask_login import UserMixin
from cryptography.fernet import Fernet

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    fernet_key = db.Column(db.String(64), nullable=False)

    def get_fernet(self):
        return Fernet(self.fernet_key.encode('utf-8'))
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(150))
    encrypted_content = db.Column(db.Text)
