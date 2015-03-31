from datetime import datetime
from unittest import TestCase

from jintolin import exception as exc
from jintolin.tests.model.mongodb import base
from jintolin.tests.model.mongodb import model_base

ID = u'_id'
DOC_ID = u'did'
TIMESTAMP = u'ts'
LOG = u'l'
DATA = u'data'
OPERATOR = u'o'


class MongodbCiTypeModelTestCase(model_base.MongodbBaseModelTestCase,
                                 base.TestCase):
    """CiTypeModel test case"""

    model_attr = "CITYPE"
    collection = "citype"

    sample1 = {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "email": {"type": "string"},
        },
        "required": ["name"]
    }

    sample2 = {
        "type": "object",
        "properties": {
            "key": {"type": "string"},
            "value": {"type": "integer"},
        },
        "required": ["key", "value"]
    }

    sample_bad = {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "email": {"type": "bad"},
        },
        "required": ["name"]
    }

    def test_validate(self):
        self.model.validate(self.sample1)
        self.model.validate(self.sample2)
        self.assertRaises(exc.ValidationError,
                          self.model.validate, self.sample_bad)
