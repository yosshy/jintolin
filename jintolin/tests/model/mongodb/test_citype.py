from copy import copy
from datetime import datetime
from unittest import TestCase

from jintolin import exception as exc
from jintolin.tests.model.mongodb import base
from jintolin.tests.model.mongodb import model_base
from jintolin.model.mongodb.const import (
    DATA, DOC_ID, ID, LOG, LINKABLE, OPERATOR, TIMESTAMP)


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

    def test_add_linkable(self):
        self._insert_data(self.id1, copy(self.sample1))
        self._insert_data(self.id2, copy(self.sample2))

        self.model.add_linkable(self.id1, self.id2)
        doc = self.col.find_one({ID: self.id1})
        self.assertEqual(doc.get(LINKABLE), [self.id2])

        self.model.add_linkable(self.id2, self.id1)
        doc = self.col.find_one({ID: self.id2})
        self.assertEqual(doc.get(LINKABLE), [self.id1])

        self.assertRaises(exc.LinkableError,
                          self.model.add_linkable, self.id1, self.id2)

        self.assertRaises(exc.LinkableError,
                          self.model.add_linkable, self.id2, self.id1)

        self.assertRaises(exc.NotFound,
                          self.model.add_linkable, self.id1, self.get_new_id())

    def test_delete_linkable(self):
        self._insert_data(self.id1, copy(self.sample1), la=[self.id2])
        self._insert_data(self.id2, copy(self.sample2))

        self.assertRaises(exc.LinkableError,
                          self.model.delete_linkable, self.id2, self.id1)

        self.model.delete_linkable(self.id1, self.id2)
        doc = self.col.find_one({ID: self.id1})
        self.assertEqual(doc[LINKABLE], [])

        self.assertRaises(exc.LinkableError,
                          self.model.delete_linkable, self.id1, self.id2)

        self.assertRaises(exc.NotFound,
                          self.model.delete_linkable,
                          self.get_new_id(), self.id1)
