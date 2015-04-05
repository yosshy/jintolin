from copy import copy

from jintolin import exception as exc
from jintolin import model
from jintolin.model.mongodb.const import ID, DATA, LOG


class TestApiV1BaseController(object):

    sample1 = None
    sample2 = None
    sample3 = None
    badsample = None
    model_name = None
    baseurl = None

    def setUp(self):
        super(TestApiV1BaseController, self).setUp()

        self.model = getattr(model, self.model_name)
        self.id1 = self.model.create(copy(self.sample1))
        self.id2 = self.model.create(copy(self.sample2))
        self.sampleset = {
            self.id1: self.sample1,
            self.id2: self.sample2
        }

    def tearDown(self):
        super(TestApiV1BaseController, self).tearDown()
        for x in self.model.list():
            self.model.delete(x[ID])

    def test_get_all(self):
        response = self.app.get(self.baseurl)
        self.assertEqual(response.status_int, 200)
        docs = response.json_body
        self.assertEqual(len(docs), 2)
        self.assertEqual({x[ID]: x[DATA] for x in docs}, self.sampleset)

    def test_get(self):
        response = self.app.get(self.baseurl + self.id1)
        self.assertEqual(response.status_int, 200)
        doc = response.json_body
        self.assertEqual(doc[ID], self.id1)
        self.assertEqual(doc[DATA], self.sample1)

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
        self.assertEqual(doc[DATA], self.sample1)

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
        self.assertEqual(doc[DATA], self.sample3)

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
