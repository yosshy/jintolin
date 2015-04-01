# JintoLin
#
# (c)2015  Akira Yoshiyama <akirayoshiyama@gmail.com>

from pecan import conf


DATABASE = None
CI = None
CITYPE = None
LOG = None
PERSON = None


def init_model():
    """
    Initialize database model
    """

    _type = conf.database.get('type')
    params = dict(conf.database.get('params'))

    if _type is None:
        raise Exception("Database configuration")

    if _type == "mongodb":
        from jintolin.model import mongodb
        mongodb.init_model(**params)

        global DATABASE, CI, CITYPE, LOG, PERSON
        DATABASE = mongodb.DATABASE
        CI = mongodb.CI
        CITYPE = mongodb.CITYPE
        PERSON = mongodb.PERSON
        LOG = mongodb.LOG
