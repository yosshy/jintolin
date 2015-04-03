# Jinto Lin
#
# (c)2015  Akira Yoshiyama <akirayoshiyama@gmail.com>

from jintolin import exception as exc
from jintolin.model.mongodb import base


class PersonModel(base.BaseModel):

    collection = 'person'

    def validate(self, data, **kwargs):
        """
        Verifies person
        """
        for i in ["name", "password"]:
            if i not in data:
                raise exc.ValidationError()
            if not isinstance(data[i], basestring):
                raise exc.ValidationError()
            if len(data[i]) == 0:
                raise exc.ValidationError()
