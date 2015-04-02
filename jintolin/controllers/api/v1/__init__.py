from pecan.rest import RestController

from jintolin.controllers.api.v1.citype import CiTypeController


class V1ApiController(RestController):

    citype = CiTypeController()
