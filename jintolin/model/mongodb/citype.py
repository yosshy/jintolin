# Jinto Lin
#
# (c)2015  Akira Yoshiyama <akirayoshiyama@gmail.com>

from copy import copy
from datetime import datetime

import jsonschema

from jintolin.model.mongodb import base
from jintolin import exception as exc
from jintolin.model.mongodb.const import (
    ID, LINKABLE, TIMESTAMP)


class CiTypeModel(base.BaseModel):

    collection = 'citype'

    def validate(self, data, **kwargs):
        """
        Verifies schema
        """
        try:
            schema = copy(data)
            schema["$schema"] = "http://json-schema.org/schema#"
            jsonschema.Draft4Validator.check_schema(schema)
        except jsonschema.SchemaError as e:
            raise exc.ValidationError()

    def add_linkable(self, id, linkable_id, operator=None):
        """
        Adds linkable_id to LINKABLE list
        """
        doc = self.get(id)
        linkable = doc.get(LINKABLE, [])

        # not allowed to add existing id
        if linkable_id in linkable:
            raise exc.LinkableError()

        self.get(linkable_id)

        # Ok, add linkable_id to LINKABLE list.
        linkable.append(linkable_id)
        doc[TIMESTAMP] = datetime.now()
        doc[LINKABLE] = linkable
        self.col.update({ID: id}, doc)
        self.db.log.create(doc, "add linkable",
                           operator=operator,
                           linkable=linkable)

    def delete_linkable(self, id, linkable_id, operator=None):
        """
        Adds linkable_id to LINKABLE list
        """
        doc = self.get(id)
        linkable = doc.get(LINKABLE, [])

        # not allowed to remove non-existing id
        if linkable_id not in linkable:
            raise exc.LinkableError()

        # Ok, add linkable_id to LINKABLE list.
        linkable.remove(linkable_id)
        doc[TIMESTAMP] = datetime.now()
        doc[LINKABLE] = linkable
        self.col.update({ID: id}, doc)
        self.db.log.create(doc, "delete linkable",
                           operator=operator,
                           linkable=linkable_id)
