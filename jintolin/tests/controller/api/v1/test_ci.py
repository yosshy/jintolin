from jintolin import model
from jintolin.model.mongodb.const import ID, DATA, CITYPE_ID, LOG, LINK
from jintolin.tests import FunctionalTest
from .base import TestApiV1BaseController


class TestApiV1CiController(TestApiV1BaseController, FunctionalTest):

    model_name = "CI"
    baseurl = "/api/v1/ci/"
    linkurl = "/api/v1/ci/%s/link"

    sample_citype1 = {
        u"type": u"object",
        u"properties": {
            u"name": {u"type": u"string"},
            u"email": {u"type": u"string"},
        },
        u"required": [u"name"]
    }

    sample_citype2 = {
        u"type": u"object",
        u"properties": {
            u"key": {u"type": u"string"},
            u"value": {u"type": u"integer"},
        },
        u"required": [u"key", u"value"]
    }

    sample1 = {
        u"name": u"foo",
        u"email": u"foo@example.com"
    }

    sample2 = {
        u"key": u"bar",
        u"value": 100
    }

    sample3 = {
        u"name": u"woo",
        u"email": u"woo@example.com"
    }

    badsample = {
        u"email": u"woo@example.com"
    }

    def setUp(self):
        super(TestApiV1BaseController, self).setUp()

        self.citype_id1 = model.CITYPE.create(self.sample_citype1)
        self.citype_id2 = model.CITYPE.create(self.sample_citype2)
        self.sample1[CITYPE_ID] = self.citype_id1
        self.sample2[CITYPE_ID] = self.citype_id2
        self.sample3[CITYPE_ID] = self.citype_id1
        self.badsample[CITYPE_ID] = self.citype_id1

        self.model = getattr(model, self.model_name)
        self.id1 = self.model.create(self.sample1)
        self.id2 = self.model.create(self.sample2)
        self.sampleset = {
            self.id1: self.sample1,
            self.id2: self.sample2
        }

    def tearDown(self):
        super(TestApiV1BaseController, self).tearDown()
        for x in self.model.list():
            self.model.delete(x[ID])

        model.CITYPE.delete(self.citype_id1)
        model.CITYPE.delete(self.citype_id2)

    def test_post(self):
        response = self.app.post_json(self.baseurl, self.sample3)
        self.assertEqual(response.status_int, 200)
        doc = response.json_body
        self.assertTrue('id' in doc)

        response = self.app.get(self.baseurl + doc['id'])
        doc = response.json_body
        self.assertEqual(doc[DATA], self.sample3)

        response = self.app.post_json(self.baseurl, self.badsample,
                                      expect_errors=True)
        self.assertEqual(response.status_int, 400)

        self.sample3[CITYPE_ID] = "foo"
        response = self.app.post_json(self.baseurl, self.sample3,
                                      expect_errors=True)
        self.assertEqual(response.status_int, 404)

    def test_put(self):
        response = self.app.put_json(self.baseurl + self.id1, self.sample3)
        self.assertEqual(response.status_int, 200)

        response = self.app.get(self.baseurl + self.id1)
        doc = response.json_body
        self.assertEqual(doc[DATA], self.sample3)

        response = self.app.put_json(self.baseurl + self.id1, self.badsample,
                                     expect_errors=True)
        self.assertEqual(response.status_int, 400)

        response = self.app.put_json(self.baseurl + "foo", self.sample1,
                                     expect_errors=True)
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
                         [u"created", u"updated", u"deleted"])

        response = self.app.get(self.baseurl + 'foo/logs',
                                expect_errors=True)
        self.assertEqual(response.status_int, 404)

    def test_link(self):
        response = self.app.get(
            self.baseurl + self.id1 + "/link")
        self.assertEqual(response.status_int, 200)
        data = response.json
        self.assertEqual(0, len(data))

        data = dict(action='add', linked_id=self.id2, relation='foo')
        response = self.app.post_json(
            self.linkurl % self.id1, data)
        self.assertEqual(response.status_int, 200)

        response = self.app.get(
            self.baseurl + self.id1 + "/link")
        self.assertEqual(response.status_int, 200)
        data = response.json
        self.assertEqual(1, len(data))
        self.assertEqual(self.id2, data[0][ID])
        self.assertEqual(self.sample2, data[0][DATA])

        data = dict(action='add', linked_id=self.id2, relation='foo')
        response = self.app.post_json(
            self.linkurl % self.id1, data, expect_errors=True)
        self.assertEqual(response.status_int, 400)

        data = dict(action='add', linked_id=self.get_new_id(), relation='foo')
        response = self.app.post_json(
            self.linkurl % self.id1, data, expect_errors=True)
        self.assertEqual(response.status_int, 404)

        data = dict(action='delete', linked_id=self.id2)
        response = self.app.post_json(
            self.linkurl % self.id1, data)
        self.assertEqual(response.status_int, 200)

        response = self.app.get(
            self.baseurl + self.id1 + "/link")
        self.assertEqual(response.status_int, 200)
        data = response.json
        self.assertEqual(0, len(data))

        data = dict(action='delete', linked_id=self.id2)
        response = self.app.post_json(
            self.linkurl % self.id1, data, expect_errors=True)
        self.assertEqual(response.status_int, 400)

        response = self.app.get(
            self.baseurl + self.get_new_id() + "/link",
            expect_errors=True)
        self.assertEqual(response.status_int, 404)

        data = dict(action='append', linked_id=self.id2)
        response = self.app.post_json(
            self.linkurl % self.id1, data, expect_errors=True)
        self.assertEqual(response.status_int, 400)

