from copy import copy
from datetime import datetime
from unittest import TestCase

from jintolin import exception as exc
from jintolin.tests.model.mongodb import base
from jintolin.tests.model.mongodb import model_base
from jintolin.model.mongodb.const import (
    ID, DOC_ID, CITYPE_ID, TIMESTAMP, LOG, DATA, OPERATOR, LINK)


class MongodbCiModelTestCase(model_base.MongodbBaseModelTestCase,
                             base.TestCase):

    model_attr = "CI"
    collection = "ci"

    sample_schema = {
        u"type": u"object",
        u"properties": {
            u"name": {u"type": u"string"},
            u"age": {u"type": u"integer"},
            u"email": {u"type": u"string"},
        },
        u"required": [u"name"]
    }

    sample1 = {
        u"name": u"boo",
        u"age": 10,
    }

    sample2 = {
        u"name": u"foo",
        u"email": u"foo@localhost"
    }

    sample_bad = {
        u"name": u"woo",
        u"age": u"10",
    }

    def setUp(self):
        super(MongodbCiModelTestCase, self).setUp()
        self.citype_id1 = self.get_new_id()
        self.DATABASE["citype"].insert({
            ID: self.citype_id1,
            TIMESTAMP: datetime.now(),
            DATA: self.sample_schema
        })
        self.sample1[CITYPE_ID] = self.citype_id1
        self.sample2[CITYPE_ID] = self.citype_id1
        self.sample_bad[CITYPE_ID] = self.citype_id1

    def _insert_data(self, doc_id, data, **kwargs):
        doc = {
            ID: doc_id,
            CITYPE_ID: self.citype_id1,
            TIMESTAMP: datetime.now(),
            DATA: data
        }
        doc.update(kwargs)
        self.col.insert(doc)

    def test_list(self):
        super(MongodbCiModelTestCase, self).test_list()
        self.assertEqual(2, len(list(self.model.list(self.citype_id1))))
        self.assertEqual(0, len(list(self.model.list(self.get_new_id()))))

    def test_validate(self):
        self.model.validate(self.sample1)
        self.model.validate(self.sample2)
        self.assertRaises(exc.ValidationError,
                          self.model.validate,
                          self.sample_bad)
        self.sample_bad.pop(CITYPE_ID)
        self.assertRaises(exc.ValidationError,
                          self.model.validate,
                          self.sample_bad)

    def test_link(self):
        self._insert_data(self.id1, copy(self.sample1))
        self._insert_data(self.id2, copy(self.sample2))

        self.model.link(self.id1, self.id2, "foo")
        doc = self.col.find_one({ID: self.id1})
        self.assertEqual(doc.get(LINK), {self.id2: "foo"})

        self.assertRaises(exc.LinkError,
                          self.model.link, self.id1, self.id2, "foo")

        self.assertRaises(exc.LinkError,
                          self.model.link, self.id2, self.id1, "foo")

        self.assertRaises(exc.NotFound,
                          self.model.link, self.id1, self.get_new_id(), "foo")

        self.assertRaises(exc.LinkError,
                          self.model.link, self.id1, self.id1, "foo")

    def test_unlink(self):
        self._insert_data(self.id1, copy(self.sample1), **{
            LINK: {self.id2: "foo"}
        })
        self._insert_data(self.id2, copy(self.sample2))

        self.model.unlink(self.id1, self.id2)
        doc = self.col.find_one({ID: self.id1})
        self.assertEqual(doc[LINK], {})

        self.col.update({ID: self.id1}, {"$set": {LINK: {self.id2: "foo"}}})
        self.model.unlink(self.id2, self.id1)
        doc = self.col.find_one({ID: self.id1})
        self.assertEqual(doc[LINK], {})

        self.assertRaises(exc.LinkError,
                          self.model.unlink, self.id1, self.id2)

        self.assertRaises(exc.NotFound,
                          self.model.unlink, self.id1, self.get_new_id())

    def test_get_linked(self):
        self._insert_data(self.id1, copy(self.sample1))
        self._insert_data(self.id2, copy(self.sample2), **{
                          LINK: {
                              self.id1: "buddy",
                          }})
        docs = self.model.get_linked(self.id1)
        self.assertEqual(1, len(docs))
        self.assertEqual(self.id2, docs[0][ID])
        docs = self.model.get_linked(self.id2)
        self.assertEqual(1, len(docs))
        self.assertEqual(self.id1, docs[0][ID])
