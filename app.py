from flask import Flask
from flask_cors import CORS
from routes import user, document
from db.postgresql.model import db

app = Flask(__name__)
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'False'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://dwmdwuxrbsmznj:ced17943385fa0ef9f237f025f138b0200ebd897f32a01bc7d9908023bcebf7c@ec2-52-204-113-104.compute-1.amazonaws.com:5432/dc3cnsfmu7o2u'
#app.config["MONGO_URI"] = "mongodb://localhost:27017/sac-ddb" 
CORS(app, support_credentials=True, resources={"*": {"origins": "*"}})
db.init_app(app)

# User routes
app.add_url_rule(user['login'], view_func=user['view_func_login'])
app.add_url_rule(user['signin'], view_func=user['view_func_signin'])

# Document routes
app.add_url_rule(document['document'], view_func=document['view_func_document'])

if __name__ == "__main__":
    app.run()