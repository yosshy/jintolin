# Jinto Lin
#
# (c)2015  Akira Yoshiyama <akirayoshiyama@gmail.com>

from pecan import expose, redirect
from webob.exc import status_map

from jintolin.controllers.api import ApiController


class RootController(object):

    api = ApiController()
