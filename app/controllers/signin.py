# Se importan las librerias y clases respectivas para hacer el signin
from marshmallow import validate
from flask.views import MethodView
from flask import jsonify, request
from app.helpers.encrypt_pass import Crypt
from app.helpers.error_handler import PostgresqlError
from app.validators.user_val import RegisterUser, RegisterExtra
from app.db.postgresql.model import User
from app.db.postgresql.postgresql_manager import PostgresqlManager
import secrets

# Se incializan las variables con su respectivo metodo
encrypt = Crypt()
user_schema = RegisterUser()
edit_schema = RegisterExtra()
postgres_tool = PostgresqlManager()
pse = PostgresqlError()


class Signin(MethodView):

    def post(self):
        try:
            user_signin = request.get_json()
            errors = user_schema.validate(user_signin)
            if errors:
                return jsonify({'status': 'validators', 'error': errors}), 403
            sac_user = postgres_tool.get_by(User, user_signin['document_u'])
            msg = pse.msg(sac_user)
            if msg.get('status') == 'user':
                new_user = User(
                    document_u=user_signin['document_u'],
                    id_u=secrets.token_hex(5),
                    email_inst=user_signin['email_inst'],
                    password_u=encrypt.hash_string(user_signin['password_u']),
                    name_u='',
                    lastname_u='',
                    phone_u='',
                    city_u='',
                    regional_u='',
                    center_u='',
                    bonding_type=3,
                )
                state = postgres_tool.add(new_user)
                msg = pse.msg(state)
                if msg.get('status') == 'ok':
                    return jsonify({'status': 'ok'}), 200
                else:
                    return jsonify(msg), 400
            else:
                return jsonify(msg), 400
        except Exception as ex:
            return jsonify({'status': 'exception', 'ex': str(ex)}), 403

    def put(self):
        try:
            edit_profile = request.get_json()
            errors = edit_schema.validate(edit_profile)
            if errors:
                return jsonify({'status': 'validators', 'error': errors}), 403
            sac_user = postgres_tool.get_by(
                User, edit_profile['document_u'])
            msg = pse.msg(sac_user)
            if msg.get('status') != 'ok':
                return jsonify(msg), 400
            # Asignacion dinamica de forma tal que los campos no ingresados
            # se guarden con una cadena vacia ('')
            #sac_user.password_u = encrypt.hash_string(edit_profile['password_u'])
            sac_user.name_u = edit_profile['name_u']
            sac_user.lastname_u = edit_profile['lastname_u']
            sac_user.phone_u = edit_profile['phone_u']
            sac_user.city_u = edit_profile['city_u']
            sac_user.regional_u = edit_profile['regional_u']
            sac_user.center_u = edit_profile['center_u']
            sac_user.bonding_type = edit_profile['bonding_type']
            state = postgres_tool.update()
            msg = pse.msg(state)
            if msg.get('status') != 'ok':
                return jsonify(msg), 400
            else:
                return jsonify({'status': 'ok'}), 200
        except Exception as e:
            return jsonify({'status': 'exception', 'ex': e}), 400
