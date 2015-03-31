# Jinto Lin
#
# (c)2015  Akira Yoshiyama <akirayoshiyama@gmail.com>

import pymongo

from jintolin.model.mongodb import ci, citype, log, person


DATABASE = None
CI = None
CITYPE = None
PERSON = None
LOG = None


def init_model(**config):
    """
    Create database model objects
    """
    global DATABASE, CI, CITYPE, PERSON, LOG

    database = config.pop('database')
    client = pymongo.MongoClient(**config)
    DATABASE = client[database]

    CI = ci.CiModel(DATABASE)
    CITYPE = citype.CiTypeModel(DATABASE)
    PERSON = person.PersonModel(DATABASE)
    LOG = log.LogModel(DATABASE)
