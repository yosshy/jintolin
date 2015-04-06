# Jinto Lin
#
# (c)2015  Akira Yoshiyama <akirayoshiyama@gmail.com>

from pecan.rest import RestController

from .ci import CiController
from .citype import CiTypeController
from .person import PersonController


class V1ApiController(RestController):

    ci = CiController()
    citype = CiTypeController()
    person = PersonController()
