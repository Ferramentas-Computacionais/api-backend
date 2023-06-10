from app.database import db

class Instituicao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    email = db.Column(db.String(100))
    telefone = db.Column(db.String(13))
    cnpj = db.Column(db.String(14))
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), unique=True)

    