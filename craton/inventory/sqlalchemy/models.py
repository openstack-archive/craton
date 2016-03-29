"""Models defined using SQLAlchemy ORM"""

from oslo_config import cfg
from oslo_db.sqlalchemy import models
from sqlalchemy import (
    Boolean, Column, ForeignKey, Integer, String, Table, Text,
    UniqueConstraint)
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref, object_mapper, relationship 
from sqlalchemy.orm.collections import attribute_mapped_collection
from sqlalchemy_utils import Timestamp
from sqlalchemy_utils.types.encrypted import EncryptedType
from sqlalchemy_utils.types.ip_address import IPAddressType
from sqlalchemy_utils.types.json import JSONType
from sqlalchemy_utils.types.url import URLType
from sqlalchemy_utils.types.uuid import UUIDType
import six.moves.urllib.parse as urlparse


# FIXME set up table args for a given database/storage engine, as configured.
# See https://github.com/rackerlabs/craton/issues/19


# Implementation is from the example code in
# http://docs.sqlalchemy.org/en/latest/_modules/examples/vertical/dictlike.html
# also see related support in HostVariable, Host
class ProxiedDictMixin(object):
    """Adds obj[key] access to a mapped class.

    This class basically proxies dictionary access to an attribute
    called ``_proxied``.  The class which inherits this class
    should have an attribute called ``_proxied`` which points to a dictionary.
    """

    def __len__(self):
        return len(self._proxied)

    def __iter__(self):
        return iter(self._proxied)

    def __getitem__(self, key):
        return self._proxied[key]

    def __contains__(self, key):
        return key in self._proxied

    def __setitem__(self, key, value):
        self._proxied[key] = value

    def __delitem__(self, key):
        del self._proxied[key]


class CratonBase(models.ModelBase, Timestamp):
    def __repr__(self):
        mapper = object_mapper(self)
        cols = getattr(self, '_repr_columns',  mapper.primary_key)
        items = [(p.key, getattr(self, p.key))
                 for p in [
                     mapper.get_property_by_column(c) for c in cols]]
        return "{0}({1})".format(
            self.__class__.__name__,
            ', '.join(['{0}={1!r}'.format(*item) for item in items]))


Base = declarative_base(cls=CratonBase)


class Tenant(Base):
    """Supports multitenancy for all other schema elements."""
    __tablename__ = 'tenants'
    id = Column(UUIDType, primary_key=True)
    name = Column(String(255))
    # TODO we will surely need to define more columns, but this
    # suffices to define multitenancy for MVP

    hosts = relationship('Host', back_populates='tenant')
    groups = relationship('Group', back_populates='tenant')


# FIXME there are stricter requirements for key names in Ansible (see
# http://docs.ansible.com/ansible/playbooks_variables.html#what-makes-a-valid-variable-name),
# and it is not clear what the encoding requirements are for values.
# We may want to represent these requirements with subclassing on
# HostVariables.

class HostVariables(Base):
    """Represents specific key/value bindings for a given host."""
    __tablename__ = 'host_variables'
    host_id = Column(ForeignKey('hosts.id'), primary_key=True)
    key = Column(String(255), primary_key=True)
    value = Column(Text)
    _repr_columns = [value]


host_grouping = Table(
    'host_grouping', Base.metadata,
    Column('host_id', ForeignKey('hosts.id'), primary_key=True),
    Column('group_id', ForeignKey('groups.id'), primary_key=True))
                      

# TODO consider using SqlAlchemy's support for inheritance
# hierarchies, eg ComputeHost < Host but first need to determine what
# is uniquely required for a ComputeHost; otherwise use an enumerated
# type to distinguish
#
# see http://docs.sqlalchemy.org/en/latest/orm/inheritance.html#single-table-inheritance

class Host(ProxiedDictMixin, Base):
    """Models descriptive data about a host, including discovered facts"""
    __tablename__ = 'hosts'
    id = Column(UUIDType, primary_key=True)
    tenant_id = Column(
        UUIDType, ForeignKey('tenants.id'), index=True, nullable=False)
    secret_id = Column(UUIDType, ForeignKey('secrets.id'))
    hostname = Column(String(255), nullable=False)
    ip_address = Column(IPAddressType, nullable=False)
    active = Column(Boolean, default=True)  # may or may not be reachable
    facts = Column(JSONType)  # discovered facts about the host

    UniqueConstraint(tenant_id, hostname)
    UniqueConstraint(tenant_id, ip_address)

    _repr_columns=[id, hostname]

    groups = relationship(
        'Group',
        secondary=host_grouping,
        back_populates='hosts')

    # many-to-one relationship with tenants
    tenant = relationship('Tenant', back_populates='hosts')

    # optional many-to-one relationship with secrets; don't care about
    # the backref
    secret = relationship('Secret')

    # provide arbitrary K/V mapping to associated HostVariables table
    variables = relationship(
        'HostVariables',
        collection_class=attribute_mapped_collection('key'))

    # allows access to a host object using dict ops - get/set/del -
    # using [] indexing
    _proxied = association_proxy(
        'variables', 'value',
        creator=lambda key, value: HostVariables(key=key, value=value))

    @classmethod
    def with_characteristic(self, key, value):
        return self.variables.any(key=key, value=value)


class Group(Base):
    """Models a grouping of hosts.

    This includes the following groupings:
    
    * Ansible groups
    * OpenStack regions and cells

    Groups use an adjacency list representation, with possibly some
    children referring to a given parent.
    """
    __tablename__ = 'groups'
    id = Column(UUIDType, primary_key=True)
    tenant_id = Column(
        UUIDType, ForeignKey('tenants.id'), index=True, nullable=False)
    parent_id = Column(UUIDType, ForeignKey('groups.id'))
    name = Column(String(255))
    # Our assumption is any config yaml file that needs some sort of
    # include/overlay mechanism will use Ansible includes/roles; or
    # perhaps something similar for YAML include in general.  So this
    # means we need just one reference.
    #
    # NOTE but we likely need some sort of resolution scheme to handle
    # branches, etc.
    config = Column(URLType)

    UniqueConstraint(tenant_id, name)

    _repr_columns = [id, name]

    # self relationship, supporting adjacency list representation
    children = relationship(
        'Group',
        backref=backref('parent', remote_side=[id]))

    # many-to-many relationship with hosts
    hosts = relationship(
        'Host',
        secondary=host_grouping,
        back_populates='groups')

    # many-to-one relationship with tenants
    tenant = relationship('Tenant', back_populates='groups')


# TODO we may want to subclass types of secrets

# TODO should determine integration with systems like Barbican that
# can provide additional secret data to decrypt encrypted certs -
# which is presumably what we should be storing. See
# https://github.com/rackerlabs/craton/issues/7

class Secret(Base):
    """Represents a secret for accessing a host. It may be shared.

    For now we assume a PEM-encoded certificate that represents the
    private key.
    """
    __tablename__ = 'secrets'
    id = Column(UUIDType, primary_key=True)
    cert = Column(Text)
