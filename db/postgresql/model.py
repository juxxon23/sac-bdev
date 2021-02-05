from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'User'

    document_u = db.Column(db.String(20), primary_key=True, nullable=False)
    email_inst = db.Column(db.String(60), nullable=False)
    password_u = db.Column(db.String(128), nullable=False)
    name_u = db.Column(db.String(30), nullable=False)
    lastname_u = db.Column(db.String(30), nullable=False)
    phone_u = db.Column(db.String(12), nullable=False)
    regional_u = db.Column(db.String(100), nullable=False)
    center_u = db.Column(db.String(100), nullable=False)
    bonding_type = db.Column(db.Integer, db.ForeignKey('Bonding.id_bon'), nullable=False)
    comp_fo = db.relationship(
        'Competencies', backref='myComp', lazy='dynamic', foreign_keys='Competencies.document_user')
    res_fo = db.relationship(
        'Results', backref='myRes', lazy='dynamic', foreign_keys='Results.document_user')

    def __init__(self, document_u, email_inst, password_u, name_u, lastname_u, phone_u, regional_u, center_u, bonding_type):
        self.document_u = document_u
        self.email_inst = email_inst
        self.password_u = password_u
        self.name_u = name_u
        self.lastname_u = lastname_u
        self.phone_u = phone_u
        self.regional_u = regional_u
        self.center_u = center_u
        self.bonding_type = bonding_type


class Competencies(db.Model):
    __tablename__ = 'Competencies'

    id_comp = db.Column(db.Integer, primary_key=True, nullable=False, index=True)
    document_user = db.Column(db.String(20), db.ForeignKey('User.document_u'), nullable=False)
    description = db.Column(db.String(255), nullable=False)


    def __init__(self, document_user, description):
        self.document_user = document_user
        self.description = description


class Results(db.Model):
    __tablename__ = 'Results'

    id_res = db.Column(db.Integer, primary_key=True, nullable=False, index=True)
    document_user = db.Column(db.String(20), db.ForeignKey('User.document_u'), nullable=False)
    comp_id = db.Column(db.Integer, db.ForeignKey('Competencies.id_comp'), nullable=False)
    description = db.Column(db.String(255))

    def __init__(self, document_user, comp_id, description):
        self.document_user = document_user
        self.comp_id = comp_id
        self.description = description

class Bonding(db.Model):
    __tablename__ = 'Bonding'

    id_bon = db.Column(db.Integer, primary_key=True, nullable=False, index=True)
    description = db.Column(db.String(255))
    user_bon = db.relationship('User', backref='myBon', lazy='dynamic', foreign_keys='User.bonding_type')

    def __init__(self, description):
        self.description = description
