from marshmallow import Schema, fields

from schema_helpers import ObjectIdField


class Stream(Schema):
    '''Encapsulates a stream origin'''
    _id = ObjectIdField(required=False)
    url = fields.Str(required=True)
    name = fields.Str(required=True)
    enabled = fields.Bool(required=False, default=False, missing=False)
    tags = fields.List(fields.Str(),required=False, default=list(['']), missing=list(['']))
    polling_frequency = fields.Int(required=False, default=30, missing=30)
    #created_at = fields.String(required=False)
    created_at = fields.String(required=False)
