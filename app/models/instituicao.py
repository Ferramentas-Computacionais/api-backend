from app.database import db
from geoalchemy2.types import Geometry

class Instituicao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    email = db.Column(db.String(100))
    telefone = db.Column(db.String(13))
    cnpj = db.Column(db.String(14))
    coordenadas = db.Column(db.String(25))
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), unique=True)
    descricao = db.Column(db.String(255))
    