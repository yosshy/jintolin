# Jinto Lin
#
# (c)2015  Akira Yoshiyama <akirayoshiyama@gmail.com>

from datetime import datetime
import uuid

import pymongo

from jintolin import exception as exc
from .const import ID, DOC_ID, DATA, OPERATOR, TIMESTAMP


class BaseModel(object):

    collection = ""

    def __init__(self, db):
        """
        Initialize a model object.
        """
        self.db = db
        self.col = db[self.collection]
        setattr(self.db, self.collection, self)

    @staticmethod
    def now():
        """
        Returns an new ID.
        """
        return datetime.now()

    @staticmethod
    def get_new_id():
        """
        Returns an new ID.
        """
        return str(uuid.uuid4())

    def list(self, cond=None):
        """ Returns a list of entries.
        """
        if cond is None:
            cond = {}

        return list(self.col.find(cond))

    def get(self, id):
        """
        Returns a dict of an entry specified by 'id'.
        """
        data = self.col.find_one({ID: id})
        if data is None:
            raise exc.NotFound()

        return data

    def validate(self, data, **extra_attr):
        """
        Verifies data
        """
        pass

    def create(self, data, operator=None, **extra_attr):
        """
        Adds a new entries to DB.
        Returns its ID.
        """
        # Verify data
        self.validate(data, **extra_attr)

        # Create a new entries
        id = self.get_new_id()
        doc = {
            ID: id,
            TIMESTAMP: self.now(),
            DATA: data
        }
        doc.update(extra_attr)
        self.col.insert(doc)
        self.db.log.create(doc, "created", **{OPERATOR: operator, DATA: data})
        # Return ID
        return id

    def update(self, id, data, operator=None, **extra_attr):
        """
        Updates an entry on DB specified by 'id'.
        """
        # Check document exists
        self.get(id)

        # Verify data
        self.validate(data, **extra_attr)

        # Overwrite attributes
        doc = {
            ID: id,
            TIMESTAMP: self.now(),
            DATA: data
        }
        doc.update(extra_attr)
        result = self.col.update({ID: id}, doc)
        self.db.log.create(doc, "updated", **{OPERATOR: operator, DATA: data})

    def delete(self, id, operator=None):
        """
        Deletes an entry on DB specified by 'id'.
        """
        # Check document exists
        self.get(id)

        # delete doc
        doc = {
            ID: id,
            TIMESTAMP: self.now(),
        }
        self.col.remove(id)
        self.db.log.create(doc, "deleted", **{OPERATOR: operator})

    def get_logs(self, id, cond=None):
        """
        Returns a dict list of an entry specified by 'id'.
        """
        if not isinstance(cond, dict):
            cond = {}
        cond[DOC_ID] = id

        logs = list(self.db.log.list(cond=cond))
        if len(logs) == 0:
            raise exc.NotFound()
        return logs
