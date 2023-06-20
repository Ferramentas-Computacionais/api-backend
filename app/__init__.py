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

    #db.drop_all()
    db.create_all()



@app.route('/create-user', methods= ['POST'])
def create_user():
    user = UsuarioController()
    return user.registrar()

@app.route('/login', methods= ['POST'])
def login():
    user = UsuarioController()
    return user.login()


@app.route("/create-instituicao", methods = ['POST'])
#@jwt_required()
def create_instituicao():
    user = InstituicaoController()
    return user.registrar()

@app.route("/mostrar-instituicao/<int:quantidade>", methods = ['GET'])
def read_instituicao(quantidade):
    user = InstituicaoController()
    return user.visualizar_instituicoes_recentes(quantidade)

@app.route('/imagens_logo/<path:filename>')
def servir_imagem(filename):
    return send_from_directory('images/logos', filename)


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


@app.route('/listar-anuncios', methods=['GET'])
def get_anuncios():
    user = AnuncioController()
    return user.listar_anuncios()


@app.route('/anuncios-recentes', methods=['GET'])
def get_anuncios_recentes():
    user = AnuncioController()
    return user.mostrar_anuncios_recentes()


@app.route('/renovar-anuncios/<int:anuncio_id>', methods=['POST'])
@jwt_required()
def renovar_anuncio(anuncio_id):
    user = AnuncioController
    return user.renovar_anuncio(anuncio_id)


if __name__ == '__main__':

    app.run()
