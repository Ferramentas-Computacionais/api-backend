from flask import Flask, Response, request
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
import mysql.connector
import json
from app.database import db  
from app.models import instituicao, produto, usuario


app = Flask(__name__)

from app.controllers import default

# Configuração do SQLAlchemy
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/doacoes'
app.config['SECRET_KEY'] = 'bazinga'
ma = Marshmallow(app)

db.init_app(app)
JWTManager(app)
with app.app_context():
    # Criar as tabelas no banco de dados
    db.drop_all()
    db.create_all()
    

if __name__ == '__main__':

    app.run()
