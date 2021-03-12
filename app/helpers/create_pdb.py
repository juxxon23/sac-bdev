from flask import Flask
from app.db.postgresql.model import db, Bonding, User
from app.db.postgresql.postgresql_manager import PostgresqlManager

def create_app():
    postgreql_tool = PostgresqlManager()
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://sac-ddb:pass123@localhost:5432/sac-ddb'
    with app.app_context():
        db.init_app(app)
        db.create_all()
        bonding_list = postgreql_tool.get_all(Bonding)
        if len(bonding_list) == 3:
            return app
        else:
            contratista = Bonding(description='Contratista')
            planta = Bonding(description='Planta')
            default = Bonding(description='Defecto')
            postgreql_tool.add(contratista, planta, default)
            return app

        
    