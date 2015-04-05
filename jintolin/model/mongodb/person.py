# Jinto Lin
#
# (c)2015  Akira Yoshiyama <akirayoshiyama@gmail.com>

from passlib.hash import sha256_crypt

from jintolin import exception as exc
from jintolin.model.mongodb import base

NAME = 'name'
PASSWORD = 'password'


class PersonModel(base.BaseModel):

    collection = 'person'

    def validate(self, data, **extra_attr):
        """
        Verifies person document
        """
        for i in [NAME, PASSWORD]:
            if i not in data:
                raise exc.ValidationError()
            if not isinstance(data[i], basestring):
                raise exc.ValidationError()
            if len(data[i]) == 0:
                raise exc.ValidationError()

        data[PASSWORD] = sha256_crypt.encrypt(str(data[PASSWORD]))

    def validate_password(self, user, password):
        """
        Verifies password
        """
        doc = self.col.find_one({NAME: user})
        if doc is None:
            raise exc.NotFound()

        return sha256_crypt.verify(password, str(doc[PASSWORD]))
