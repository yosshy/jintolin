import copy
from datetime import datetime

from jintolin import exception as exc

ID = u'_id'
DOC_ID = u'did'
TIMESTAMP = u'ts'
LOG = u'l'
DATA = u'data'
OPERATOR = u'o'

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

        self._insert_data(self.id1, copy.copy(self.sample1))
        self._insert_data(self.id2, copy.copy(self.sample2))
        docs = list(self.model.list())
        self.assertEqual(len(docs), 2)
        self.assertEqual(self.sample1, docs[0][DATA])
        self.assertEqual(self.sample2, docs[1][DATA])

    def test_get(self):

        self._insert_data(self.id1, copy.copy(self.sample1))
        self._insert_data(self.id2, copy.copy(self.sample2))
        docs = list(self.col.find())
        doc1 = self.model.get(docs[0][ID])
        doc2 = self.model.get(docs[1][ID])
        self.assertEqual(self.sample1, doc1[DATA])
        self.assertEqual(self.sample2, doc2[DATA])
        self.assertRaises(exc.DbNotFound,
                          self.model.get, self.get_new_id())

    def test_create(self):

        id1 = self.model.create(data=self.sample1, operator="foo",
                                **self.kwargs)
        id2 = self.model.create(data=self.sample2, operator="bar",
                                **self.kwargs)
        docs = list(self.col.find())
        self.assertEqual(len(docs), 2)
        self.assertTrue(self.sample1, docs[0][DATA])
        self.assertTrue(self.sample2, docs[1][DATA])
        logs = list(self.DATABASE['log'].find())
        self.assertEqual(len(logs), 2)
        self.assertEqual([id1, id2],
                         [x[DOC_ID] for x in logs])
        self.assertEqual([self.sample1, self.sample2],
                         [x[DATA] for x in logs])
        self.assertEqual(["created", "created"],
                         [x[LOG] for x in logs])

    def test_update(self):

        self._insert_data(self.id1, copy.copy(self.sample2))
        self._insert_data(self.id2, copy.copy(self.sample1))
        self.model.update(self.id1, data=copy.copy(self.sample1),
                          operator="foo", **self.kwargs)
        self.model.update(self.id2, data=copy.copy(self.sample2),
                          operator="bar", **self.kwargs)
        docs = list(self.col.find())
        self.assertEqual(len(docs), 2)
        self.assertTrue(self.sample1, docs[0][DATA])
        self.assertTrue(self.sample2, docs[1][DATA])
        logs = list(self.DATABASE['log'].find())
        self.assertEqual(len(logs), 2)
        self.assertEqual([self.id1, self.id2],
                         [x[DOC_ID] for x in logs])
        self.assertEqual([self.sample1, self.sample2],
                         [x[DATA] for x in logs])
        self.assertEqual(["updated", "updated"],
                         [x[LOG] for x in logs])

    def test_delete(self):

        self._insert_data(self.id1, copy.copy(self.sample1))
        self._insert_data(self.id2, copy.copy(self.sample2))
        docs = list(self.col.find())
        self.assertEqual(2, self.col.count())
        doc1 = self.model.delete(self.id1)
        doc2 = self.model.delete(self.id2)
        self.assertEqual(0, self.col.count())
        logs = list(self.DATABASE['log'].find())
        self.assertEqual(len(logs), 2)
        self.assertEqual([self.id1, self.id2],
                         [x[DOC_ID] for x in logs])
        self.assertEqual(["deleted", "deleted"],
                         [x[LOG] for x in logs])

    def test_get_logs(self):
        self._insert_log(self.id1, "created",
                         data=copy.copy(self.sample1))
        self._insert_log(self.id1, "updated",
                         data=copy.copy(self.sample2))
        self._insert_log(self.id1, "deleted")

        logs = list(self.model.get_logs(self.id1))
        self.assertEqual(len(logs), 3)
        self.assertEqual(["created", "updated", "deleted"],
                         [x[LOG] for x in logs])
        self.assertEqual([self.sample1, self.sample2, None],
                         [x.get(DATA) for x in logs])
