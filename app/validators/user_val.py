from marshmallow import Schema, fields, validate, validates, ValidationError


class RegisterUser(Schema):

    valid_email = ""
    email_inst = fields.String(
        required=True, validate=validate.Length(min=13, max=50))
    document_u = fields.String(
        required=True, validate=validate.Length(min=3, max=50))
    password_u = fields.String(
        required=True, validate=validate.Length(min=8, max=20))

    @validates('email_inst')
    def validate_email(self, email_inst):
        self.valid_email = email_inst.split('@')
        if self.valid_email[1] == 'misena.edu.co' or self.valid_email[1] == 'sena.edu.co':
            pass
        else:
            raise ValidationError('Invalid email domain')


class RegisterExtra(Schema):
    document_u = fields.String(required=True)
    name_u = fields.String(
        required=False, validate=validate.Length(min=3, max=30))
    lastname_u = fields.String(
        required=False, validate=validate.Length(min=3, max=30))
    phone_u = fields.String(
        required=False, validate=validate.Length(min=7, max=10))
    city_u = fields.String(
        required=False, validate=validate.Length(min=7, max=10))
    regional_u = fields.String(
        required=False, validate=validate.Length(min=3, max=100))
    center_u = fields.String(
        required=False, validate=validate.Length(min=3, max=100))
    bonding_type = fields.Integer(required=False)
    password_u = fields.String(
        required=False, validate=validate.Length(min=8, max=20))


class LoginUser(Schema):
    email_inst = fields.String(
        required=True, validate=validate.Length(min=13, max=50))
    password_u = fields.String(
        required=True, validate=validate.Length(min=8, max=20))
