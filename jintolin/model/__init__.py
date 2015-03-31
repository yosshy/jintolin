# JintoLin
#
# (c)2015  Akira Yoshiyama <akirayoshiyama@gmail.com>

DATABASE = None
CI = None
CITYPE = None
LOG = None
PERSON = None


def init_model(database):
    """
    Initialize database model

    Params::
    database = {
        'type': 'mongodb',
        'params': {
            'host': 'localhost',
            'database': 'jintolin'
        }
    }
    """

    _type = database.get('type')
    params = dict(database.get('params'))

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
