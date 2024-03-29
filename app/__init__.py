from flask import Flask, Response, request,current_app
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

import mysql.connector
import json
from flask_jwt_extended import jwt_required
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from app.database import db  
from app.controllers.usuario_controller import UsuarioController
from app.controllers.instituicao_controller import InstituicaoController
from app.controllers.produto_controller import AnuncioController
from app.controllers.campanha_controller import CampanhaController

from flask import Flask, send_from_directory

app = Flask(__name__)
app.debug = True
CORS(app, origins='http://localhost:4200')
# Configuração do SQLAlchemy


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/doacoes'
app.config['SECRET_KEY'] = 'bazinga'
JWTManager(app)


ma = Marshmallow(app)

db.init_app(app)
with app.app_context():
    # Importar os modelos
    from app.models.usuario import Usuario
    from app.models.instituicao import Instituicao
    from app.models.produto import Produto
    from app.models.campanha import Campanha

    #pfvr, n descomentem essa linha no servidor de deploy :) S2
    #db.drop_all()
    db.create_all()


#TODO organizar essas rotas (tá muito bagunçado)

#rotas de user

@app.route('/create-user', methods= ['POST'])
@jwt_required()
def create_user():
    user = UsuarioController()
    return user.registrar()

@app.route('/excluir-user/<int:id>', methods= ['POST'])
@jwt_required()
def delete_user(id):
    user = InstituicaoController()
    return user.excluirTudoDoUsuario(id)

@app.route('/login', methods= ['POST'])
def login():
    user = UsuarioController()
    return user.login()

@app.route('/refresh-token', methods=['POST'])
@jwt_required(refresh=True)
def refresh_token():
    user = UsuarioController()
    return user.refresh_token
#rotas de instituição
@app.route("/create-instituicao", methods = ['POST'])
@jwt_required()
def create_instituicao():
    user = InstituicaoController()
    return user.registrar()

@app.route("/mostrar-instituicao/<int:quantidade>", methods = ['GET'])
def read_instituicao(quantidade):
    user = InstituicaoController()
    return user.visualizar_instituicoes_recentes(quantidade)

@app.route("/mostrar-instituicao/id/<int:id>", methods = ['GET'])
def read_instituicao_id(id):
    user = InstituicaoController()
    return user.visualizar_instituicao_id(id)

@app.route("/verificar_instituicao/<int:id>", methods = ['GET'])
def verificar_instituicao(id):
    user = InstituicaoController()
    return user.verificar_instituicao(id)

@app.route('/imagens_logo/<path:filename>')
def servir_imagem(filename):
    return send_from_directory('images/logos', filename)

#rotas de anuncio
@app.route('/create-anuncio', methods=['POST'])
@jwt_required()
def create_anuncio():
    
    user = AnuncioController()
    return user.criar_anuncio()


@app.route('/delete-anuncio/<int:anuncio_id>', methods=['DELETE'])
@jwt_required()
def delete_anuncio(anuncio_id):
    user = AnuncioController()
    return user.excluir_anuncio(anuncio_id)


@app.route('/edit-anuncio/<int:anuncio_id>', methods=['PUT'])
@jwt_required()
def edit_anuncio(anuncio_id):
    user = AnuncioController()
    return user.editar_anuncio(anuncio_id)


@app.route('/mostrar-anuncio/<int:anuncio_id>', methods=['GET'])
def get_anuncio(anuncio_id):
    user = AnuncioController()
    return user.mostrar_anuncio(anuncio_id)

@app.route('/imagens_anuncio/<path:filename>')
def servir_imagem_anuncio(filename):
    return send_from_directory('images/anuncios', filename)

@app.route('/listar-anuncios', methods=['GET'])
def get_anuncios():
    user = AnuncioController()
    return user.listar_anuncios()

@app.route('/listar-anuncios-usuario/<int:usuario_id>', methods=['GET'])
def get_anuncios_user_id(usuario_id):
    user = AnuncioController()
    return user.listar_anuncios_por_usuario(usuario_id)

@app.route('/listar-anuncios-usuario_admin/<int:usuario_id>', methods=['GET'])
@jwt_required()
def get_anuncios_user_id_admin(usuario_id):
    user = AnuncioController()
    return user.listar_anuncios_por_usuario_admin(usuario_id)


@app.route('/anuncios_admin', methods=['GET'])
@jwt_required()
def get_anuncios_admin():
    user = AnuncioController()
    return user.listar_anuncios_admin()

@app.route('/verificar_anuncios_admin/<int:anuncio_id>', methods=['GET'])
@jwt_required()
def verificar_anuncios_admin(anuncio_id):
    user = AnuncioController()
    return user.verificar_anuncio_admin(anuncio_id)

@app.route('/anuncios-recentes', methods=['GET'])
def get_anuncios_recentes():
    user = AnuncioController()
    return user.mostrar_anuncios_recentes()


@app.route('/renovar-anuncios/<int:anuncio_id>', methods=['POST'])
@jwt_required()
def renovar_anuncio(anuncio_id):
    user = AnuncioController
    return user.renovar_anuncio(anuncio_id)


#rotas de campanha
@app.route('/create-campanha', methods=['POST'])
@jwt_required()
def create_campanha():
    user = CampanhaController()
    return user.criar_campanha()

@app.route('/delete-campanha/<int:campanha_id>', methods=['DELETE'])
@jwt_required()
def delete_campanha(campanha_id):
    user = CampanhaController()
    return user.excluir_campanha(campanha_id)

@app.route('/imagens_campanha/<path:filename>')
def servir_imagem_campanha(filename):
    return send_from_directory('images/campanhas', filename)

@app.route('/mostrar-campanha/<int:quantidade>', methods=['GET'])
def mostrar_campanha(quantidade):
    campanha_controller = CampanhaController()
    return campanha_controller.mostrar_campanhas(quantidade)

@app.route('/campanhas/<int:usuario_id>', methods=['GET'])
def achar_campanha_por_user_id(usuario_id):
    campanha_controller = CampanhaController()
    return campanha_controller.achar_campanha_por_usuario_id(usuario_id)

@app.route('/campanhas_admin/<int:usuario_id>', methods=['GET'])
@jwt_required()
def achar_campanha_por_user_id_admin(usuario_id):
    campanha_controller = CampanhaController()
    return campanha_controller.achar_campanha_por_usuario_id_admin(usuario_id)

@app.route('/verificar_campanha_admin/<int:campanha_id>', methods=['GET'])
@jwt_required()
def verificar_campanha_admin(campanha_id):
    user = CampanhaController()
    return user.verificar_campanha_admin(campanha_id)

@app.route('/campanhas_admin', methods=['GET'])
@jwt_required()
def campanhas_admin():
    campanha_controller = CampanhaController()
    return campanha_controller.mostrar_campanhas_admin()

if __name__ == '__main__':

    app.run()
