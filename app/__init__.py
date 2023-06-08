from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy
import mysql.connector
import json
from app.database import db

app = Flask(__name__)



from app.controllers import default

# Configuração do SQLAlchemy
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/doacoes'
db.init_app(app)

    

if __name__ == '__main__':
    with app.app_context():
        # Criar as tabelas no banco de dados
        db.create_all()
    app.run()
