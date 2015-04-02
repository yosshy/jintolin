# Jinto Lin
#
# (c)2015  Akira Yoshiyama <akirayoshiyama@gmail.com>

from pecan.rest import RestController

from jintolin.controllers.api.v1.ci import CiController
from jintolin.controllers.api.v1.citype import CiTypeController
from jintolin.controllers.api.v1.person import PersonController


class V1ApiController(RestController):

    ci = CiController()
    citype = CiTypeController()
    person = PersonController()
