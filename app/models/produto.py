from app.database import db
from datetime import datetime, timedelta

class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    descricao = db.Column(db.String(255))
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    verificado = db.Column(db.Boolean, default=False)
    imagem = db.Column(db.String(255))
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    usuario = db.relationship('Usuario', backref=db.backref('produtos'))
    instituicao_id = db.Column(db.Integer, db.ForeignKey('instituicao.id'))
    instituicao = db.relationship('Instituicao', backref=db.backref('produtos'))