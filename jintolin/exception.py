# JintoLin
#
# (c)2015  Akira Yoshiyama <akirayoshiyama@gmail.com>


class JintolinException(Exception):
    pass


class DbError(JintolinException):
    pass


class DbNotFound(DbError):
    pass


class ValidationError(JintolinException):
    pass


class LinkError(DbError):
    pass


class LinkableError(DbError):
    pass
