from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
import os
from app.database import db
from app.models.produto import Produto
import json

UPLOAD_FOLDER = 'app/images/anuncios'

class AnuncioController:

    
    def criar_anuncio(self):
        data = json.loads(request.form.get('data'))
        nome = data['nome']
        descricao = data['descricao']
        usuario_id = get_jwt_identity()
        file = request.files['imagem']

        filename = secure_filename(file.filename)
        if file:
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)
            imagem_path = os.path.join(UPLOAD_FOLDER, filename)
        else:
            imagem_path = 'app/images/anuncios/default.png'

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
        if anuncio.data_expiracao < datetime.now().date():
            anuncio.desativado = True
            db.session.commit()
            return jsonify({'error': 'Anúncio expirado'}), 400

        if not anuncio:
            return jsonify({'error': 'Anúncio não encontrado'}), 404

        anuncio_data = {
            'id': anuncio.id,
            'nome': anuncio.nome,
            'descricao': anuncio.descricao
        }

        return jsonify(anuncio_data), 200
    
    def mostrar_anuncios_recentes(self):
        # Obtém o valor do parâmetro "limite" da query string (GET)
        limite = request.args.get('limite', default=10, type=int)

        # Retorna os anúncios mais recentes
        anuncios = Produto.query.order_by(Produto.data_publicacao.desc()).limit(limite).all()

        return jsonify({'anuncios': [anuncio.to_dict() for anuncio in anuncios]}), 200

    def listar_anuncios(self):
        produtos = Produto.query.filter(Produto.ativo == True, Produto.data_expiracao >= datetime.now().date()).all()

        produtos_data = []
        for produto in produtos:
            produto_data = {
                'id': produto.id,
                'nome': produto.nome,
                'descricao': produto.descricao
            }
            produtos_data.append(produto_data)

        return jsonify(produtos_data), 200
    

    def renovar_anuncio(self, anuncio_id):
        produto = Produto.query.get(anuncio_id)

        if not produto:
            return jsonify({'error': 'Anúncio não encontrado'}), 404

        # Verifica se o usuário autenticado é o proprietário do anúncio
        elif produto.usuario_id != get_jwt_identity():
            return jsonify({'error': 'Acesso não autorizado'}), 401

        # Verifica se o anúncio já está expirado
        elif produto.data_expiracao >= datetime.now().date():
            return jsonify({'error': 'O anúncio ainda está ativo'}), 400
        else:
            # Define a nova data de expiração para 14 dias a partir da data atual
            nova_data_expiracao = datetime.now().date() + timedelta(days=14)
            produto.data_expiracao = nova_data_expiracao
            produto.ativo = True
            db.session.commit()

            return jsonify({'message': 'Anúncio renovado com sucesso'}),200