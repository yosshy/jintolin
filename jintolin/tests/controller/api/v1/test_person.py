from jintolin.tests import FunctionalTest
from jintolin.tests.controller.v1.base import TestApiV1BaseController


class TestApiV1PersonController(TestApiV1BaseController, FunctionalTest):

    model_name = "PERSON"
    baseurl = "/api/v1/person/"

    sample1 = {
        "name": "account1",
        "password": "foo"
    }

    sample2 = {
        "name": "account2",
        "password": "bar"
    }

    sample3 = {
        "name": "account1",
        "password": "boo"
    }

    badsample = {
        "name": "account1",
        "password": ""
    }
