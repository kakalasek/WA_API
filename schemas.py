from marshmallow import fields, Schema

class UserSchema(Schema):
    username = fields.String()