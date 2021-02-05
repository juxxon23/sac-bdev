# Se importan las librerias y clases respectivas para hacer el signin
from marshmallow import validate
from flask.views import MethodView
from flask import jsonify, request
from helpers.encrypt_pass import Crypt
from db.postgresql.model import User, Competencies, Results
from validators.user_val import RegisterUser, RegisterExtra
from db.postgresql.postgresql_manager import PostgresqlManager
from db.postgresql.model import User, Competencies, Results


# Se incializan las variables con su respectivo metodo
encrypt = Crypt()
user_schema1 = RegisterUser()
user_schema2 = RegisterExtra()
postgres_tool = PostgresqlManager()


class Signin(MethodView):

    def post(self):
        try:
            user_signin = request.get_json()
            errors = user_schema1.validate(user_signin)
            if errors:
                return jsonify({'state': 'error', 'error': errors}), 403
            document_cp = postgres_tool.get_by(User, user_signin['document_u'])
            if document_cp != None:
                return jsonify({'state': 'user exists'}), 403
            new_user = User(
                document_u=user_signin['document_u'],
                email_inst=user_signin['email_inst'],
                password_u=encrypt.hash_string(user_signin['password_u']),
                name_u='',
                lastname_u='',
                phone_u='',
                regional_u='',
                center_u='',
                bonding_type=3,
            )
            state = postgres_tool.add(new_user)
            if state == 'ok':
                return jsonify({'state': 'ok', 'msg': str(state)}), 200
            elif type(state) == dict:
                return jsonify({'status': state['error'], 'ex': state['ex']}), 403  
            else:
                return jsonify({'status': 'unknown'}), 403        
        except Exception as ex:
            return jsonify({'state': 'exception', 'ex':str(ex)}), 403

    def put(self):
        try:
            users_signinExt = request.get_json()
            erorrs = user_schema2.validate(users_signinExt)
            if erorrs:
                return jsonify({'state': 'error', 'error': erorrs}), 403
            document = postgres_tool.get_by(
                User, users_signinExt['document_u'])
            document.name_u = users_signinExt['name_u']
            document.lastname_u = users_signinExt['lastname_u']
            document.phone_u = users_signinExt['phone_u']
            document.regional_u = users_signinExt['regional_u']
            document.center_u = users_signinExt['center_u']
            document.description_c = users_signinExt['description_c']
            document.description_r = users_signinExt['description_r']
            state = postgres_tool.update()
            return jsonify({'state': 'ok'}), 203
        except Exception as e:
            return jsonify({'status': 'error', 'error': e}), 403
