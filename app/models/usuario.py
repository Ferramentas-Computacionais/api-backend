from app.database import db
from passlib.hash import pbkdf2_sha256
from app.models.instituicao import Instituicao

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable = False)
    password = db.Column(db.String(255), nullable = False)
    instituicao = db.relationship('Instituicao', backref='usuario', uselist=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def gen_hash(self):
        self.password = pbkdf2_sha256.hash(self.password)

    def verify_password(self, password):
        #TODO talvez o hash de 512 seja mais seguro
        return pbkdf2_sha256.verify(password, self.password)
    
    def show(self):
        user = {}

        user['id'] = self.id
        user['username'] = self.username

        return user



