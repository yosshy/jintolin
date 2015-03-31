# Jinto Lin
#
# (c)2015  Akira Yoshiyama <akirayoshiyama@gmail.com>

from jintolin.model.mongodb import base


class PersonModel(base.BaseModel):

    collection = 'person'
