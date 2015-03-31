# Jinto Lin
#
# (c)2015  Akira Yoshiyama <akirayoshiyama@gmail.com>

from datetime import datetime
import uuid

import pymongo

from jintolin import exception as exc

ID = u"_id"
DOC_ID = u"did"
LOG = u"l"
TIMESTAMP = u"ts"
OPERATOR = u"op"
DATA = u"data"


class LogModel(object):

    collection = "log"

    def __init__(self, db):
        """
        Initialize a model object.
        """
        self.db = db
        self.col = db[self.collection]
        setattr(self.db, self.collection, self)

    @staticmethod
    def get_new_id():
        """
        Returns an new ID.
        """
        return str(uuid.uuid4())

    def list(self, cond=None):
        """
        Returns a list of entries.
        """
        sort = [(TIMESTAMP, pymongo.ASCENDING)]
        if cond is None:
            cond = {}

        return self.col.find(cond, sort=sort)

    def get(self, id):
        """
        Returns a dict of an entry specified by 'id'.
        """
        doc = self.col.find_one(id)

        if doc is None:
            raise exc.DbNotFound()

        return doc

    def create(self, doc, log, **kwargs):
        """
        Adds a new entries to DB.
        Returns its ID.
        """
        doc = {
            ID: self.get_new_id(),
            DOC_ID: doc[ID],
            TIMESTAMP: doc[TIMESTAMP],
            LOG: log
        }
        doc.update(kwargs)

        self.col.insert(doc)

    def delete(self, cond=None):
        """
        Deletes an entry on DB specified by 'id'.
        """
        if cond is None:
            cond = {}

        self.col.remove(cond)
