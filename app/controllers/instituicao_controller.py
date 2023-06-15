from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
import os
from app.database import db
from app.models.instituicao import Instituicao

UPLOAD_FOLDER = 'app/images/logos'

class InstituicaoController:

    @jwt_required()
    def registrar(self):

        nome = request.json.get('nome')
        email = request.json.get('email')
        telefone = request.json.get('telefone')
        cnpj = request.json.get('cnpj')
        latitude = request.json.get('latitude')
        longitude = request.json.get('longitude')
        coordenadas = str(longitude)+","+str(latitude)
        descricao = request.json.get('descricao')
        usuario_id = get_jwt_identity()

      
        file = request.files['file']
        filename = file.filename
        if file:
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)
            imagem_path = os.path.join(UPLOAD_FOLDER, filename)
        else:
            
            imagem_path = 'app/images/logos/default.png'





        existing_instituicao = Instituicao.query.filter_by(usuario_id=usuario_id).first()
        if existing_instituicao:
            return jsonify({'error': ' Uma Instituição já está registrada para este usuário'}), 400



        instituicao = Instituicao(nome=nome, email=email, telefone=telefone, cnpj=cnpj, coordenadas=coordenadas, imagem=imagem_path, descricao=descricao,  usuario_id=usuario_id)

        db.session.add(instituicao)
        db.session.commit()

        return jsonify({'message': 'Nova Instituição registrada com sucesso'}), 200
