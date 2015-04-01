from datetime import datetime
from unittest import TestCase

from jintolin.tests.model.mongodb import base
from jintolin.tests.model.mongodb import model_base
from jintolin.model.mongodb.const import (
    ID, DOC_ID, TIMESTAMP, LOG, DATA, OPERATOR)


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
