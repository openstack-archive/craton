"""Models defined using SQLAlchemy ORM"""

from oslo_config import cfg
from oslo_db.sqlalchemy import models
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table, Text
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


# FIXME set table_args for mysql?


# From http://docs.sqlalchemy.org/en/latest/_modules/examples/vertical/dictlike.html
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
    """Cloud tenant"""
    __tablename__ = 'tenants'
    id = Column(UUIDType, primary_key=True)
    name = Column(String(255))
    # FIXME probably need more columns in this schema, but suffices
    # for initial multitenancy for now...


# Note that for host variables key/value pairs, we assume bytestring, not Unicode
class HostVariables(Base):
    __tablename__ = 'host_variables'
    host_id = Column(ForeignKey('hosts.id'), primary_key=True)
    key = Column(String(255), primary_key=True)
    value = Column(Text)
    _repr_columns = [value]


host_grouping = Table(
    'host_grouping', Base.metadata,
    Column('host_id', ForeignKey('hosts.id'), primary_key=True),
    Column('group_id', ForeignKey('groups.id'), primary_key=True))
                      

# FIXME use SqlAlchemy's support for inheritance hierarchies, eg ComputeHost < Host
# For Sulo's type, compute - what are the actual column types?
# most likely it makes sense to use single table inheritance;
# see http://docs.sqlalchemy.org/en/latest/orm/inheritance.html#single-table-inheritance

class Host(ProxiedDictMixin, Base):
    """Models descriptive data about a host. Does not model its current state."""
    __tablename__ = 'hosts'
    id = Column(UUIDType, primary_key=True)
    tenant_id = Column(UUIDType, ForeignKey('tenants.id'), index=True, nullable=False)
    hostname = Column(String(255), nullable=False, unique=True)
    ip_address = Column(IPAddressType, nullable=False, unique=True)
    active = Column(Boolean)
    discovered = Column(JSONType)
    _repr_columns=[id, hostname]

    groups = relationship(
        'Group',
        secondary=host_grouping,
        back_populates='hosts')

    # provide arbitrary K/V mapping to associated HostVariables table
    variables = relationship(
        'HostVariables',
        collection_class=attribute_mapped_collection('key'))

    # allows access to a host object using dict ops - get/set/del - using [] indexing
    _proxied = association_proxy(
        'variables', 'value',
        creator=lambda key, value: HostVariables(key=key, value=value))

    @classmethod
    def with_characteristic(self, key, value):
        return self.variables.any(key=key, value=value)


class Group(Base):
    """Models a grouping of hosts: Ansible groups, OpenStack regions and cells"""
    __tablename__ = 'groups'
    id = Column(UUIDType, primary_key=True)
    parent_id = Column(UUIDType, ForeignKey('groups.id'))
    name = Column(String(255))

    # Our assumption is any config yaml file that needs some sort of include/overlay mechanism
    # will use Ansible includes/roles; or perhaps something similar for YAML include in general.
    # So this means we need just one reference.
    # NOTE we likely need some sort of resolution scheme to handle branches, etc.
    config = Column(URLType)

    _repr_columns = [id, name]

    # self relationship, supporting adjacency list representation
    children = relationship(
        "Group",
        backref=backref('parent', remote_side=[id]))

    # many-to-many relationship with hosts
    hosts = relationship(
        'Host',
        secondary=host_grouping,
        back_populates='groups')
