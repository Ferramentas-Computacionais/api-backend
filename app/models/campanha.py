from app.database import db

class Campanha(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    descricao = db.Column(db.String(255))
    data_criacao = db.Column(db.DateTime, default=None)
    data_expiracao = db.Column(db.DateTime, default=None)
    ativo = db.Column(db.Boolean, default=False)
    verificado = db.Column(db.Boolean, default=False)
    imagem = db.Column(db.String(255))
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), unique=True)
