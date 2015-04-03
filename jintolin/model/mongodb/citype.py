# Jinto Lin
#
# (c)2015  Akira Yoshiyama <akirayoshiyama@gmail.com>

from copy import copy

import jsonschema

from jintolin import exception as exc
from jintolin.model.mongodb import base
from jintolin.model.mongodb.const import ID, TIMESTAMP


class CiTypeModel(base.BaseModel):

    collection = 'citype'

    def validate(self, data, **kwargs):
        """
        Verifies schema
        """
        try:
            schema = copy(data)
            schema["$schema"] = "http://json-schema.org/schema#"
            jsonschema.Draft4Validator.check_schema(schema)
        except jsonschema.SchemaError as e:
            raise exc.ValidationError()
