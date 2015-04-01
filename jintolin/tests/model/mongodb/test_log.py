from datetime import datetime

from jintolin import exception as exc
from jintolin.tests.model.mongodb import base
from jintolin.model.mongodb.const import (
    ID, DOC_ID, TIMESTAMP, LOG, DATA, OPERATOR)


class MongodbLogTestCase(base.TestCase):

    def _insert_data(self, doc_id, log, **kwargs):
        entry = {
            ID: self.get_new_id(),
            TIMESTAMP: datetime.now(),
            DOC_ID: doc_id,
            LOG: log
        }
        entry.update(kwargs)
        self.DATABASE['log'].insert(entry)

    def test_list(self):
        id1 = self.get_new_id()
        id2 = self.get_new_id()
        sample = {'a': 1, 'b': 2}
        self._insert_data(id1, "created", data=sample)
        self._insert_data(id1, "updated")
        self._insert_data(id2, "created", data=sample)
        self._insert_data(id2, "deleted")
        logs = list(self.LOG.list())
        logs1 = list(self.LOG.list({DOC_ID: id1}))
        self.assertEqual(len(logs), 4)
        self.assertEqual(len(logs1), 2)
        self.assertEqual(["created", "updated", "created", "deleted"],
                         [x[LOG] for x in logs])
        self.assertTrue(sample, logs[0][DATA])
        self.assertTrue(DATA not in logs[1])

    def test_get(self):
        id1 = self.get_new_id()
        sample = {'a': 1, 'b': 2}
        self._insert_data(id1, "created", data=sample)
        self._insert_data(id1, "updated")
        logs = list(self.DATABASE['log'].find())
        log1 = self.LOG.get(logs[0][ID])
        log2 = self.LOG.get(logs[1][ID])
        self.assertEqual(log1[DATA], sample)
        self.assertTrue(DATA not in log2)
        self.assertRaises(exc.DbNotFound,
                          self.LOG.get, self.get_new_id())

    def test_create(self):
        id1 = self.get_new_id()
        id2 = self.get_new_id()
        sample = {'a': 1, 'b': 2}
        self.LOG.create({ID: id1, TIMESTAMP: datetime.now()}, "created",
                        data=sample)
        self.LOG.create({ID: id1, TIMESTAMP: datetime.now()}, "updated")
        self.LOG.create({ID: id2, TIMESTAMP: datetime.now()}, "created")
        self.LOG.create({ID: id2, TIMESTAMP: datetime.now()}, "deleted")
        logs = list(self.DATABASE['log'].find())
        logs1 = list(self.DATABASE['log'].find({DOC_ID: id1}))
        self.assertEqual(len(logs), 4)
        self.assertEqual(len(logs1), 2)
        self.assertEqual(set(["created", "updated", "created", "deleted"]),
                         set([x[LOG] for x in logs]))
        self.assertTrue(DATA in logs1[0])
        self.assertEqual(logs1[0][DATA], sample)
        self.assertTrue(DATA not in logs1[1])

    def test_delete(self):
        id1 = self.get_new_id()
        id2 = self.get_new_id()
        sample = {'a': 1, 'b': 2}
        self._insert_data(id1, "created", data=sample)
        self._insert_data(id1, "updated")
        self._insert_data(id2, "created", data=sample)
        self._insert_data(id2, "deleted")
        self.assertEqual(self.DATABASE['log'].count(), 4)
        self.LOG.delete({DOC_ID: id1})
        self.assertEqual(self.DATABASE['log'].count(), 2)
        self.LOG.delete()
        self.assertEqual(self.DATABASE['log'].count(), 0)
