import unittest
import uuid

from jintolin.tests import FunctionalTest

from jintolin import model


class TestCase(FunctionalTest):

    @staticmethod
    def get_new_id():
        """
        Returns an new ID.
        """
        return str(uuid.uuid4())

    def setUp(self):
        super(TestCase, self).setUp()
        self.DATABASE = model.DATABASE
        self.CI = model.CI
        self.CITYPE = model.CITYPE
        self.LOG = model.LOG
        self.PERSON = model.PERSON
        self.remove_docs()

    def tearDown(self):
        self.remove_docs()
        super(TestCase, self).tearDown()

    def remove_docs(self):
        for i in ['ci', 'citype', 'person', 'log']:
            self.DATABASE[i].remove(multi=True)
