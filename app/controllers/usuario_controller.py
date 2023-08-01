from flask import request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token
from datetime import timedelta
from app.database import db
from app.models.usuario import Usuario

class UsuarioController():

    def registrar(self):

        username =request.json.get('username')
        password =request.json.get('password')

        existing_user = Usuario.query.filter_by(username=username).first()
        if existing_user:
            return jsonify({'error': 'Nome de usuário já está em uso'}), 400
        # Criar um novo usuário
    
        user = Usuario(username, password)
        user.gen_hash()
        
 
        res = db.session.add(user)

        db.session.commit()
        


        return jsonify({'message': 'Usuário criado com sucesso'}), 200
    
    def login(self):
        
        username =request.json.get('username')
        password =request.json.get('password')

        # teste de JWT

        user = Usuario.query.filter_by(username=username).first()

        if user and user.verify_password(password):
            access_token = create_access_token(identity=user.id)
            refresh_token = create_refresh_token(
                identity=user.id,
                expires_delta=timedelta(seconds=1000)

             )
            return jsonify({
                'access_token': access_token,
                'refresh_token': refresh_token,
                'message': 'sucess'
            }),200
        else:
            return jsonify({
                'message': 'usuário ou senha inválidos'
            }), 401

       