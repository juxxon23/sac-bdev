from flask import Flask
from flask_cors import CORS
from .db.postgresql.model import db

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('config')
    #app.config.from_pyfile('config.py')
    CORS(app, support_credentials=True)
    
    with app.app_context():
        from .routes import user, document
        add_routes(app, user, document)
        db.init_app(app)
        return app

def add_routes(app, user, document):
    # User routes
    app.add_url_rule(user['login'], view_func=user['view_func_login'])
    app.add_url_rule(user['signin'], view_func=user['view_func_signin'])

    # Document routes
    app.add_url_rule(document['document'], view_func=document['view_func_document'])
