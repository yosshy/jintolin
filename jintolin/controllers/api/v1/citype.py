# Jinto Lin
#
# (c)2015  Akira Yoshiyama <akirayoshiyama@gmail.com>

from pecan.core import abort, request
from pecan import expose
from pecan.rest import RestController

from jintolin import exception as exc
from jintolin import model
from .base import BaseController


class CiTypeController(BaseController):

    model_name = "CITYPE"
