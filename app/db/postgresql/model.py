from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'User'

    document_u = db.Column(db.String(20), primary_key=True, nullable=False)
    id_u = db.Column(db.String(10), nullable=False, unique=True)
    email_inst = db.Column(db.String(60), nullable=False)
    password_u = db.Column(db.String(128), nullable=False)
    name_u = db.Column(db.String(30), nullable=False)
    lastname_u = db.Column(db.String(30), nullable=False)
    phone_u = db.Column(db.String(12), nullable=False)
    city_u = db.Column(db.String(30), nullable=False)
    regional_u = db.Column(db.String(100), nullable=False)
    center_u = db.Column(db.String(100), nullable=False)
    bonding_type = db.Column(db.Integer, db.ForeignKey('Bonding.id_bon'), nullable=False)

    def __init__(self, document_u, id_u, email_inst, password_u, name_u, lastname_u, phone_u, city_u, regional_u, center_u, bonding_type):
        self.document_u = document_u
        self.id_u = id_u
        self.email_inst = email_inst
        self.password_u = password_u
        self.name_u = name_u
        self.lastname_u = lastname_u
        self.phone_u = phone_u
        self.city_u = city_u
        self.regional_u = regional_u
        self.center_u = center_u
        self.bonding_type = bonding_type


class Bonding(db.Model):
    __tablename__ = 'Bonding'

    id_bon = db.Column(db.Integer, primary_key=True, nullable=False, index=True)
    description = db.Column(db.String(30))
    user_bon = db.relationship('User', backref='myBon', lazy='dynamic', foreign_keys='User.bonding_type')

    def __init__(self, description):
        self.description = description


class Paths(db.Model):
    __tablename__ = 'Paths'

    id_path = db.Column(db.Integer, primary_key=True, nullable=False)
    path =  db.Column(db.String(255))
    
    def __init__(self, id_path, path):
        self.path = id_path
        self.path = path