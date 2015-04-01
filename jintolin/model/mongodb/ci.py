# Jinto Lin
#
# (c)2015  Akira Yoshiyama <akirayoshiyama@gmail.com>

import jsonschema

from jintolin.model.mongodb import base
from jintolin.model.mongodb.const import CITYPE_ID, DATA
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

    def validate(self, data, citype_id=None):
        """
        Verifies data with schema specified by 'citype_id'.
        Raises ValidationError if data are invalid.
        """
        if citype_id is None:
            raise exc.ValidationError()

        # Get its CI type schema
        citype = self.db.citype.get(citype_id)
        schema = citype[DATA]

        try:
            jsonschema.validate(data, schema)
        except jsonschema.ValidationError as e:
            raise exc.ValidationError()
