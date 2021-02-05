from marshmallow import Schema, fields, validate, validates, ValidationError


class RegisterUser(Schema):
    email_inst = fields.String(
        required=True, validate=validate.Length(min=13, max=50))
    document_u = fields.String(
        required=True, validate=validate.Length(min=3, max=50))
    password_u = fields.String(
        required=True, validate=validate.Length(min=8, max=20))


class RegisterExtra(Schema):
    document_u = fields.String(required=True)
    name_u = fields.String(
        required=False, validate=validate.Length(min=3, max=30))
    lastname_u = fields.String(
        required=False, validate=validate.Length(min=3, max=30))
    phone_u = fields.String(
        required=False, validate=validate.Length(min=7, max=10))
    regional_u = fields.String(
        required=False, validate=validate.Length(min=3, max=100))
    center_u = fields.String(
        required=False, validate=validate.Length(min=3, max=100))
    description_c = fields.List(fields.String(), required=False)
    description_r = fields.List(fields.String(), required=False)
    bonding_type = fields.Integer(required=False)


class LoginUser(Schema):
    document_u = fields.String(
        required=True, validate=validate.Length(min=10, max=50))
    password_u = fields.String(
        required=True, validate=validate.Length(min=8, max=20))
