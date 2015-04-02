from pecan.rest import RestController

from jintolin.controllers.api.v1 import V1ApiController


class ApiController(RestController):

    v1 = V1ApiController()
