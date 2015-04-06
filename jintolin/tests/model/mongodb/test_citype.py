from copy import copy
from datetime import datetime
from unittest import TestCase

from jintolin import exception as exc
from . import base
from . import model_base
from jintolin.model.mongodb.const import (
    DATA, DOC_ID, ID, LOG, OPERATOR, TIMESTAMP)


class MongodbCiTypeModelTestCase(model_base.MongodbBaseModelTestCase,
                                 base.TestCase):
    """CiTypeModel test case"""

    model_attr = "CITYPE"
    collection = "citype"

    sample1 = {
        u"type": u"object",
        u"properties": {
            u"name": {u"type": u"string"},
            u"email": {u"type": u"string"},
        },
        u"required": [u"name"]
    }

    sample2 = {
        u"type": u"object",
        u"properties": {
            u"key": {u"type": u"string"},
            u"value": {u"type": u"integer"},
        },
        u"required": [u"key", u"value"]
    }

    sample_bad = {
        u"type": u"object",
        u"properties": {
            u"name": {u"type": u"string"},
            u"email": {u"type": u"bad"},
        },
        u"required": [u"name"]
    }

    def test_validate(self):
        self.model.validate(self.sample1)
        self.model.validate(self.sample2)
        self.assertRaises(exc.ValidationError,
                          self.model.validate, self.sample_bad)
