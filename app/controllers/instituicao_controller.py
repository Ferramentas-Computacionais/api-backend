import json
from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
import os
from app.database import db
from app.models.usuario import Usuario
from app.models.campanha import Campanha
from app.models.produto import Produto
from app.models.instituicao import Instituicao
from app.constants import ADDRESS, ID_ADMIN
from datetime import datetime
import uuid


UPLOAD_FOLDER = 'app/images/logos'
class InstituicaoController:
    #TODO fazer as funções de edição de instituição para o usuário
    #@jwt_required()
    def registrar(self):
        nome = request.form.get('nome')
        email = request.form.get('email')
        telefone = request.form.get('telefone')
        cnpj = request.form.get('cnpj')
        descricao = request.form.get('descricao')
        usuario_id = get_jwt_identity()
        coordenadas = request.form.get('coordenadas')
        
        file = request.files.get('imagem')

        if file:
            filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            random_id = uuid.uuid4().hex[:6]  # Gera um ID aleatório de 6 caracteres
            unique_filename = f"{timestamp}_{random_id}_{filename}"
            filepath = os.path.join(UPLOAD_FOLDER, unique_filename)
            file.save(filepath)
            imagem_path = ADDRESS + "/imagens_logo/" + unique_filename

        else:
            
            imagem_path = ADDRESS + "/imagens_logo/default.png"

        existing_instituicao = Instituicao.query.filter_by(usuario_id=usuario_id).first()
        if existing_instituicao:
            return jsonify({'error': ' Uma Instituição já está registrada para este usuário'}), 400

        instituicao = Instituicao(nome=nome, email=email, telefone=telefone, cnpj=cnpj, coordenadas=coordenadas, imagem=imagem_path, descricao=descricao,  usuario_id=usuario_id)

        db.session.add(instituicao)
        db.session.commit()

        return jsonify({'message': 'Nova Instituição registrada com sucesso'}), 200
    
    def visualizar_instituicoes_recentes(self, quantidade):
        instituicoes = Instituicao.query.order_by(Instituicao.data_criacao.desc()).limit(quantidade).all()
        instituicoes_recentes = []

        for instituicao in instituicoes:
            instituicao_data = {
                'id': instituicao.id,
                'nome': instituicao.nome,
                'email': instituicao.email,
                'telefone': instituicao.telefone,
                'cnpj': instituicao.cnpj,
                'coordenadas': instituicao.coordenadas,
                'imagem': instituicao.imagem,
                'usuario_id': instituicao.usuario_id,
                'descricao': instituicao.descricao,
                'data_criacao': instituicao.data_criacao.strftime("%Y-%m-%d %H:%M:%S")
            }
            instituicoes_recentes.append(instituicao_data)

        return jsonify(instituicoes_recentes), 200
    
    def visualizar_instituicao_id(self, id):
        instituicao = Instituicao.query.filter_by(usuario_id=id).first()

        if instituicao:
            instituicao_data = {
                'id': instituicao.id,
                'nome': instituicao.nome,
                'email': instituicao.email,
                'telefone': instituicao.telefone,
                'cnpj': instituicao.cnpj,
                'coordenadas': instituicao.coordenadas,
                'imagem': instituicao.imagem,
                'usuario_id': instituicao.usuario_id,
                'descricao': instituicao.descricao,
                'data_criacao': instituicao.data_criacao.strftime("%Y-%m-%d %H:%M:%S")
            }

            return jsonify(instituicao_data), 200
        else:
            return jsonify({'message': 'Instituição não encontrada'}), 404
        
    def verificar_instituicao(self, usuario_id):
        existing_instituicao = Instituicao.query.filter_by(usuario_id=usuario_id).first()

        if existing_instituicao:
            return jsonify({'message': 'O usuário já possui uma instituição registrada'}), 200
        else:
            return jsonify({'message': 'O usuário ainda não possui uma instituição registrada'}), 404

    
    def excluirTudoDoUsuario(self, usuario_id):
        try:
            # Excluir campanhas do usuário
            campanhas = Campanha.query.filter_by(usuario_id=usuario_id).all()
            for campanha in campanhas:
                db.session.delete(campanha)

            # Excluir anúncios do usuário
            produtos = produto.query.filter_by(usuario_id=usuario_id).all()
            for produto in produtos:
                db.session.delete(produto)

            # Excluir instituição do usuário
            instituicao = Instituicao.query.filter_by(usuario_id=usuario_id).first()
            if instituicao:
                db.session.delete(instituicao)

            # Excluir o usuário
            usuario = Usuario.query.get(usuario_id)
            if usuario:
                db.session.delete(usuario)

            db.session.commit()
            return jsonify({'message': 'Tudo do usuário foi excluído com sucesso'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'Erro ao excluir tudo do usuário'}), 500
    def excluirTudoDoUsuario(self, usuario_id):
        try:
            # Verificar identidade do usuário
            current_user_id = get_jwt_identity()
            
            if current_user_id != ID_ADMIN:
                return jsonify({'error': 'Usuário não tem esse poder'}), 400

            # Excluir campanhas do usuário
            campanhas = Campanha.query.filter_by(usuario_id=usuario_id).all()
            for campanha in campanhas:
                db.session.delete(campanha)

            # Excluir anúncios do usuário
            produtos = Produto.query.filter_by(usuario_id=usuario_id).all()
            for produto in produtos:
                db.session.delete(produto)

            # Excluir instituição do usuário
            instituicao = Instituicao.query.filter_by(usuario_id=usuario_id).first()
            if instituicao:
                db.session.delete(instituicao)

            # Excluir o usuário
            usuario = Usuario.query.get(usuario_id)
            if usuario:
                db.session.delete(usuario)

            db.session.commit()
            return jsonify({'message': 'Tudo do usuário foi excluído com sucesso'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'Erro ao excluir tudo do usuário'}), 500