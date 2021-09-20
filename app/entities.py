from app import db

class Users(db.Model):
    id_user = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), index=True, unique=True)
    passw = db.Column(db.String(), index=True, unique=True)
    adm = db.Column(db.Boolean, index=True, unique=True)

    def __repr__(self):
        return '<Users {}>'.format(self.username)