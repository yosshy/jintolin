# Jinto Lin
#
# (c)2015  Akira Yoshiyama <akirayoshiyama@gmail.com>

import jsonschema

from jintolin.model.mongodb import base
from jintolin.model.mongodb.const import (
    ID, CITYPE_ID, DATA, LINK, LINKABLE, TIMESTAMP)
from jintolin import exception as exc


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

    def create(self, data, operator=None, citype_id=None):
        """
        Adds a new entries to DB.
        Returns its ID.
        """
        kwargs = {CITYPE_ID: citype_id}
        return super(CiModel, self).create(data,
                                           operator=operator,
                                           **kwargs)

    def update(self, id, data, operator=None, citype_id=None):
        """
        Updates an entry on DB specified by 'id'.
        """
        kwargs = {CITYPE_ID: citype_id}
        return super(CiModel, self).update(id, data,
                                           operator=operator,
                                           **kwargs)

    def validate(self, data, **kwargs):
        """
        Verifies data with schema specified by 'citype_id'.
        Raises ValidationError if data are invalid.
        """
        citype_id = kwargs.get(CITYPE_ID)
        if citype_id is None:
            raise exc.ValidationError()

        # Get its CI type schema
        citype = self.db.citype.get(citype_id)
        schema = citype[DATA]

        try:
            jsonschema.validate(data, schema)
        except jsonschema.ValidationError as e:
            raise exc.ValidationError()

    def link(self, id, linked_id, operator=None):
        """
        Adds linked_id to doc[LINK] list.
        """
        doc = self.get(id)
        citype_id = doc[CITYPE_ID]
        citype = self.db.citype.get(citype_id)
        link = doc.get(LINK, [])

        # Link not allowd if already linked from local
        if linked_id in link:
            raise exc.LinkError()

        linked_doc = self.get(linked_id)
        linked_citype_id = linked_doc[CITYPE_ID]
        linked_citype = self.db.citype.get(linked_citype_id)
        linked_link = linked_doc.get(LINK, [])

        # Link not allowed if already linked from remote
        if id in linked_link:
            raise exc.LinkError()

        # Link not allowed if both CI type ID doesn't exist
        # at LINKABLE list of the other
        if linked_citype_id not in citype[LINKABLE] and \
           citype_id not in linked_citype[LINKABLE]:
            raise exc.LinkError()

        # Ok, link it
        link.append(linked_id)
        doc[TIMESTAMP] = self.now()
        doc[LINK] = link
        result = self.col.update({ID: id}, doc)
        self.db.log.create(doc, "linked",
                           operator=operator,
                           linked=linked_id)

    def unlink(self, id, linked_id, operator=None):
        """
        Removes linked_id to doc[LINK] list.
        """
        doc = self.get(id)
        data = doc[DATA]
        citype = doc[CITYPE_ID]
        link = doc.get(LINK, [])

        if linked_id in link:
            link.remove(linked_id)
            result = self.col.update({ID: id}, doc)
            self.db.log.create(doc, "unlinked",
                               operator=operator,
                               linked=linked_id)
            return

        linked_doc = self.get(linked_id)
        linked_citype = linked_doc[CITYPE_ID]
        linked_link = linked_doc.get(LINK, [])

        if id in linked_link:
            linked_link.remove(id)
            result = self.col.update({ID: linked_id}, linked_doc)
            self.db.log.create(linked_doc, "unlinked",
                               operator=operator,
                               linked=id)
            return

        # Not linked from both
        raise exc.LinkError()
