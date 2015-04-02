from copy import copy
from datetime import datetime

from jintolin import exception as exc
from jintolin.model.mongodb.const import (
    ID, DOC_ID, TIMESTAMP, LOG, DATA, OPERATOR)


class MongodbBaseModelTestCase(object):

    collection = None
    model_attr = None
    sample1 = None
    sample2 = None
    id1 = None
    id2 = None
    kwargs = None

    def setUp(self):
        super(MongodbBaseModelTestCase, self).setUp()
        self.col = self.DATABASE[self.collection]
        self.model = getattr(self, self.model_attr)
        self.id1 = self.get_new_id()
        self.id2 = self.get_new_id()
        if self.kwargs is None:
            self.kwargs = {}
        self.sampleset = {
            self.id1: self.sample1,
            self.id2: self.sample2
        }

    def _insert_data(self, doc_id, data, **kwargs):
        doc = {
            ID: doc_id,
            TIMESTAMP: datetime.now(),
            DATA: data
        }
        doc.update(kwargs)
        self.col.insert(doc)

    def _insert_log(self, doc_id, log, **kwargs):
        entry = {
            ID: self.get_new_id(),
            TIMESTAMP: datetime.now(),
            DOC_ID: doc_id,
            LOG: log
        }
        entry.update(kwargs)
        self.DATABASE['log'].insert(entry)

    def test_list(self):

        self._insert_data(self.id1, copy(self.sample1))
        self._insert_data(self.id2, copy(self.sample2))
        docs = list(self.model.list())
        self.assertEqual(len(docs), 2)
        self.assertEqual({x[ID]: x[DATA] for x in docs}, self.sampleset)

    def test_get(self):

        self._insert_data(self.id1, copy(self.sample1))
        self._insert_data(self.id2, copy(self.sample2))
        doc1 = self.model.get(self.id1)
        doc2 = self.model.get(self.id2)
        self.assertEqual(doc1[DATA], self.sample1)
        self.assertEqual(doc2[DATA], self.sample2)
        self.assertRaises(exc.DbNotFound,
                          self.model.get, self.get_new_id())

    def test_create(self):

        id1 = self.model.create(data=self.sample1, operator="foo",
                                **self.kwargs)
        id2 = self.model.create(data=self.sample2, operator="bar",
                                **self.kwargs)
        sampleset = {id1: self.sample1, id2: self.sample2}
        docs = list(self.col.find())
        self.assertEqual(len(docs), 2)
        self.assertEqual({x[ID]: x[DATA] for x in docs}, sampleset)
        logs = list(self.DATABASE['log'].find())
        self.assertEqual(len(logs), 2)
        self.assertEqual({x[DOC_ID]: x[DATA] for x in logs}, sampleset)
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
        self.assertEqual({x[ID]: x[DATA] for x in docs}, self.sampleset)
        logs = list(self.DATABASE['log'].find())
        self.assertEqual(len(logs), 2)
        self.assertEqual({x[DOC_ID]: x[DATA] for x in logs}, self.sampleset)
        self.assertEqual(["updated", "updated"],
                         [x[LOG] for x in logs])
        self.assertRaises(exc.DbNotFound,
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
        self._insert_log(self.id1, "created",
                         data=copy(self.sample1))
        self._insert_log(self.id1, "updated",
                         data=copy(self.sample2))
        self._insert_log(self.id1, "deleted")

        logs = list(self.model.get_logs(self.id1))
        self.assertEqual(len(logs), 3)
        self.assertEqual(["created", "updated", "deleted"],
                         [x[LOG] for x in logs])
        self.assertEqual([self.sample1, self.sample2, None],
                         [x.get(DATA) for x in logs])
