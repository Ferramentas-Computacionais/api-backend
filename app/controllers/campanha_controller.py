from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity
from werkzeug.utils import secure_filename
from app.database import db
from app.models.campanha import Campanha
import json
import os
UPLOAD_FOLDER = 'app/images/campanhas'
ADDRESS = 'http://localhost:5000'
class CampanhaController:

    def criar_campanha(self):
        data = json.loads(request.form.get('data'))
        nome = data['nome']
        descricao = data['descricao']
        usuario_id = 2#get_jwt_identity()
        file = request.files['imagem']

        filename = secure_filename(file.filename)
        filename = file.filename
        if file:
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)
            imagem_path = ADDRESS + "/imagens_campanha/" + filename

        else:
            
            imagem_path = ADDRESS + "/imagens_campanha/default.png"
        campanha_existente = Campanha.query.filter_by(usuario_id=usuario_id).first()
        if campanha_existente:
            return jsonify({'message': 'Já existe uma campanha para este usuário'}), 400
        anuncio = Campanha(nome=nome, descricao=descricao, usuario_id=usuario_id, imagem=imagem_path)

        db.session.add(anuncio)
        db.session.commit()

        return jsonify({'message': 'Campanha criado com sucesso'}), 200
    
    def mostrar_campanhas(self, quantidade):
        campanhas = Campanha.query.order_by(Campanha.id.desc()).limit(quantidade).all()
        campanhas_data = []

        for campanha in campanhas:
            campanha_data = {
                'id': campanha.id,
                'nome': campanha.nome,
                'descricao': campanha.descricao,
                'data_criacao': campanha.data_criacao.strftime('%Y-%m-%d %H:%M:%S') if campanha.data_criacao else None,
                'data_expiracao': campanha.data_expiracao.strftime('%Y-%m-%d %H:%M:%S') if campanha.data_expiracao else None,
                'ativo': campanha.ativo,
                'verificado': campanha.verificado,
                'imagem': campanha.imagem,
                'usuario_id': campanha.usuario_id
            }
            campanhas_data.append(campanha_data)

        return jsonify(campanhas_data), 200
    def achar_campanha_por_usuario_id(self, usuario_id):
            campanha = Campanha.query.filter_by(usuario_id=usuario_id).first()
            if campanha:
                campanha_data = {
                    'id': campanha.id,
                    'nome': campanha.nome,
                    'descricao': campanha.descricao,
                    'data_criacao': campanha.data_criacao.strftime('%Y-%m-%d %H:%M:%S') if campanha.data_criacao else None,
                    'data_expiracao': campanha.data_expiracao.strftime('%Y-%m-%d %H:%M:%S') if campanha.data_expiracao else None,
                    'ativo': campanha.ativo,
                    'verificado': campanha.verificado,
                    'imagem': campanha.imagem,
                    'usuario_id': campanha.usuario_id
                }
                return jsonify(campanha_data), 200
            else:
                return jsonify({'message': 'Nenhuma campanha encontrada para o usuário'}), 404