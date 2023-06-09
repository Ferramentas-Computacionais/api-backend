from app.database import db

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable = False)
    password = db.Column(db.String(255), nullable = False)