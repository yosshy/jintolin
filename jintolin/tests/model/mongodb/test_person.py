from datetime import datetime
from unittest import TestCase

from jintolin.tests.model.mongodb import base
from jintolin.tests.model.mongodb import model_base

ID = u'_id'
DOC_ID = u'did'
TIMESTAMP = u'ts'
LOG = u'l'
DATA = u'data'
OPERATOR = u'o'


class MongodbPersonModelTestCase(model_base.MongodbBaseModelTestCase,
        base.TestCase):

    model_attr = "PERSON"
    collection = "person"

    sample1 = {
        "name": "hoge",
        "password": "fuga"
    }

    sample2 = {
        "name": "foo",
        "password": "bar"
    }
