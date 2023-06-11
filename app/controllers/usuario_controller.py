from flask import request, jsonify

from app.database import db
from app.models.usuario import Usuario


class UsuarioController():
    def registrar(self):

        username =request.json.get('username')
        password =request.json.get('password')

    
        # Criar um novo usuário
    
        user = Usuario(username, password)
        user.gen_hash()
        
 
        res = db.session.add(user)

        db.session.commit()



        return jsonify({'message': 'Usuário criado com sucesso'}), 200
