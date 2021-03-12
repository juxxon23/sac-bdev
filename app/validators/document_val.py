from marshmallow import Schema, fields, validate, validates, ValidationError

class DocumentVal(Schema):
    document_u = fields.String(required=True, validate=validate.Length(min=3, max=50))
    format_id = fields.Integer(required=True)
    
class CollaboratorShare(Schema):
    id_acta = fields.String(required=True)
    email_inst = fields.String(required=True, validate=validate.Length(min=3, max=50))

class DocumentUpdate(Schema):
    id_acta = fields.String(required=True)
    document_u = fields.String(required=True, validate=validate.Length(min=3, max=50))
    content = fields.String(required=True)