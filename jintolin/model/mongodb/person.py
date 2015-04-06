# Jinto Lin
#
# (c)2015  Akira Yoshiyama <akirayoshiyama@gmail.com>

import logging

import jsonschema
from passlib.hash import sha256_crypt

from jintolin import exception as exc
from jintolin.model.mongodb import base
from .const import DATA

NAME = u'name'
PASSWORD = u'password'

SCHEMA = {
    "type": "object",
    "properties": {
        NAME: {
            "type": "string",
            "minLength": 1
        },
        PASSWORD: {
            "type": "string",
            "minLength": 8
        },
    },
    "required": [NAME, PASSWORD]
}


class PersonModel(base.BaseModel):

    collection = 'person'

    def validate(self, data, **extra_attr):
        """
        Verifies person document
        """
        try:
            jsonschema.validate(data, SCHEMA)
        except jsonschema.ValidationError as e:
            raise exc.ValidationError()

        data[PASSWORD] = sha256_crypt.encrypt(unicode(data[PASSWORD]))

    def verify_password(self, user, password):
        """
        Verifies password
        """
        try:
            jsonschema.validate({NAME: user, PASSWORD: password}, SCHEMA)
        except jsonschema.ValidationError as e:
            raise exc.AuthError()

        doc = self.col.find_one({"%s.%s" % (DATA, NAME): unicode(user)})
        if doc is None:
            raise exc.AuthError()

        if sha256_crypt.verify(password, unicode(doc[DATA][PASSWORD])):
            return

        raise exc.AuthError()
