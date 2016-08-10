"""Models inventory, as defined using SQLAlchemy ORM
There are three independent parts to a specific workflow execution:
* configuration, as managed by a GitHub-like versioned set of config
  files (as used by Ansible and similar systems)
* specific workflow, which is written in Python (eg with TaskFlow)
* inventory of hosts for a given project, as organized by region, cell,
  and labels, with overrides on variables; this module models that for
  SQLAlchemy
In particular, this means that the configuration is used to interpret
any inventory data.
"""

try:
    from collections import ChainMap
except ImportError:
    # else get the backport of this Python 3 functionality
    from chainmap import ChainMap
from operator import attrgetter

from oslo_db.sqlalchemy import models
from sortedcontainers import SortedSet
from sqlalchemy import (
    Boolean, Column, ForeignKey, Integer, String, Table, Text,
    UniqueConstraint)
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import object_mapper, relationship
from sqlalchemy.orm.collections import attribute_mapped_collection
from sqlalchemy_utils.types.ip_address import IPAddressType
from sqlalchemy_utils.types.json import JSONType


# TODO(jimbaker) set up table args for a given database/storage
# engine, as configured.  See
# https://github.com/rackerlabs/craton/issues/19


class CratonBase(models.ModelBase, models.TimestampMixin):
    def __repr__(self):
        mapper = object_mapper(self)
        cols = getattr(self, '_repr_columns', mapper.primary_key)
        items = [(p.key, getattr(self, p.key))
                 for p in [
                     mapper.get_property_by_column(c) for c in cols]]
        return "{0}({1})".format(
            self.__class__.__name__,
            ', '.join(['{0}={1!r}'.format(*item) for item in items]))


Base = declarative_base(cls=CratonBase)


class VariableMixin(object):
    """Some metaprogramming so we can avoid repeating this construction"""

    @declared_attr
    def _variables(cls):
        # Camelcase the tablename to give the Variable inner class
        # here a specific class name; necessary for reporting on
        # classes
        class_name = \
            "".join(x.title() for x in cls.vars_tablename[:-1].split('_'))

        # Because we are constructing Variable inner class with the
        # 3-arg `type` function, we need to pull out all SA columns
        # given that initialization order matters for SA!
        #
        # * Defines the primary key with correct ordering
        # * Captures references, as seen in _repr_columns
        parent_id = Column(ForeignKey(
            '%s.id' % cls.__tablename__), primary_key=True)
        key = Column(String(255), primary_key=True)
        value = Column(JSONType)
        Variable = type(class_name, (Base,), {
            '__tablename__': cls.vars_tablename,
            'parent_id': parent_id,
            'key': key,
            'value': value,
            '_repr_columns': [key, value]})

        # Need a reference for the association proxy to lookup the
        # Variable class so it can reference
        cls.variable_class = Variable

        return relationship(
            Variable,
            collection_class=attribute_mapped_collection('key'),
            cascade='all, delete-orphan', lazy='joined')

    @declared_attr
    def variables(cls):
        return association_proxy(
            '_variables', 'value',
            creator=lambda key, value: cls.variable_class(key=key,
                                                          value=value))

    @classmethod
    def with_characteristic(self, key, value):
        return self._variables.any(key=key, value=value)


class Project(Base):
    """Supports multitenancy for all other schema elements."""
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    _repr_columns = [id, name]

    # TODO(jimbaker) we will surely need to define more columns, but
    # this suffices to define multitenancy for MVP

    # one-to-many relationship with the following objects
    regions = relationship('Region', back_populates='project')
    cells = relationship('Cell', back_populates='project')
    devices = relationship('Device', back_populates='project')
    users = relationship('User', back_populates='project')

#Create Global Variable for charset of db
mysql_table_args = {'mysql_charset': 'utf8mb4', 'mysql_engine': 'InnoDB'}

class User(Base):
    __tablename__ = 'users'
    __table_args__ = (
        UniqueConstraint("username", "project_id",
                         name="uq_user0username0project"),
                         mysql_table_args
    )
    id = Column(Integer, primary_key=True)
    project_id = Column(
        Integer, ForeignKey('projects.id'), index=True, nullable=False)
    username = Column(String(255))
    api_key = Column(String(36))
    is_admin = Column(Boolean, default=False)
    roles = Column(JSONType)

    project = relationship('Project', back_populates='users')


class Region(Base, VariableMixin):
    __tablename__ = 'regions'
    __table_args__ = (
        UniqueConstraint("project_id", "name",
                         name="uq_region0projectid0name"),
                         mysql_table_args
    )
    vars_tablename = 'region_variables'
    id = Column(Integer, primary_key=True)
    project_id = Column(
        Integer, ForeignKey('projects.id'), index=True, nullable=False)
    name = Column(String(255))
    note = Column(Text)
    _repr_columns = [id, name]

    project = relationship('Project', back_populates='regions')
    cells = relationship('Cell', back_populates='region')
    devices = relationship('Device', back_populates='region')


class Cell(Base, VariableMixin):
    __tablename__ = 'cells'
    __table_args__ = (
        UniqueConstraint("region_id", "name",
                         name="uq_cell0regionid0name"),
                         mysql_table_args
    )
    vars_tablename = 'cell_variables'
    id = Column(Integer, primary_key=True)
    region_id = Column(
        Integer, ForeignKey('regions.id'), index=True, nullable=False)
    project_id = Column(
        Integer, ForeignKey('projects.id'), index=True, nullable=False)
    name = Column(String(255))
    note = Column(Text)
    _repr_columns = [id, name]

    region = relationship('Region', back_populates='cells')
    devices = relationship('Device', back_populates='cell')
    project = relationship('Project', back_populates='cells')


class Device(Base, VariableMixin):
    """Models descriptive data about a host"""
    __tablename__ = 'devices'
    __table_args__ = (
        UniqueConstraint("region_id", "name",
                         name="uq_device0regionid0name"),
                         mysql_table_args
    )
    vars_tablename = 'device_variables'
    id = Column(Integer, primary_key=True)
    type = Column(String(50))  # discriminant for joined table inheritance
    name = Column(String(255), nullable=False)
    region_id = Column(
        Integer, ForeignKey('regions.id'), index=True, nullable=False)
    cell_id = Column(
        Integer, ForeignKey('cells.id'), index=True, nullable=True)
    project_id = Column(
        Integer, ForeignKey('projects.id'), index=True, nullable=False)
    ip_address = Column(IPAddressType, nullable=False)
    device_type = Column(String(255), nullable=False)
    # this means the host is "active" for administration
    # the device may or may not be reachable by Ansible/other tooling
    #
    # TODO(jimbaker) generalize `note` for supporting governance
    active = Column(Boolean, default=True)
    note = Column(Text)
    _repr_columns = [id, name]

    # many-to-many relationship with labels; labels are sorted to
    # ensure that variable resolution is stable if labels have
    # conflicting settings for a given key
    labels = relationship(
        'Label',
        secondary=lambda: device_labels,
        collection_class=lambda: SortedSet(key=attrgetter('label')))
    associated_labels = association_proxy('labels', 'label')

    # many-to-one relationship to regions and cells
    region = relationship('Region', back_populates='devices')
    cell = relationship('Cell', back_populates='devices')
    project = relationship('Project', back_populates='devices')

    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'devices',
        'with_polymorphic': '*'
    }


class Host(Device):
    __tablename__ = 'hosts'
    __table_args__ = mysql_table_args
    id = Column(Integer, ForeignKey('devices.id'), primary_key=True)
    hostname = Device.name
    access_secret_id = Column(Integer, ForeignKey('access_secrets.id'))
    parent_id = Column(Integer, ForeignKey('hosts.id'))
    # optional many-to-one relationship to a host-specific secret
    access_secret = relationship('AccessSecret', back_populates='hosts')

    @property
    def resolved(self):
        """Provides a mapping that uses scope resolution for variables"""
        if self.cell:
            return ChainMap(
                self.variables,
                ChainMap(*[label.variables for label in self.labels]),
                self.cell.variables,
                self.region.variables)
        else:
            return ChainMap(
                self.variables,
                ChainMap(*[label.variables for label in self.labels]),
                self.region.variables)

    __mapper_args__ = {
        'polymorphic_identity': 'hosts',
    }


device_labels = Table(
    'device_labels', Base.metadata,
    Column('device_id', ForeignKey('devices.id'), primary_key=True),
    Column('label_id', ForeignKey('labels.id'), primary_key=True))


class Label(Base, VariableMixin):
    """Models a label on hosts, with a many-to-many relationship.
    Such labels include groupings like Ansible groups; as well as
    arbitrary other labels.
    Rather than subclassing labels, we can use prefixes such as
    "group-".
    It is assumed that hierarchies for groups, if any, is represented
    in an external format, such as a group-of-group inventory in
    Ansible.
    """
    __tablename__ = 'labels'
    __table_args__ = mysql_table_args
    vars_tablename = 'label_variables'
    id = Column(Integer, primary_key=True)
    label = Column(String(255), unique=True)

    _repr_columns = [label]

    def __init__(self, label):
        self.label = label

    devices = relationship(
        "Device",
        secondary=device_labels,
        back_populates="labels")


class AccessSecret(Base):
    """Represents a secret for accessing a host. It may be shared.
    For now we assume a PEM-encoded certificate that wraps the private
    key. Such certs may or may not be encrypted; if encrypted, the
    configuration specifies how to interact with other systems, such
    as Barbican or Hashicorp Vault, to retrieve secret data to unlock
    this cert.
    Note that this does not include secrets such as Ansible vault
    files; those are stored outside the inventory database as part of
    the configuration.
    """
    __tablename__ = 'access_secrets'
    __table_args__ = mysql_table_args
    id = Column(Integer, primary_key=True)
    cert = Column(Text)

    hosts = relationship('Host', back_populates='access_secret')
