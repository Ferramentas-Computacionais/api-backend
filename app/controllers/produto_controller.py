from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
import os
from app.database import db
from app.models.produto import Produto
import json
from app.constants import ADDRESS, ID_ADMIN
from datetime import datetime
import uuid
UPLOAD_FOLDER = 'app/images/anuncios'
class AnuncioController:

    
    def criar_anuncio(self):
        nome = request.form.get('nome')
        descricao = request.form.get('descricao')
        usuario_id = get_jwt_identity()
        file = request.files.get('imagem')
        if file:
            filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            random_id = uuid.uuid4().hex[:6]  # Gera um ID aleatório de 6 caracteres
            unique_filename = f"{timestamp}_{random_id}_{filename}"
            filepath = os.path.join(UPLOAD_FOLDER, unique_filename)
            file.save(filepath)
            imagem_path = ADDRESS + "/imagens_anuncio/" + unique_filename

        else:
            
            imagem_path = ADDRESS + "/imagens_logo/default.png"
        anuncio = Produto(nome=nome, descricao=descricao, usuario_id=usuario_id, imagem=imagem_path)

        db.session.add(anuncio)
        db.session.commit()

        return jsonify({'message': 'Anúncio criado com sucesso'}), 200


    def excluir_anuncio(self, anuncio_id):
        anuncio = Produto.query.get(anuncio_id)

        if not anuncio:
            return jsonify({'error': 'Anúncio não encontrado'}), 404

        # Verifica se o usuário autenticado é o proprietário do anúncio
        if anuncio.usuario_id != get_jwt_identity():
            return jsonify({'error': 'Acesso não autorizado'}), 401

        db.session.delete(anuncio)
        db.session.commit()

        return jsonify({'message': 'Anúncio excluído com sucesso'}), 200


    def editar_anuncio(self, anuncio_id):
        anuncio = Produto.query.get(anuncio_id)

        if not anuncio:
            return jsonify({'error': 'Anúncio não encontrado'}), 404

        # Verifica se o usuário autenticado é o proprietário do anúncio
        if anuncio.usuario_id != get_jwt_identity():
            return jsonify({'error': 'Acesso não autorizado'}), 401

        nome = request.form.get['nome']
        descricao = request.form.get['descricao']

        file = request.files['imagem']
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)
            imagem_path = os.path.join(UPLOAD_FOLDER, filename)
            anuncio.imagem = imagem_path

        anuncio.nome = nome
        anuncio.descricao = descricao

        db.session.commit()

        return jsonify({'message': 'Anúncio atualizado com sucesso'}), 200

    def mostrar_anuncio(self, anuncio_id):
        anuncio = Produto.query.get(anuncio_id)

        # Verifica se o anúncio está expirado
        if anuncio.verificado==False:
            db.session.commit()
            return jsonify({'error': 'Anúncio não verificado ainda'}), 400

        if not anuncio:
            return jsonify({'error': 'Anúncio não encontrado'}), 404

        anuncio_data = {
            'id': anuncio.id,
            'nome': anuncio.nome,
            'descricao': anuncio.descricao,
            'data_criacao': anuncio.data_criacao,
            'imagem': anuncio.imagem,
            'instituicao': {
                'id': anuncio.usuario.instituicao.id,
                'nome': anuncio.usuario.instituicao.nome,
                'endereco': anuncio.usuario.instituicao.coordenadas,
            }

        }

        return jsonify(anuncio_data), 200
    
    def mostrar_anuncios_recentes(self):
        # Obtém o valor do parâmetro "limite" da query string (GET)
        limite = request.args.get('limite', default=10, type=int)

        # Retorna os anúncios mais recentes
        anuncios = Produto.query.order_by(Produto.data_publicacao.desc()).limit(limite).all()

        return jsonify({'anuncios': [anuncio.to_dict() for anuncio in anuncios]}), 200

    def listar_anuncios(self):
        produtos = Produto.query.filter(Produto.verificado == True).all()

        produtos_data = []
        for produto in produtos:
            produto_data = {
            'id': produto.id,
            'nome': produto.nome,
            'descricao': produto.descricao,
            'data_criacao': produto.data_criacao,
            'imagem': produto.imagem,
            
            'instituicao': {
                'id': produto.usuario.instituicao.id,
                'nome': produto.usuario.instituicao.nome,
                'endereco': produto.usuario.instituicao.coordenadas,
                # Adicione outros campos da instituição que você deseja incluir no JSON
            }
            }
            produtos_data.append(produto_data)

        return jsonify(produtos_data), 200
    
    def listar_anuncios_por_usuario(self, usuario_id):
        produtos = Produto.query.filter_by(usuario_id=usuario_id, verificado=True).all()

        produtos_data = []
        for produto in produtos:
            produto_data = {
                'id': produto.id,
                'nome': produto.nome,
                'descricao': produto.descricao,
                'imagem': produto.imagem,
                'verificado': produto.verificado,
                'instituicao': {
                    'id': produto.usuario.instituicao.id,
                    'nome': produto.usuario.instituicao.nome,
                    'endereco': produto.usuario.instituicao.coordenadas,
                }
            }
            produtos_data.append(produto_data)

        return jsonify(produtos_data), 200
    
    def listar_anuncios_por_usuario_admin(self, usuario_id):
        produtos = Produto.query.filter_by(usuario_id=usuario_id).all()

        produtos_data = []
        for produto in produtos:
            produto_data = {
                'id': produto.id,
                'nome': produto.nome,
                'descricao': produto.descricao,
                'imagem': produto.imagem,
                'verificado': produto.verificado,
                'instituicao': {
                    'id': produto.usuario.instituicao.id,
                    'nome': produto.usuario.instituicao.nome,
                    'endereco': produto.usuario.instituicao.coordenadas,
                }
            }
            produtos_data.append(produto_data)

        return jsonify(produtos_data), 200
    

    def listar_anuncios_admin(self):
        usuario_id = get_jwt_identity()
        if usuario_id == ID_ADMIN:
            produtos = Produto.query.filter_by(verificado=False).all()

            produtos_data = []
            for produto in produtos:
                produto_data = {
                'id': produto.id,
                'nome': produto.nome,
                'descricao': produto.descricao,
                'data_criacao': produto.data_criacao,
                'imagem': produto.imagem,
                
                'instituicao': {
                    'id': produto.usuario.instituicao.id,
                    'nome': produto.usuario.instituicao.nome,
                    'endereco': produto.usuario.instituicao.coordenadas,
                    # Adicione outros campos da instituição que você deseja incluir no JSON
                }
                }
                produtos_data.append(produto_data)

            return jsonify(produtos_data), 200
        else:
            return jsonify({'message': 'anuncios não mostrados com sucesso'}), 404
        

    def verificar_anuncio_admin(self, anuncio_id):
        anuncio = Produto.query.get(anuncio_id)
        usuario_id = get_jwt_identity()

        if not anuncio:
            return jsonify({'error': 'Anúncio não encontrado'}), 404

        if usuario_id != ID_ADMIN:
            return jsonify({'error': 'Acesso não autorizado'}), 401

        anuncio.verificado = True  # Define o campo "verificado" como True
        db.session.commit()

        return jsonify({'message': 'Anúncio verificado com sucesso'}), 200

