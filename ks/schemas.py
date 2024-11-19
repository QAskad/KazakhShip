from marshmallow import Schema, fields

class UserSchema(Schema):
    id = fields.Int()
    username = fields.Str()
    email = fields.Str()

class FileSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    author = fields.Str()
    genre = fields.Str()
    subgenre = fields.Str()
    downloads = fields.Int()
    user_id = fields.Int()
