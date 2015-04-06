# Jinto Lin
#
# (c)2015  Akira Yoshiyama <akirayoshiyama@gmail.com>

from copy import copy
import jsonschema

from jintolin import exception as exc
from . import base
from .const import (
    ID, CITYPE_ID, DATA, LINK, LINKED_ID, OPERATOR, RELATION, TIMESTAMP)


class CiModel(base.BaseModel):

    collection = 'ci'

    def list(self, citype_id=None):
        """
        Returns a list of CIs.
        """
        cond = {}
        if citype_id is not None:
            cond = {CITYPE_ID: citype_id}

        return super(CiModel, self).list(cond=cond)

    def validate(self, data, **extra_attr):
        """
        Verifies data with schema specified by 'citype_id'.
        Raises ValidationError if data are invalid.
        """
        _data = copy(data)
        citype_id = _data.pop(CITYPE_ID, None)
        if citype_id is None:
            raise exc.ValidationError()

        # Get its CI type schema
        citype = self.db.citype.get(citype_id)
        schema = citype[DATA]

        try:
            jsonschema.validate(_data, schema)
        except jsonschema.ValidationError as e:
            raise exc.ValidationError()

    def get_linked(self, id):
        """
        Retrieve linked CIs
        """
        doc = self.get(id)
        linked_kv = doc.get(LINK, {})
        linked_ids = linked_kv.keys()

        linking_docs = self.col.find({LINK: {"$exists": {id: True}}})
        linked_ids.extend([x[ID] for x in linking_docs])

        linked_ids = list(set(linked_ids))
        if id in linked_ids:
            linked_ids.remove(id)

        linked_docs = list(self.col.find({ID: {"$in": linked_ids}}))
        return linked_docs

    def link(self, id, linked_id, relation, operator=None):
        """
        Adds linked_id to doc[LINK] list.
        """
        # Link not allowd if already linked from local
        if id == linked_id:
            raise exc.LinkError()

        doc = self.get(id)
        link = doc.get(LINK, {})

        # Link not allowd if already linked from local
        if linked_id in link:
            raise exc.LinkError()

        linked_doc = self.get(linked_id)
        linked_link = linked_doc.get(LINK, {})

        # Link not allowed if already linked from remote
        if id in linked_link:
            raise exc.LinkError()

        # Ok, link it
        link[linked_id] = relation
        doc[TIMESTAMP] = self.now()
        doc[LINK] = link
        result = self.col.update({ID: id}, doc)
        self.db.log.create(doc, "linked", **{
            OPERATOR: operator,
            LINKED_ID: linked_id,
            RELATION: relation
        })

    def unlink(self, id, linked_id, operator=None):
        """
        Removes linked_id to doc[LINK] list.
        """
        doc = self.get(id)
        data = doc[DATA]
        link = doc.get(LINK, {})

        if linked_id in link:
            link.pop(linked_id)
            result = self.col.update({ID: id}, doc)
            self.db.log.create(doc, "unlinked", **{
                OPERATOR: operator,
                LINKED_ID: linked_id,
            })
            return

        linked_doc = self.get(linked_id)
        linked_link = linked_doc.get(LINK, {})

        if id in linked_link:
            linked_link.pop(id)
            result = self.col.update({ID: linked_id}, linked_doc)
            self.db.log.create(linked_doc, "unlinked", **{
                OPERATOR: operator,
                LINKED_ID: id,
            })
            return

        # Not linked from both
        raise exc.LinkError()
