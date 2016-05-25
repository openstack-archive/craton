"""Custom SQLAlchemy types for craton inventory."""

import netaddr
import six
from sqlalchemy import types


# TODO(sulo): get rid of this once we have
# ipaddress supported by oslo.serialization.


class IPAddressType(types.TypeDecorator):

    impl = types.String(64)

    def process_result_value(self, value, dialect):
        return netaddr.IPAddress(value) if value else None

    def process_bind_param(self, value, dialect):
        return six.text_type(value) if value else None
