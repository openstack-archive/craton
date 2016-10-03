"""Exceptions for Craton Inventory system."""


class Base(Exception):
    """Base Exception for Craton Inventory."""
    code = 500
    message = "An unknown exception occurred"

    def __str__(self):
        return self.message

    def __init__(self, code=None, message=None):
        if code:
            self.code = code

        if message:
            self.message = message

        super(Base, self).__init__(
            '%s: %s' % (self.code, self.message))


class AdminRequired(Base):
    code = 401
    message = "This action requires the 'admin' role"


class BadRequest(Base):
    code = 400


class NotFound(Base):
    code = 404
    message = "Not Found"


class UnknownException(Base):
    code = 500
