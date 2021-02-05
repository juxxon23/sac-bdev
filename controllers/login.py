from flask import jsonify, request
from flask.views import MethodView
from validators.user_val import LoginUser
from config.config_key import KEY_TOKEN_AUTH
from db.postgresql.model import User, Competencies
from db.postgresql.postgresql_manager import PostgresqlManager
from helpers.encrypt_pass import Crypt
import jwt
import bcrypt
import datetime

user_schema = LoginUser()
postgres_tool = PostgresqlManager()
crypt = Crypt()

class Login(MethodView):

    def post(self):
        try:
            user_login = request.get_json()
            errors = user_schema.validate(user_login)
            if errors:
                return jsonify({'status': 'validators', 'error': errors}), 403
            user_cred = postgres_tool.get_by(User, user_login['document_u'])
            if user_cred == None:
                return jsonify({'status': 'document'}), 403
            elif type(user_cred) == dict:
                return jsonify({'status': user_cred['error'], 'ex': user_cred['ex']}), 403  
            else:
                if crypt.check_hash(user_login['password_u'], user_cred.password_u):
                    encoded_jwt = jwt.encode({'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=300), 'nombre': user_cred.name_u}, KEY_TOKEN_AUTH, algorithm='HS256')
                    return jsonify({'status': 'welcome', 'token': encoded_jwt}), 203
                else:
                    return jsonify({'status': 'password'}), 403
        except Exception as ex:
            return jsonify({'status': 'exception', 'ex': str(ex)}), 403
