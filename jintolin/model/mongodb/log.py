# Jinto Lin
#
# (c)2015  Akira Yoshiyama <akirayoshiyama@gmail.com>

import uuid

import pymongo

from jintolin import exception as exc
from jintolin.model.mongodb.const import (
    ID, DOC_ID, LOG, TIMESTAMP, OPERATOR, DATA)


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
            raise exc.NotFound()

        return doc

    def create(self, doc, log, **kwargs):
        """
        Adds a new entries to DB.
        Returns its ID.
        """
        log_doc = {
            ID: self.get_new_id(),
            DOC_ID: doc[ID],
            TIMESTAMP: doc[TIMESTAMP],
            LOG: log
        }
        log_doc.update(kwargs)

        self.col.insert(log_doc)

    def delete(self, cond=None):
        """
        Deletes an entry on DB specified by 'id'.
        """
        if cond is None:
            cond = {}

        self.col.remove(cond)
