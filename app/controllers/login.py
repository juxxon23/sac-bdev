from flask import jsonify, request
from flask.views import MethodView
from app.validators.user_val import LoginUser
from app.db.postgresql.model import User
from app.db.postgresql.postgresql_manager import PostgresqlManager
from app.helpers.encrypt_pass import Crypt
from app.helpers.error_handler import PostgresqlError
from flask import current_app as app
import jwt
import bcrypt
import datetime

user_schema = LoginUser()
postgres_tool = PostgresqlManager()
crypt = Crypt()
pse = PostgresqlError()

class Login(MethodView):

    def post(self):
        try:
            user_login = request.get_json()
            errors = user_schema.validate(user_login)
            if errors:
                return jsonify({'status': 'validators', 'error': errors}), 400
            sac_user = postgres_tool.get_by_email(User, user_login['email_inst'])
            msg = pse.msg(sac_user)
            if msg.get('status') != 'ok':
                return jsonify(msg), 400
            else:
                if crypt.check_hash(user_login['password_u'], sac_user.password_u):
                    encoded_jwt = jwt.encode({'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=300), 'udosc': sac_user.document_u}, app.config['SECRET_KEY'], algorithm='HS256')
                    return jsonify({'status': 'welcome', 'username': sac_user.document_u, 'tkse': encoded_jwt}), 200
                else:
                    return jsonify({'status': 'password'}), 400
        except Exception as ex:
            return jsonify({'status': 'exception', 'ex': str(ex)}), 400
