# JintoLin
#
# (c)2015  Akira Yoshiyama <akirayoshiyama@gmail.com>


class JintolinException(Exception):
    pass


class DbError(JintolinException):
    pass


class NotFound(DbError):
    pass


class ValidationError(JintolinException):
    pass


class LinkError(DbError):
    pass


class AuthError(JintolinException):
    pass
