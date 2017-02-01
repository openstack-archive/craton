"""Models inventory, as defined using SQLAlchemy ORM

Craton uses the following related aspects of inventory:

* Device inventory, with devices are further organized by region,
  cell, and labels. Variables are associated with all of these
  entities, with the ability to override via resolution and to track
  with blaming. This in terms forms the foundation of an *inventory
  fabric*, which is implemented above this level.

* Workflows are run against this inventory, taking in account the
  variable configuration; as well as any specifics baked into the
  workflow itself.

"""

from collections import ChainMap
import itertools

from oslo_db.sqlalchemy import models
from sqlalchemy import (
    Boolean, Column, ForeignKey, Integer, String, Text, UniqueConstraint)
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.ext.declarative.api import _declarative_constructor
from sqlalchemy.orm import backref, object_mapper, relationship
from sqlalchemy.orm.collections import attribute_mapped_collection
from sqlalchemy_utils.types.ip_address import IPAddressType
from sqlalchemy_utils.types.json import JSONType
from sqlalchemy_utils.types.uuid import UUIDType

from craton.db.api import Blame


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


def _variable_mixin_aware_constructor(self, **kwargs):
    # The standard default for the underlying relationship for
    # variables sets it to None, which means it cannot directly be
    # used as a mappable collection. Cure the problem accordingly with
    # a different default.
    if isinstance(self, VariableMixin):
        kwargs.setdefault('variables', {})
    return _declarative_constructor(self, **kwargs)


Base = declarative_base(
    cls=CratonBase, constructor=_variable_mixin_aware_constructor)


class VariableAssociation(Base):
    """Associates a collection of Variable key-value objects
    with a particular parent.

    """
    __tablename__ = "variable_association"

    id = Column(Integer, primary_key=True)
    discriminator = Column(String(50), nullable=False)
    """Refers to the type of parent, such as 'cell' or 'device'"""

    variables = relationship(
        'Variable',
        collection_class=attribute_mapped_collection('key'),
        back_populates='association',
        cascade='all, delete-orphan', lazy='joined',
    )

    def _variable_creator(key, value):
        # Necessary to create a single key/value setting, even once
        # the corresponding variable association has been setup
        return Variable(key=key, value=value)

    values = association_proxy(
        'variables', 'value', creator=_variable_creator)

    __mapper_args__ = {
        'polymorphic_on': discriminator,
    }


class Variable(Base):
    """The Variable class.

    This represents all variable records in a single table.
    """
    __tablename__ = 'variables'
    association_id = Column(
        Integer,
        ForeignKey(VariableAssociation.id,
                   name='fk_variables_variable_association'),
        primary_key=True)
    # Use "key_", "value_" to avoid the use of reserved keywords in
    # MySQL.  This difference in naming is only visible in the use of
    # raw SQL.
    key = Column('key_', String(255), primary_key=True)
    value = Column('value_', JSONType)
    association = relationship(
        VariableAssociation, back_populates='variables',
    )
    parent = association_proxy('association', 'parent')

    def __repr__(self):
        return '%s(key=%r, value=%r)' % \
            (self.__class__.__name__, self.key, self.value)


# The VariableMixin mixin is adapted from this example code:
# http://docs.sqlalchemy.org/en/latest/_modules/examples/generic_associations/discriminator_on_association.html
# This blog post goes into more details about the underlying modeling:
# http://techspot.zzzeek.org/2007/05/29/polymorphic-associations-with-sqlalchemy/

class VariableMixin(object):
    """VariableMixin mixin, creates a relationship to
    the variable_association table for each parent.

    """

    @declared_attr
    def variable_association_id(cls):
        return Column(
            Integer,
            ForeignKey(VariableAssociation.id,
                       name='fk_%ss_variable_association' %
                       cls.__name__.lower()))

    @declared_attr
    def variable_association(cls):
        name = cls.__name__
        discriminator = name.lower()

        # Defines a polymorphic class to distinguish variables stored
        # for regions, cells, etc.
        cls.variable_assoc_cls = assoc_cls = type(
            "%sVariableAssociation" % name,
            (VariableAssociation,),
            {
                '__tablename__': None,  # because mapping into a shared table
                '__mapper_args__': {
                    'polymorphic_identity': discriminator
                }
            })

        def _assoc_creator(kv):
            assoc = assoc_cls()
            for key, value in kv.items():
                assoc.variables[key] = Variable(key=key, value=value)
            return assoc

        cls._variables = association_proxy(
            'variable_association', 'variables', creator=_assoc_creator)

        # Using a composite associative proxy here enables returning the
        # underlying values for a given key, as opposed to the
        # Variable object; we need both.
        cls.variables = association_proxy(
            'variable_association', 'values', creator=_assoc_creator)

        def with_characteristic(self, key, value):
            return self._variables.any(key=key, value=value)

        cls.with_characteristic = classmethod(with_characteristic)

        rel = relationship(
            assoc_cls,
            collection_class=attribute_mapped_collection('key'),
            cascade='all, delete-orphan', lazy='joined',
            single_parent=True,
            backref=backref('parent', uselist=False))

        return rel

    # For resolution ordering, the default is to just include
    # self. Override as desired for other resolution policy.

    @property
    def resolution_order(self):
        return [self]

    @property
    def resolution_order_variables(self):
        return [obj.variables for obj in self.resolution_order]

    @property
    def resolved(self):
        """Provides a mapping that uses scope resolution for variables"""
        return ChainMap(*self.resolution_order_variables)

    def blame(self, keys=None):
        """Determines the sources of how variables have been set.
        :param keys: keys to check sourcing, or all keys if None

        Returns the (source, variable) in a named tuple; note that
        variable contains certain audit/governance information
        (created_at, modified_at).

        TODO(jimbaker) further extend schema on mixed-in variable tables
        to capture additional governance, such as user who set the key;
        this will then transparently become available in the blame.
        """

        if keys is None:
            keys = self.resolved.keys()
        blamed = {}
        for key in keys:
            for source in self.resolution_order:
                try:
                    blamed[key] = Blame(source, source._variables[key])
                    break
                except KeyError:
                    pass
        return blamed


class Project(Base, VariableMixin):
    """Supports multitenancy for all other schema elements."""
    __tablename__ = 'projects'
    id = Column(UUIDType(binary=False), primary_key=True)
    name = Column(String(255))
    _repr_columns = [id, name]

    # TODO(jimbaker) we will surely need to define more columns, but
    # this suffices to define multitenancy for MVP

    # one-to-many relationship with the following objects
    regions = relationship('Region', back_populates='project')
    cells = relationship('Cell', back_populates='project')
    devices = relationship('Device', back_populates='project')
    users = relationship('User', back_populates='project')
    networks = relationship('Network', back_populates='project')


class User(Base, VariableMixin):
    __tablename__ = 'users'
    __table_args__ = (
        UniqueConstraint("username", "project_id",
                         name="uq_user0username0project"),
    )
    id = Column(Integer, primary_key=True)
    project_id = Column(
        UUIDType(binary=False), ForeignKey('projects.id'), index=True,
        nullable=False)
    username = Column(String(255))
    api_key = Column(String(36))
    # root = craton admin that can create other pojects/usrs
    is_root = Column(Boolean, default=False)
    # admin = project context admin
    is_admin = Column(Boolean, default=False)
    roles = Column(JSONType)

    project = relationship('Project', back_populates='users')


class Region(Base, VariableMixin):
    __tablename__ = 'regions'
    __table_args__ = (
        UniqueConstraint("project_id", "name",
                         name="uq_region0projectid0name"),
    )
    id = Column(Integer, primary_key=True)
    project_id = Column(
        UUIDType(binary=False), ForeignKey('projects.id'), index=True,
        nullable=False)
    name = Column(String(255))
    note = Column(Text)
    _repr_columns = [id, name]

    project = relationship('Project', back_populates='regions')
    cells = relationship('Cell', back_populates='region')
    devices = relationship('Device', back_populates='region')
    networks = relationship('Network', back_populates='region')


class Cell(Base, VariableMixin):
    __tablename__ = 'cells'
    __table_args__ = (
        UniqueConstraint("region_id", "name",
                         name="uq_cell0regionid0name"),
    )
    id = Column(Integer, primary_key=True)
    region_id = Column(
        Integer, ForeignKey('regions.id'), index=True, nullable=False)
    project_id = Column(
        UUIDType(binary=False), ForeignKey('projects.id'), index=True,
        nullable=False)
    name = Column(String(255))
    note = Column(Text)
    _repr_columns = [id, name]

    region = relationship('Region', back_populates='cells')
    devices = relationship('Device', back_populates='cell')
    project = relationship('Project', back_populates='cells')
    networks = relationship('Network', back_populates='cell')


class Device(Base, VariableMixin):
    """Base class for all devices."""

    __tablename__ = 'devices'
    __table_args__ = (
        UniqueConstraint("region_id", "name",
                         name="uq_device0regionid0name"),
    )
    id = Column(Integer, primary_key=True)
    type = Column(String(50))  # discriminant for joined table inheritance
    name = Column(String(255), nullable=False)
    region_id = Column(
        Integer, ForeignKey('regions.id'), index=True, nullable=False)
    cell_id = Column(
        Integer, ForeignKey('cells.id'), index=True, nullable=True)
    project_id = Column(
        UUIDType(binary=False), ForeignKey('projects.id'), index=True,
        nullable=False)
    access_secret_id = Column(Integer, ForeignKey('access_secrets.id'))
    parent_id = Column(Integer, ForeignKey('devices.id'))
    ip_address = Column(IPAddressType, nullable=False)
    device_type = Column(String(255), nullable=False)
    # TODO(jimbaker) generalize `note` for supporting governance
    active = Column(Boolean, default=True)
    note = Column(Text)

    _repr_columns = [id, name]

    project = relationship('Project', back_populates='devices')
    region = relationship('Region', back_populates='devices')
    cell = relationship('Cell', back_populates='devices')
    related_labels = relationship(
        'Label', back_populates='device', collection_class=set,
        cascade='all, delete-orphan', lazy='joined')
    labels = association_proxy('related_labels', 'label')
    access_secret = relationship('AccessSecret', back_populates='devices')
    interfaces = relationship('NetworkInterface', back_populates='device')
    children = relationship(
        'Device', backref=backref('parent', remote_side=[id]))

    @property
    def ancestors(self):
        lineage = []
        ancestor = self.parent
        while ancestor:
            lineage.append(ancestor)
            ancestor = ancestor.parent
        return lineage

    @property
    def resolution_order(self):
        # TODO(jimbaker) add self.project to resolution_order
        return list(itertools.chain(
            [self],
            self.ancestors,
            [self.cell] if self.cell else [],
            [self.region]))

    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'devices',
        'with_polymorphic': '*'
    }


class Host(Device):
    __tablename__ = 'hosts'
    id = Column(Integer, ForeignKey('devices.id'), primary_key=True)
    hostname = Device.name

    __mapper_args__ = {
        'polymorphic_identity': 'hosts',
        'inherit_condition': (id == Device.id)
    }


class NetworkInterface(Base):
    __tablename__ = 'network_interfaces'
    __table_args__ = (
        UniqueConstraint("device_id", "name",
                         name="uq_netinter0deviceid0name"),
    )
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=True)
    interface_type = Column(String(255), nullable=True)
    vlan_id = Column(Integer, nullable=True)
    port = Column(Integer, nullable=True)
    vlan = Column(String(255), nullable=True)
    duplex = Column(String(255), nullable=True)
    speed = Column(String(255), nullable=True)
    link = Column(String(255), nullable=True)
    cdp = Column(String(255), nullable=True)
    security = Column(String(255), nullable=True)
    ip_address = Column(IPAddressType, nullable=False)
    project_id = Column(UUIDType(binary=False), ForeignKey('projects.id'),
                        index=True, nullable=False)
    device_id = Column(Integer, ForeignKey('devices.id'))
    network_id = Column(Integer, ForeignKey('networks.id'), nullable=True)

    network = relationship('Network', back_populates="devices",
                           cascade='all', lazy='joined')
    device = relationship('Device', back_populates="interfaces",
                          cascade='all', lazy='joined')


class Network(Base, VariableMixin):
    __tablename__ = 'networks'
    __table_args__ = (
        UniqueConstraint("name", "project_id", "region_id",
                         name="uq_name0projectid0regionid"),
    )
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=True)
    cidr = Column(String(255), nullable=True)
    gateway = Column(String(255), nullable=True)
    netmask = Column(String(255), nullable=True)
    ip_block_type = Column(String(255), nullable=True)
    nss = Column(String(255), nullable=True)
    region_id = Column(
        Integer, ForeignKey('regions.id'), index=True, nullable=False)
    cell_id = Column(
        Integer, ForeignKey('cells.id'), index=True, nullable=True)
    project_id = Column(
        UUIDType(binary=False), ForeignKey('projects.id'), index=True,
        nullable=False)

    devices = relationship('NetworkInterface', back_populates='network')
    region = relationship('Region', back_populates='networks')
    cell = relationship('Cell', back_populates='networks')
    project = relationship('Project', back_populates='networks')


class NetworkDevice(Device):
    __tablename__ = 'network_devices'
    id = Column(Integer, ForeignKey('devices.id'), primary_key=True)
    hostname = Device.name
    # network device specific properties
    model_name = Column(String(255), nullable=True)
    os_version = Column(String(255), nullable=True)
    vlans = Column(JSONType)

    __mapper_args__ = {
        'polymorphic_identity': 'network_devices',
        'inherit_condition': (id == Device.id)
    }


class Label(Base):
    """Models arbitrary labeling (aka tagging) of devices."""
    __tablename__ = 'labels'
    device_id = Column(
        Integer,
        ForeignKey(Device.id, name='fk_labels_devices'),
        primary_key=True)
    label = Column(String(255), primary_key=True)
    _repr_columns = [device_id, label]

    def __init__(self, label):
        self.label = label

    device = relationship("Device", back_populates="related_labels")


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
    id = Column(Integer, primary_key=True)
    cert = Column(Text)

    devices = relationship('Device', back_populates='access_secret')
