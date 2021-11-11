import json
from wsgiref.simple_server import make_server

import falcon
from marshmallow import Schema, fields, ValidationError


def password_validator(p):
    if len(p) < 8:
        raise ValidationError("password must be atleast 8 characters")
    if len(p) > 50:
        raise ValidationError("password must have maximum 50 characters")
    if not any(i.isdigit() for i in p):
        raise ValidationError("password must contain at least 1 number")
    if not any(lambda x: x in "!#$%&'()*+,/-.:;<=>?@[\]^_`{|}~".split() for i in p):  # could have used re module also
        raise ValidationError("password must contain one of these special characters - !#$%&'()*+,/-.:;<=>?@[\]^_`{|}~")


class UserSchema(Schema):
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=password_validator)


class UserResource:

    def on_post(self, req, resp):
        if req.content_length:
            user_dict = json.load(req.stream)
        try:
            user = UserSchema().load(user_dict)
        except ValidationError as err:
            resp.status = falcon.HTTP_400
            resp_dict = {"error": "Bad request", "field_errors": err.messages}
            resp.text = json.dumps(resp_dict)
        print("validation successful. saving the user to the imaginary db!")
        resp.status = falcon.HTTP_201

