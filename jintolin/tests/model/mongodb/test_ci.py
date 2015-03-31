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
CITYPE_ID = u'tid'

class MongodbCiModelTestCase(model_base.MongodbBaseModelTestCase,
                             base.TestCase):

    model_attr = "CI"
    collection = "ci"

    sample_schema = {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "age": {"type": "integer"},
            "email": {"type": "string"},
        },
        "required": ["name"]
    }

    sample1 = {
        "name": "boo",
        "age": 10,
    }

    sample2 = {
        "name": "foo",
        "email": "foo@localhost"
    }

    sample_bad = {
        "name": "woo",
        "age": "10",
    }

    def setUp(self):
        super(MongodbCiModelTestCase, self).setUp()
        self.citype_id = self.get_new_id()
        self.DATABASE["citype"].insert({
            ID: self.citype_id,
            TIMESTAMP: datetime.now(),
            DATA: self.sample_schema
        })
        self.kwargs = dict(citype_id=self.citype_id)

    def _insert_data(self, doc_id, data, **kwargs):
        doc = {
            ID: doc_id,
            CITYPE_ID: self.citype_id,
            TIMESTAMP: datetime.now(),
            DATA: data
        }
        doc.update(kwargs)
        self.col.insert(doc)

    def test_list(self):
        super(MongodbCiModelTestCase, self).test_list()
        self.assertEqual(2, len(list(self.model.list(self.citype_id))))
        self.assertEqual(0, len(list(self.model.list(self.get_new_id()))))

    def test_validate(self):
        self.model.validate(self.sample1, self.citype_id)
        self.model.validate(self.sample2, self.citype_id)
        self.assertRaises(exc.ValidationError,
                          self.model.validate, self.sample1)
        self.assertRaises(exc.ValidationError,
                          self.model.validate, self.sample_bad, self.citype_id)
