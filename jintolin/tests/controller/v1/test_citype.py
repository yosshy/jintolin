from jintolin.tests import FunctionalTest
from jintolin.tests.controller.v1.base import TestApiV1BaseController


class TestApiV1CitypeController(TestApiV1BaseController, FunctionalTest):

    model_name = "CITYPE"
    baseurl = "/api/v1/citype/"
    linkableurl = "/api/v1/citype/linkable/%s/%s"

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

    def test_add_linkable(self):
        response = self.app.post(
            self.linkableurl % (self.id1, self.id2))
        self.assertEqual(response.status_int, 200)

        response = self.app.post(
            self.linkableurl % (self.id1, self.id2), expect_errors=True)
        self.assertEqual(response.status_int, 400)

    def test_delete_linkable(self):
        self.app.post(self.linkableurl % (self.id1, self.id2))

        response = self.app.delete(
            self.linkableurl % (self.id1, self.id2))
        self.assertEqual(response.status_int, 200)

        response = self.app.delete(
            self.linkableurl % (self.id1, self.id2), expect_errors=True)
        self.assertEqual(response.status_int, 400)
