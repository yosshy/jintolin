from jintolin.tests import FunctionalTest
from jintolin.tests.controller.v1.base import TestApiV1BaseController


class TestApiV1CitypeController(TestApiV1BaseController, FunctionalTest):

    modelname = "CITYPE"
    baseurl = "/api/v1/citype/"

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
