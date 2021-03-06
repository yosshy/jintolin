# Jinto Lin
#
# (c)2015  Akira Yoshiyama <akirayoshiyama@gmail.com>

from pecan.core import abort, request
from pecan import expose
from pecan.rest import RestController

from jintolin import exception as exc
from jintolin import model
from .base import BaseController


ACTION = 'action'
LINKED_ID = 'linked_id'
RELATION = 'relation'


class CiController(BaseController):

    model_name = "CI"

    _custom_actions = {
        'logs': ['GET'],
        'link': ['GET', 'POST']
    }

    @expose('json')
    def get_link(self, id):
        try:
            return self.model.get_linked(id)
        except exc.NotFound:
            abort(404)

    @expose('json')
    def post_link(self, id):
        try:
            data = request.json
            action = data.get(ACTION)
            if action == 'add':
                self.model.link(id, data.get(LINKED_ID), data.get(RELATION))
            elif action == 'delete':
                self.model.unlink(id, data.get(LINKED_ID))
            else:
                abort(400)
        except exc.LinkError:
            abort(400)
        except exc.NotFound:
            abort(404)
