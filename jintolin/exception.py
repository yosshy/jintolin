# JintoLin
#
# (c)2015  Akira Yoshiyama <akirayoshiyama@gmail.com>


class DbError(Exception):
    pass


class DbNotFound(DbError):
    pass


class ValidationError(Exception):
    pass
