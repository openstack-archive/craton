"""craton_inventory_init

Revision ID: ffdc1a500db1
Revises:
Create Date: 2016-06-03 09:52:55.302936

"""

# revision identifiers, used by Alembic.
revision = 'ffdc1a500db1'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


def upgrade():
    op.create_table(
        'variable_association',
        sa.Column('created_at', sa.DateTime, nullable=True),
        sa.Column('updated_at', sa.DateTime, nullable=True),
        sa.Column('id', sa.Integer, nullable=False),
        sa.Column('discriminator', sa.String(length=50), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'variables',
        sa.Column('created_at', sa.DateTime, nullable=True),
        sa.Column('updated_at', sa.DateTime, nullable=True),
        sa.Column('association_id', sa.Integer),
        sa.Column('key_', sa.String(length=255), nullable=False),
        sa.Column('value_', sqlalchemy_utils.types.json.JSONType(),
                  nullable=True),
        sa.PrimaryKeyConstraint('association_id', 'key_'),
        sa.ForeignKeyConstraint(
            ['association_id'], ['variable_association.id'],
            'fk_variables_variable_association')
    )
    op.create_table(
        'access_secrets',
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('cert', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'labels',
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('variable_association_id', sa.Integer),
        sa.Column('label', sa.String(length=255), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('label'),
        sa.ForeignKeyConstraint(
            ['variable_association_id'], ['variable_association.id'],
            'fk_labels_variable_association')
    )
    op.create_table(
        'projects',
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('variable_association_id', sa.Integer),
        sa.Column('name', sa.String(length=255), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(
            ['variable_association_id'], ['variable_association.id'],
            'fk_projects_variable_association')
    )
    op.create_table(
        'regions',
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('project_id', sa.Integer(), nullable=False),
        sa.Column('variable_association_id', sa.Integer),
        sa.Column('name', sa.String(length=255), nullable=True),
        sa.Column('note', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('project_id', 'name',
                            name='uq_region0projectid0name'),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
        sa.ForeignKeyConstraint(
            ['variable_association_id'], ['variable_association.id'],
            'fk_regions_variable_association')
    )
    op.create_index(op.f('ix_regions_project_id'),
                    'regions', ['project_id'], unique=False)
    op.create_table(
        'users',
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('project_id', sa.Integer(), nullable=False),
        sa.Column('variable_association_id', sa.Integer),
        sa.Column('username', sa.String(length=255), nullable=True),
        sa.Column('api_key', sa.String(length=36), nullable=True),
        sa.Column('is_root', sa.Boolean(), nullable=True),
        sa.Column('is_admin', sa.Boolean(), nullable=True),
        sa.Column('roles', sqlalchemy_utils.types.json.JSONType(),
                  nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('username', 'project_id',
                            name='uq_user0username0project'),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
        sa.ForeignKeyConstraint(
            ['variable_association_id'], ['variable_association.id'],
            'fk_users_variable_association')
    )
    op.create_index(op.f('ix_users_project_id'), 'users', ['project_id'],
                    unique=False)
    op.create_table(
        'cells',
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('project_id', sa.Integer(), nullable=False),
        sa.Column('region_id', sa.Integer(), nullable=False),
        sa.Column('variable_association_id', sa.Integer),
        sa.Column('name', sa.String(length=255), nullable=True),
        sa.Column('note', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('region_id', 'name', name='uq_cell0regionid0name'),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
        sa.ForeignKeyConstraint(['region_id'], ['regions.id'], ),
        sa.ForeignKeyConstraint(
            ['variable_association_id'], ['variable_association.id'],
            'fk_cells_variable_association')
    )
    op.create_index(op.f('ix_cells_project_id'), 'cells', ['project_id'],
                    unique=False)
    op.create_index(op.f('ix_cells_region_id'), 'cells', ['region_id'],
                    unique=False)
    op.create_table(
        'networks',
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('project_id', sa.Integer(), nullable=False),
        sa.Column('region_id', sa.Integer(), nullable=False),
        sa.Column('cell_id', sa.Integer(), nullable=True),
        sa.Column('variable_association_id', sa.Integer),
        sa.Column('name', sa.String(length=255), nullable=True),
        sa.Column('cidr', sa.String(length=255), nullable=True),
        sa.Column('gateway', sa.String(length=255), nullable=True),
        sa.Column('netmask', sa.String(length=255), nullable=True),
        sa.Column('ip_block_type', sa.String(length=255), nullable=True),
        sa.Column('nss', sa.String(length=255), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
        sa.ForeignKeyConstraint(['region_id'], ['regions.id'], ),
        sa.ForeignKeyConstraint(['cell_id'], ['cells.id'], ),
        sa.ForeignKeyConstraint(
            ['variable_association_id'], ['variable_association.id'],
            'fk_networks_variable_association')
    )
    op.create_index(
        op.f('ix_networks_cell_id'),
        'networks',
        ['cell_id'],
        unique=False)
    op.create_index(
        op.f('ix_networks_project_id'),
        'networks',
        ['project_id'],
        unique=False)
    op.create_index(
        op.f('ix_networks_region_id'),
        'networks',
        ['region_id'],
        unique=False)
    op.create_table(
        'devices',
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('type', sa.String(length=50), nullable=True),
        sa.Column('device_type', sa.String(length=255), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('project_id', sa.Integer(), nullable=False),
        sa.Column('region_id', sa.Integer(), nullable=False),
        sa.Column('cell_id', sa.Integer(), nullable=True),
        sa.Column('parent_id', sa.Integer(), nullable=True),
        sa.Column('access_secret_id', sa.Integer(), nullable=True),
        sa.Column('variable_association_id', sa.Integer),
        sa.Column('ip_address',
                  sqlalchemy_utils.types.IPAddressType(length=64),
                  nullable=False),
        sa.Column('active', sa.Boolean(), nullable=True),
        sa.Column('note', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('region_id', 'name',
                            name='uq_device0regionid0name'),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
        sa.ForeignKeyConstraint(['region_id'], ['regions.id'], ),
        sa.ForeignKeyConstraint(['cell_id'], ['cells.id'], ),
        sa.ForeignKeyConstraint(['access_secret_id'], ['access_secrets.id'], ),
        sa.ForeignKeyConstraint(['parent_id'], ['devices.id'], ),
        sa.ForeignKeyConstraint(
            ['variable_association_id'], ['variable_association.id'],
            'fk_devices_variable_association')
    )
    op.create_index(op.f('ix_devices_cell_id'), 'devices', ['cell_id'],
                    unique=False)
    op.create_index(op.f('ix_devices_project_id'), 'devices', ['project_id'],
                    unique=False)
    op.create_index(op.f('ix_devices_region_id'), 'devices', ['region_id'],
                    unique=False)
    op.create_table(
        'device_labels',
        sa.Column('device_id', sa.Integer(), nullable=False),
        sa.Column('label_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['device_id'], ['devices.id'], ),
        sa.ForeignKeyConstraint(['label_id'], ['labels.id'], ),
        sa.PrimaryKeyConstraint('device_id', 'label_id')
    )
    op.create_table(
        'hosts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['id'], ['devices.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'net_devices',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('model_name', sa.String(length=255), nullable=True),
        sa.Column('os_version', sa.String(length=255), nullable=True),
        sa.Column('vlans', sqlalchemy_utils.types.json.JSONType(),
                  nullable=True),
        sa.ForeignKeyConstraint(['id'], ['devices.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'net_interfaces',
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('variable_association_id', sa.Integer),
        sa.Column('name', sa.String(length=255), nullable=True),
        sa.Column('interface_type', sa.String(length=255), nullable=True),
        sa.Column('vlan_id', sa.Integer(), nullable=True),
        sa.Column('port', sa.Integer(), nullable=True),
        sa.Column('vlan', sa.String(length=255), nullable=True),
        sa.Column('duplex', sa.String(length=255), nullable=True),
        sa.Column('speed', sa.String(length=255), nullable=True),
        sa.Column('link', sa.String(length=255), nullable=True),
        sa.Column('cdp', sa.String(length=255), nullable=True),
        sa.Column('security', sa.String(length=255), nullable=True),
        sa.Column('device_id', sa.Integer(), nullable=False),
        sa.Column('network_id', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('device_id', 'name',
                            name='uq_netinter0deviceid0name'),
        sa.ForeignKeyConstraint(['device_id'], ['net_devices.id'], ),
        sa.ForeignKeyConstraint(['network_id'], ['networks.id'], ),
        sa.ForeignKeyConstraint(
            ['variable_association_id'], ['variable_association.id'],
            'fk_net_interfaces_variable_association')
    )


def downgrade():
    op.drop_table('net_interfaces')
    op.drop_table('net_devices')
    op.drop_table('hosts')
    op.drop_index(op.f('ix_networks_region_id'), table_name='networks')
    op.drop_index(op.f('ix_networks_project_id'), table_name='networks')
    op.drop_index(op.f('ix_networks_cell_id'), table_name='networks')
    op.drop_table('networks')
    op.drop_table('device_labels')
    op.drop_index(op.f('ix_devices_region_id'), table_name='devices')
    op.drop_index(op.f('ix_devices_project_id'), table_name='devices')
    op.drop_index(op.f('ix_devices_cell_id'), table_name='devices')
    op.drop_table('devices')
    op.drop_index(op.f('ix_cells_region_id'), table_name='cells')
    op.drop_index(op.f('ix_cells_project_id'), table_name='cells')
    op.drop_table('cells')
    op.drop_index(op.f('ix_users_project_id'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_regions_project_id'), table_name='regions')
    op.drop_table('regions')
    op.drop_table('projects')
    op.drop_table('labels')
    op.drop_table('access_secrets')
    op.drop_table('variables')
    op.drop_table('variable_association')
