from copy import copy
from passlib.hash import sha256_crypt

from jintolin import model
from jintolin.model.mongodb.const import ID, LOG, DATA
from jintolin.tests import FunctionalTest
from .base import TestApiV1BaseController

NAME = u'name'


class TestApiV1PersonController(TestApiV1BaseController, FunctionalTest):

    model_name = "PERSON"
    baseurl = "/api/v1/person/"

    sample1 = {
        u"name": u"account1",
        u"password": u"foo"
    }

    sample2 = {
        u"name": u"account2",
        u"password": u"bar"
    }

    sample3 = {
        u"name": u"account3",
        u"password": u"boo"
    }

    badsample = {
        u"name": u"account1",
        u"password": u""
    }

    def setUp(self):
        super(TestApiV1BaseController, self).setUp()

        self.model = getattr(model, self.model_name)
        self.id1 = self.model.create(copy(self.sample1))
        self.id2 = self.model.create(copy(self.sample2))
        self.sampleset = {
            self.id1: self.sample1[NAME],
            self.id2: self.sample2[NAME]
        }

    def test_get_all(self):
        response = self.app.get(self.baseurl)
        self.assertEqual(response.status_int, 200)
        docs = response.json_body
        self.assertEqual(len(docs), 2)
        self.assertEqual({x[ID]: x[DATA][NAME] for x in docs}, self.sampleset)

    def test_get(self):
        response = self.app.get(self.baseurl + self.id1)
        self.assertEqual(response.status_int, 200)
        doc = response.json_body
        self.assertEqual(doc[ID], self.id1)
        self.assertEqual(doc[DATA][NAME], self.sample1[NAME])

        response = self.app.get(self.baseurl + 'foo', expect_errors=True)
        self.assertEqual(response.status_int, 404)

    def test_post(self):
        response = self.app.post_json(self.baseurl,
                                      copy(self.sample1))
        self.assertEqual(response.status_int, 200)
        doc = response.json_body
        self.assertTrue('id' in doc)

        response = self.app.get(self.baseurl + doc['id'])
        doc = response.json_body
        self.assertEqual(doc[DATA][NAME], self.sample1[NAME])

        response = self.app.post_json(self.baseurl,
                                      copy(self.badsample),
                                      expect_errors=True)
        self.assertEqual(response.status_int, 400)

    def test_put(self):
        response = self.app.put_json(self.baseurl + self.id1,
                                     copy(self.sample3))
        self.assertEqual(response.status_int, 200)

        response = self.app.get(self.baseurl + self.id1)
        doc = response.json_body
        self.assertEqual(doc[DATA][NAME], self.sample3[NAME])

        response = self.app.put_json(self.baseurl + self.id1,
                                     copy(self.badsample),
                                     expect_errors=True)
        self.assertEqual(response.status_int, 400)

        response = self.app.put_json(self.baseurl + 'foo',
                                     self.sample3, expect_errors=True)
        self.assertEqual(response.status_int, 404)

    def test_delete(self):
        response = self.app.delete(self.baseurl + self.id1)
        self.assertEqual(response.status_int, 200)

        response = self.app.get(self.baseurl + self.id1, expect_errors=True)
        self.assertEqual(response.status_int, 404)

        response = self.app.delete(self.baseurl + self.id1, expect_errors=True)
        self.assertEqual(response.status_int, 404)

    def test_get_logs(self):
        response = self.app.post_json(self.baseurl, self.sample1)
        doc = response.json_body
        id = doc['id']
        self.app.put_json(self.baseurl + id, self.sample3)
        self.app.delete(self.baseurl + id)
        response = self.app.get(self.baseurl + '%s/logs' % id)
        self.assertEqual(response.status_int, 200)
        doc = response.json_body
        self.assertEqual([x[LOG] for x in doc],
                         ["created", "updated", "deleted"])

        response = self.app.get(self.baseurl + 'foo/logs',
                                expect_errors=True)
        self.assertEqual(response.status_int, 404)
