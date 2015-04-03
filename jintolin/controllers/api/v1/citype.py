# Jinto Lin
#
# (c)2015  Akira Yoshiyama <akirayoshiyama@gmail.com>

from pecan.core import abort, request
from pecan import expose
from pecan.rest import RestController

from jintolin import exception as exc
from jintolin import model
from jintolin.controllers.api.v1.base import BaseController


class CiTypeLinkableController(RestController):

    @expose('json')
    def post(self, id, linkable_id):
        try:
            model.CITYPE.add_linkable(id, linkable_id)
        except exc.LinkableError:
            abort(400)

    @expose('json')
    def delete(self, id, linkable_id):
        try:
            model.CITYPE.delete_linkable(id, linkable_id)
        except exc.LinkableError:
            abort(400)


class CiTypeController(BaseController):

    model_name = "CITYPE"

    linkable = CiTypeLinkableController()
