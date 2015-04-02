from pecan.core import abort, request
from pecan import expose
from pecan.rest import RestController

from jintolin import exception as exc
from jintolin import model


class CiTypeController(RestController):

    @expose('json')
    def get_all(self):
        return model.CITYPE.list()

    @expose('json')
    def get(self, id, type=None):
        if type == 'log':
            try:
                return model.CITYPE.get_logs(id)
            except exc.DbNotFound:
                abort(404)

        if type is None:
            try:
                return model.CITYPE.get(id)
            except exc.DbNotFound:
                abort(404)

    @expose('json')
    def post(self):
        try:
            data = request.json
            return {'id': model.CITYPE.create(data)}
        except exc.ValidationError:
            abort(400)

    @expose('json')
    def put(self, id):
        try:
            data = request.json
            model.CITYPE.update(id, data)
        except exc.ValidationError:
            abort(400)
        except exc.DbNotFound:
            abort(404)

    @expose('json')
    def delete(self, id):
        try:
            model.CITYPE.delete(id)
        except exc.DbNotFound:
            abort(404)
