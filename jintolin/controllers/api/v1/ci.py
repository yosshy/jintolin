# Jinto Lin
#
# (c)2015  Akira Yoshiyama <akirayoshiyama@gmail.com>

from pecan.core import abort, request
from pecan import expose
from pecan.rest import RestController

from jintolin.controllers.api.v1.base import BaseController
from jintolin import exception as exc
from jintolin import model


class CiController(BaseController):

    model_name = "CI"

    @expose('json')
    def post(self, citype_id=None):
        try:
            data = request.json
            return {'id': self.model.create(data, citype_id=citype_id)}
        except exc.ValidationError:
            abort(400)
        except exc.NotFound:
            abort(404)

    @expose('json')
    def put(self, id, citype_id=None):
        try:
            data = request.json
            self.model.update(id, data, citype_id=citype_id)
        except exc.ValidationError:
            abort(400)
        except exc.NotFound:
            abort(404)
