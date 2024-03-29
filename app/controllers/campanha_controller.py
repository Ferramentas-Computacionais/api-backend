from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity
from werkzeug.utils import secure_filename
from app.database import db
from app.models.campanha import Campanha
from app.constants import ADDRESS, ID_ADMIN
import json
import os
import random
from datetime import datetime
import uuid
UPLOAD_FOLDER = 'app/images/campanhas'

class CampanhaController:

    def criar_campanha(self):
      
        nome =  request.form.get('nome')
        descricao =  request.form.get('descricao')
        file =  request.files.get('imagem')
        usuario_id = get_jwt_identity()

        if file:
            filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            random_id = uuid.uuid4().hex[:6]  # Gera um ID aleatório de 6 caracteres
            unique_filename = f"{timestamp}_{random_id}_{filename}"
            filepath = os.path.join(UPLOAD_FOLDER, unique_filename)
            file.save(filepath)
            imagem_path = ADDRESS + "/imagens_campanha/" + unique_filename

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
        campanhas_verificadas = Campanha.query.filter_by(verificado=True).all()

        quantidade = min(quantidade, len(campanhas_verificadas))
        
        campanhas_exibicao = random.sample(campanhas_verificadas, quantidade)

        campanhas_data = []

        for campanha in campanhas_exibicao:
            campanha_data = {
                'id': campanha.id,
                'nome': campanha.nome,
                'descricao': campanha.descricao,
                'verificado': campanha.verificado,
                'imagem': campanha.imagem,
                'usuario_id': campanha.usuario_id
            }
            campanhas_data.append(campanha_data)

        return jsonify(campanhas_data), 200
    
    def excluir_campanha(self, campanha_id):
        campanha = Campanha.query.get(campanha_id)

        if not campanha:
            return jsonify({'error': 'campanha não encontrado'}), 404

        # Verifica se o usuário autenticado é o proprietário do campanha
        if campanha.usuario_id != get_jwt_identity():
            return jsonify({'error': 'Acesso não autorizado'}), 401

        db.session.delete(campanha)
        db.session.commit()

        return jsonify({'message': 'campanha excluído com sucesso'}), 200


    def mostrar_campanhas_admin(self):
        usuario_id = get_jwt_identity()
        
        if usuario_id == ID_ADMIN:
            campanhas = Campanha.query.filter_by(verificado=False).all()
            campanhas_data = []

            for campanha in campanhas:
                campanha_data = {
                    'id': campanha.id,
                    'nome': campanha.nome,
                    'descricao': campanha.descricao,
                    'verificado': campanha.verificado,
                    'imagem': campanha.imagem,
                    'usuario_id': campanha.usuario_id
                }
                campanhas_data.append(campanha_data)

            return jsonify(campanhas_data), 200
        else:
            return jsonify({'message': 'Acesso não autorizado'}), 403

    def achar_campanha_por_usuario_id(self, usuario_id):
            campanha = Campanha.query.filter_by(usuario_id=usuario_id, verificado=True).first()
            campanha_data = []

            if campanha:
                campanhas_data = {
                    'id': campanha.id,
                    'nome': campanha.nome,
                    'descricao': campanha.descricao,
                    
                    'verificado': campanha.verificado,
                    'imagem': campanha.imagem,
                    'usuario_id': campanha.usuario_id
                }
                campanha_data.append(campanhas_data)

                return jsonify(campanha_data), 200
            else:
                return jsonify({'message': 'Nenhuma campanha encontrada para o usuário'}), 404
            
    def achar_campanha_por_usuario_id_admin(self, usuario_id):
            campanha = Campanha.query.filter_by(usuario_id=usuario_id).first()
            campanha_data = []

            if campanha:
                campanhas_data = {
                    'id': campanha.id,
                    'nome': campanha.nome,
                    'descricao': campanha.descricao,
                    
                    'verificado': campanha.verificado,
                    'imagem': campanha.imagem,
                    'usuario_id': campanha.usuario_id
                }
                campanha_data.append(campanhas_data)

                return jsonify(campanha_data), 200
            else:
                return jsonify({'message': 'Nenhuma campanha encontrada para o usuário'}), 404
    def verificar_campanha_admin(self, campanha_id):
        campanha = Campanha.query.get(campanha_id)
        usuario_id = get_jwt_identity()

        if not campanha:
            return jsonify({'error': 'campanha não encontrada'}), 404

        if usuario_id != ID_ADMIN:
            return jsonify({'error': 'Acesso não autorizado'}), 401

        campanha.verificado = True  # Define o campo "verificado" como True
        db.session.commit()

        return jsonify({'message': 'campanha verificada com sucesso'}), 200
    