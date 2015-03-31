import copy
import unittest
import uuid

from jintolin import model


class TestCase(unittest.TestCase):

    database = {
        'type': 'mongodb',
        'params': {
            'host': 'localhost',
            'database': 'jintolintest'
        }
    }

    @staticmethod
    def get_new_id():
        """
        Returns an new ID.
        """
        return str(uuid.uuid4())

    def setUp(self):
        model.init_model(copy.copy(self.database))
        self.DATABASE = model.DATABASE
        self.CI = model.CI
        self.CITYPE = model.CITYPE
        self.LOG = model.LOG
        self.PERSON = model.PERSON
        self.remove_docs()

    def tearDown(self):
        self.remove_docs()

    def remove_docs(self):
        for i in ['ci', 'citype', 'person', 'log']:
            self.DATABASE[i].remove(multi=True)
