from bson.errors import InvalidId
from bson.objectid import ObjectId
from marshmallow import ValidationError, fields


class ObjectIdField(fields.Field):
    """
    Marshmallow field for :class:`bson.ObjectId`
    """
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        return str(value)

    def _deserialize(self, value, attr, data, **kwargs):
        try:
            return ObjectId(value)
        except (TypeError, InvalidId) as error:
            raise ValidationError('Invalid ObjectId: %s' % error) from error
