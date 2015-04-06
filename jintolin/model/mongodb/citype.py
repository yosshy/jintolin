# Jinto Lin
#
# (c)2015  Akira Yoshiyama <akirayoshiyama@gmail.com>

from copy import copy

import jsonschema

from jintolin import exception as exc
from . import base
from .const import ID, TIMESTAMP


class CiTypeModel(base.BaseModel):

    collection = 'citype'

    def validate(self, data, **extra_attr):
        """
        Verifies schema
        """
        try:
            schema = copy(data)
            schema["$schema"] = "http://json-schema.org/schema#"
            jsonschema.Draft4Validator.check_schema(schema)
        except jsonschema.SchemaError as e:
            raise exc.ValidationError()
