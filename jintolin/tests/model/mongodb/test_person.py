from copy import copy
from datetime import datetime
from unittest import TestCase

from jintolin import exception as exc
from jintolin.tests.model.mongodb import base
from jintolin.tests.model.mongodb import model_base
from jintolin.model.mongodb.const import (
    ID, DOC_ID, TIMESTAMP, LOG, DATA, OPERATOR)


NAME = u"name"
PASSWORD = u"password"


class MongodbPersonModelTestCase(model_base.MongodbBaseModelTestCase,
                                 base.TestCase):

    model_attr = "PERSON"
    collection = "person"

    sample1 = {
        u"name": u"hoge",
        u"password": u"fugafuga"
    }

    sample2 = {
        u"name": u"foo",
        u"password": u"barbarbar"
    }

    def setUp(self):
        super(model_base.MongodbBaseModelTestCase, self).setUp()
        self.col = self.DATABASE[self.collection]
        self.model = getattr(self, self.model_attr)
        self.id1 = self.get_new_id()
        self.id2 = self.get_new_id()
        if self.kwargs is None:
            self.kwargs = {}
        self.sampleset = {
            self.id1: self.sample1[NAME],
            self.id2: self.sample2[NAME]
        }

    def test_list(self):

        self._insert_data(self.id1, copy(self.sample1))
        self._insert_data(self.id2, copy(self.sample2))
        docs = list(self.model.list())
        self.assertEqual(len(docs), 2)
        self.assertEqual({x[ID]: x[DATA][NAME] for x in docs},
                         self.sampleset)

    def test_get(self):

        self._insert_data(self.id1, copy(self.sample1))
        self._insert_data(self.id2, copy(self.sample2))
        doc1 = self.model.get(self.id1)
        doc2 = self.model.get(self.id2)
        self.assertEqual(doc1[DATA][NAME], self.sample1[NAME])
        self.assertEqual(doc2[DATA][NAME], self.sample2[NAME])
        self.assertRaises(exc.NotFound,
                          self.model.get, self.get_new_id())

    def test_create(self):

        id1 = self.model.create(data=copy(self.sample1),
                                operator="foo", **self.kwargs)
        id2 = self.model.create(data=copy(self.sample2),
                                operator="bar", **self.kwargs)
        sampleset = {id1: self.sample1[NAME], id2: self.sample2[NAME]}
        docs = list(self.col.find())
        self.assertEqual(len(docs), 2)
        self.assertEqual({x[ID]: x[DATA][NAME] for x in docs}, sampleset)
        logs = list(self.DATABASE['log'].find())
        self.assertEqual(len(logs), 2)
        self.assertEqual({x[DOC_ID]: x[DATA][NAME] for x in logs}, sampleset)
        self.assertEqual(["created", "created"],
                         [x[LOG] for x in logs])

    def test_update(self):

        self._insert_data(self.id1, copy(self.sample2))
        self._insert_data(self.id2, copy(self.sample1))
        self.model.update(self.id1, data=copy(self.sample1),
                          operator="foo", **self.kwargs)
        self.model.update(self.id2, data=copy(self.sample2),
                          operator="bar", **self.kwargs)
        docs = list(self.col.find())
        self.assertEqual(len(docs), 2)
        self.assertEqual({x[ID]: x[DATA][NAME] for x in docs},
                         self.sampleset)
        logs = list(self.DATABASE['log'].find())
        self.assertEqual(len(logs), 2)
        self.assertEqual({x[DOC_ID]: x[DATA][NAME] for x in logs},
                         self.sampleset)
        self.assertEqual(["updated", "updated"],
                         [x[LOG] for x in logs])
        self.assertRaises(exc.NotFound,
                          self.model.update,
                          self.get_new_id(), data=copy(self.sample1),
                          operator="foo", **self.kwargs)

    def test_delete(self):

        self._insert_data(self.id1, copy(self.sample1))
        self._insert_data(self.id2, copy(self.sample2))
        docs = list(self.col.find())
        self.assertEqual(2, self.col.count())
        doc1 = self.model.delete(self.id1)
        doc2 = self.model.delete(self.id2)
        self.assertEqual(0, self.col.count())
        logs = list(self.DATABASE['log'].find())
        self.assertEqual(len(logs), 2)
        self.assertEqual(set([x[DOC_ID] for x in logs]),
                         set([self.id1, self.id2]))
        self.assertEqual(["deleted", "deleted"],
                         [x[LOG] for x in logs])

    def test_get_logs(self):

        self._insert_log(self.id1, "created", **{DATA: copy(self.sample1)})
        self._insert_log(self.id1, "updated", **{DATA: copy(self.sample2)})
        self._insert_log(self.id1, "deleted")

        logs = list(self.model.get_logs(self.id1))
        self.assertEqual(len(logs), 3)
        self.assertEqual(["created", "updated", "deleted"],
                         [x[LOG] for x in logs])
        self.assertEqual([self.sample1[NAME], self.sample2[NAME], None],
                         [x.get(DATA, {}).get(NAME) for x in logs])

    def test_validate(self):

        self.assertRaises(exc.ValidationError,
                          self.model.validate,
                          {"password": "hoge"})

        self.assertRaises(exc.ValidationError,
                          self.model.validate,
                          {"name": "", "password": "hoge"})

        self.assertRaises(exc.ValidationError,
                          self.model.validate,
                          {"name": "hoge"})

        self.assertRaises(exc.ValidationError,
                          self.model.validate,
                          {"name": "hoge", "password": ""})

        self.assertRaises(exc.ValidationError,
                          self.model.validate,
                          {"name": "hoge", "password": ["hoge"]})

    def test_verify_password(self):

        self.model.create(data=copy(self.sample1),
                          operator="foo", **self.kwargs)

        self.assertEqual(None,
                         self.model.verify_password(self.sample1[NAME],
                                                    self.sample1[PASSWORD]))

        self.assertRaises(exc.AuthError,
                          self.model.verify_password,
                          self.sample1[NAME], "badpassword")

        self.assertRaises(exc.AuthError,
                          self.model.verify_password,
                          "boo", "hogehoge")

        self.assertRaises(exc.AuthError,
                          self.model.verify_password,
                          "hoge", ["hoge"])
