# Jinto Lin
#
# (c)2015  Akira Yoshiyama <akirayoshiyama@gmail.com>

import copy

import jsonschema

from jintolin.model.mongodb import base
from jintolin import exception as exc


class CiTypeModel(base.BaseModel):

    collection = 'citype'

    def validate(self, data):
        """
        Verifies schema
        """
        try:
            schema = copy.copy(data)
            schema["$schema"] = "http://json-schema.org/schema#"
            jsonschema.Draft4Validator.check_schema(schema)
        except jsonschema.SchemaError as e:
            raise exc.ValidationError()
