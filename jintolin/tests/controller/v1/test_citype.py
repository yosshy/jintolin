from unittest import TestCase
from webtest import TestApp

from jintolin import exception as exc
from jintolin import model
from jintolin.model.mongodb.const import ID, DATA, LOG

from jintolin.tests import FunctionalTest


class TestApiV1CitypeController(FunctionalTest):

    sample1 = {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "email": {"type": "string"},
        },
        "required": ["name"]
    }

    sample2 = {
        "type": "object",
        "properties": {
            "key": {"type": "string"},
            "value": {"type": "integer"},
        },
        "required": ["key", "value"]
    }

    sample3 = {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "email": {"type": "string"},
            "age": {"type": "integer"},
        },
        "required": ["name"]
    }

    badsample = {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "email": {"type": "email"},
        },
        "required": ["name"]
    }

    def setUp(self):
        super(TestApiV1CitypeController, self).setUp()
        self.id1 = model.CITYPE.create(self.sample1)
        self.id2 = model.CITYPE.create(self.sample2)
        self.sampleset = {
            self.id1: self.sample1,
            self.id2: self.sample2
        }

    def tearDown(self):
        super(TestApiV1CitypeController, self).tearDown()
        for x in model.CITYPE.list():
            model.CITYPE.delete(x[ID])

    def test_get_all(self):
        response = self.app.get('/api/v1/citype/')
        self.assertEqual(response.status_int, 200)
        docs = response.json_body
        self.assertEqual(len(docs), 2)
        self.assertEqual({x[ID]: x[DATA] for x in docs}, self.sampleset)

    def test_get(self):
        response = self.app.get('/api/v1/citype/' + self.id1)
        self.assertEqual(response.status_int, 200)
        doc = response.json_body
        self.assertEqual(doc[ID], self.id1)
        self.assertEqual(doc[DATA], self.sample1)

        response = self.app.get('/api/v1/citype/foo',  expect_errors=True)
        self.assertEqual(response.status_int, 404)

    def test_post(self):
        response = self.app.post_json('/api/v1/citype/', self.sample1)
        self.assertEqual(response.status_int, 200)
        doc = response.json_body
        self.assertTrue('id' in doc)

        response = self.app.get('/api/v1/citype/' + doc['id'])
        doc = response.json_body
        self.assertEqual(doc[DATA], self.sample1)

        response = self.app.post_json('/api/v1/citype/', self.badsample,
                                      expect_errors=True)
        self.assertEqual(response.status_int, 400)

    def test_put(self):
        response = self.app.put_json('/api/v1/citype/' + self.id1,
                                     self.sample3)
        self.assertEqual(response.status_int, 200)

        response = self.app.get('/api/v1/citype/' + self.id1)
        doc = response.json_body
        self.assertEqual(doc[DATA], self.sample3)

        response = self.app.put_json('/api/v1/citype/' + self.id1,
                                     self.badsample, expect_errors=True)
        self.assertEqual(response.status_int, 400)

        response = self.app.put_json('/api/v1/citype/foo',
                                     self.sample3, expect_errors=True)
        self.assertEqual(response.status_int, 404)

    def test_delete(self):
        response = self.app.delete('/api/v1/citype/' + self.id1)
        self.assertEqual(response.status_int, 200)

        response = self.app.get('/api/v1/citype/' + self.id1,
                                expect_errors=True)
        self.assertEqual(response.status_int, 404)

        response = self.app.delete('/api/v1/citype/' + self.id1,
                                   expect_errors=True)
        self.assertEqual(response.status_int, 404)

    def test_get_logs(self):
        response = self.app.post_json('/api/v1/citype/', self.sample1)
        doc = response.json_body
        id = doc['id']
        self.app.put_json('/api/v1/citype/' + id, self.sample3)
        self.app.delete('/api/v1/citype/' + id)
        response = self.app.get('/api/v1/citype/%s?type=log' % id)
        self.assertEqual(response.status_int, 200)
        doc = response.json_body
        self.assertEqual([x[LOG] for x in doc],
                         ["created", "updated", "deleted"])

        response = self.app.get('/api/v1/citype/foo?type=log',
                                expect_errors=True)
        self.assertEqual(response.status_int, 404)
