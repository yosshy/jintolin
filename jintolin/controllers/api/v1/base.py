# Jinto Lin
#
# (c)2015  Akira Yoshiyama <akirayoshiyama@gmail.com>

from pecan.core import abort, request
from pecan import expose
from pecan.rest import RestController

from jintolin import exception as exc
from jintolin import model


class BaseController(RestController):

    model_name = None

    _custom_actions = {
        'logs': ['GET']
    }

    @property
    def model(self):
        return getattr(model, self.model_name)

    @expose('json')
    def get_all(self):
        return self.model.list()

    @expose('json')
    def get(self, id):
        try:
            return self.model.get(id)
        except exc.NotFound:
            abort(404)

    @expose('json')
    def post(self):
        try:
            data = request.json
            return {'id': self.model.create(data)}
        except exc.ValidationError:
            abort(400)

    @expose('json')
    def put(self, id):
        try:
            data = request.json
            self.model.update(id, data)
        except exc.ValidationError:
            abort(400)
        except exc.NotFound:
            abort(404)

    @expose('json')
    def delete(self, id):
        try:
            self.model.delete(id)
        except exc.NotFound:
            abort(404)

    @expose('json')
    def logs(self, id):
        try:
            return self.model.get_logs(id)
        except exc.NotFound:
            abort(404)
