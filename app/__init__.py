from flask import Flask, Response, request,current_app
from flask_sqlalchemy import SQLAlchemy
import mysql.connector
import json
from flask_jwt_extended import jwt_required
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from app.database import db  

from app.controllers.usuario_controller import UsuarioController


app = Flask(__name__)
app.debug = True

# Configuração do SQLAlchemy

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/doacoes'
app.config['SECRET_KEY'] = 'bazinga'
ma = Marshmallow(app)

db.init_app(app)
with app.app_context():
    # Criar as tabelas no banco de dados
    #db.drop_all()
    db.create_all()


@app.route('/create-user', methods= ['POST'])
def create_user():
    user = UsuarioController()
    return user.registrar()
JWTManager(app)

@app.route('/login', methods= ['POST'])
def login():
    user = UsuarioController()
    return user.login()


@app.route("/")
@jwt_required()
def index():
    return 'testando autenticação jwt'

if __name__ == '__main__':

    app.run()
