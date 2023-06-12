from flask import jsonify, request
from app.models.instituicao import Instituicao
from app.database import db
from flask_jwt_extended import jwt_required, get_jwt_identity

class InstituicaoController:

    @jwt_required()
    def registrar(self):
        nome = request.json.get('nome')
        email = request.json.get('email')
        telefone = request.json.get('telefone')
        cnpj = request.json.get('cnpj')
        usuario_id = get_jwt_identity()

        existing_instituicao = Instituicao.query.filter_by(usuario_id=usuario_id).first()
        if existing_instituicao:
            return jsonify({'error': 'Instituição já está registrada para este usuário'}), 400

        instituicao = Instituicao(nome=nome, email=email, telefone=telefone, cnpj=cnpj, usuario_id=usuario_id)

        db.session.add(instituicao)
        db.session.commit()

        return jsonify({'message': 'Instituição registrada com sucesso'}), 200
