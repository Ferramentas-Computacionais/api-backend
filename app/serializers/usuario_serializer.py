from marshmallow import fields, validates, ValidationError
from flask_marshmallow import Marshmallow
from app.models import usuario


ma = Marshmallow()

class UserSchema(ma.ModelSchema):
    class Meta:
        model = usuario
    
    username = fields.Str(required=True)
    password = fields.Str(required=True)
