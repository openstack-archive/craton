"""Exceptions for Craton Inventory system."""
from oslo_log import log as logging


LOG = logging.getLogger(__name__)


class Base(Exception):
    """Base Exception for Craton Inventory."""
    code = 500
    message = "An unknown exception occurred"

    def __str__(self):
        return self.message

    def __init__(self, code=None, message=None, **kwargs):
        if code:
            self.code = code

        if not message:
            try:
                message = self.msg % kwargs
            except Exception:
                LOG.exception('Error in formatting exception message')
                message = self.msg

        self.message = message

        super(Base, self).__init__(
            '%s: %s' % (self.code, self.message))


class DuplicateRegion(Base):
    code = 409
    msg = "A region with the given name already exists."


class DuplicateCell(Base):
    code = 409
    msg = "A cell with the given name already exists."


class DuplicateDevice(Base):
    code = 409
    msg = "A device with the given name already exists."


class DuplicateNetwork(Base):
    code = 409
    msg = "Network with the given name already exists in this region."


class NetworkNotFound(Base):
    code = 404
    msg = "Network not found for ID %(id)s."


class DeviceNotFound(Base):
    code = 404
    msg = "%(device_type)s device not found for ID %(id)s."


class AdminRequired(Base):
    code = 401
    msg = "This action requires the 'admin' role"


class BadRequest(Base):
    code = 400


class NotFound(Base):
    code = 404
    msg = "Not Found"


class UnknownException(Base):
    code = 500
