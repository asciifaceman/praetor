from marshmallow import Schema, fields

from schema_helpers import ObjectIdField


class Error400(Schema):
    '''Encapsulates a 400 error'''
    status = fields.Integer()
    error = fields.String()
