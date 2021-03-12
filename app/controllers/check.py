from flask import jsonify, request
from flask.views import MethodView
from flask import current_app as app
import jwt

class Check(MethodView):

    def get(self):
        header = request.request.headers.get('Authorization')
        if header:
            token = header.split(" ")
            try:
                token_auth = jwt.decode(token[1], app.config['SECRET_KEY'], algorithms=['HS256'])
                return jsonify({'state': 'welcome'}), 200
            except:
                return jsonify({'state': 'token'}), 403
        return jsonify({'state': 'not found'}), 404