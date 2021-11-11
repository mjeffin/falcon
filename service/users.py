import json
import falcon
from marshmallow import Schema, fields, ValidationError


def password_validator(p):
    """Marshmallow validator for password field.
    Could have used re module also, but used conditions to give specific errors"""
    if len(p) < 8:
        raise ValidationError("password must be at least 8 characters")
    if len(p) > 50:
        raise ValidationError("password must have maximum 50 characters")
    if not any(i.isdigit() for i in p):
        raise ValidationError("password must contain at least 1 number")
    special_chars = "!#$%&'()*+,/-.:;<=>?@[\]^_`{|}~"
    if not any(map(lambda x: x in list(special_chars), list(p))):
        raise ValidationError(f"password must contain one of these special characters - {special_chars}")


class UserSchema(Schema):
    """Marshmallow schema to validate user input as per requirements."""
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=password_validator)


class UserResource:
    """Falcon User resource model"""

    def on_post(self,req, resp):
        """handler for post request on User resource"""
        if req.content_length:
            user_dict = json.load(req.stream)
        else:
            user_dict = {}
        has_validation_errors = False
        try:
            user = UserSchema().load(user_dict)
        except ValidationError as err:
            resp.status = falcon.HTTP_400
            resp_dict = {"error": "Bad request", "field_errors": err.messages}
            resp.text = json.dumps(resp_dict)
            has_validation_errors = True # since I couldn't find explicit return in falcon docs
        if not has_validation_errors:
            print("validation successful. saving the user to the imaginary db!")
            resp.status = falcon.HTTP_201
