"""Use polymorphic association for variables instead of a separate mixin table

Revision ID: b3263ee5bbc2
Revises: ffdc1a500db1
Create Date: 2016-08-15 23:25:15.795190

"""

# revision identifiers, used by Alembic.
revision = 'b3263ee5bbc2'
down_revision = 'ffdc1a500db1'
branch_labels = None
depends_on = None


from alembic import op
from oslo_utils import timeutils
import sqlalchemy as sa
import sqlalchemy_utils


# Follow loosely the approach in
# http://stackoverflow.com/a/24623979/423006, which shows how to do
# both a schema migration and a nontrivial data migration. Note that
# cannot be readily done with portable SQL - but SQLAlchemy itself can
# do this!
#
# The only drawback of this approach is that we do not support SQL
# script migrations (--sql) with this approach. With some additional work,
# possibly such a data migration could be emitted.

def upgrade():
    # Commands tediously created by hand! Such polymorphic
    # associations, and certainly their rewrite from the parent
    # approach, are not supported by autogeneration.
    op.create_table(
        'variable_association',
        sa.Column('created_at', sa.DateTime, nullable=True),
        sa.Column('updated_at', sa.DateTime, nullable=True),
        sa.Column('id', sa.Integer, nullable=False),
        sa.Column('discriminator', sa.String(length=50), nullable=False),
        sa.PrimaryKeyConstraint('id'))

    op.create_table(
        'variables',
        sa.Column('created_at', sa.DateTime, nullable=True),
        sa.Column('updated_at', sa.DateTime, nullable=True),
        sa.Column('association_id', sa.Integer),
        sa.Column('key_', sa.String(length=255), nullable=False),
        sa.Column('value_', sqlalchemy_utils.types.json.JSONType(),
                  nullable=True),
        sa.PrimaryKeyConstraint('association_id', 'key_')
    )

    var_tables = ['users', 'regions', 'cells', 'labels', 'devices', 'networks']
    for table_name in var_tables:
        copy_and_move(table_name, copy_data=table_name != 'users')

    with op.batch_alter_table('variables') as batch_op:
        batch_op.create_foreign_key('fk_variables_variable_association',
                                    'variable_association',
                                    ['association_id'], ['id'])


def copy_and_move(resources_table_name, copy_data):
    global variable_association_id_counter

    op.add_column(
        resources_table_name, sa.Column('variable_association_id', sa.Integer))

    if copy_data:
        copy_and_move_data(resources_table_name)

    with op.batch_alter_table(resources_table_name) as batch_op:
        batch_op.create_foreign_key(
            'fk_%s_variable_association' % resources_table_name,
            'variable_association',
            ['variable_association_id'], ['id'])


variable_association_id_counter = 0


def copy_and_move_data(resources_table_name):
    global variable_association_id_counter

    connection = op.get_bind()

    # Our table shapes - we avoid directly working with SA models
    # since we have to deal with coexistence of old and new schema.
    #
    # Note how pluralization works - 'cells' vs 'cell_variables'.
    # Fortunately all of our resources pluralize by just adding 's'.
    resource_name = resources_table_name[:-1]
    resources = sa.sql.table(
        resources_table_name,
        sa.sql.column('id', sa.Integer),
        sa.sql.column('variable_association_id', sa.Integer))
    resource_variables = sa.sql.table(
        resource_name + '_variables',
        sa.sql.column('created_at', sa.DateTime),
        sa.sql.column('updated_at', sa.DateTime),
        sa.sql.column('parent_id', sa.Integer),
        sa.sql.column('key', sa.String),
        sa.sql.column('value', sqlalchemy_utils.types.json.JSONType))
    variables = sa.sql.table(
        'variables',
        sa.sql.column('created_at', sa.DateTime),
        sa.sql.column('updated_at', sa.DateTime),
        sa.sql.column('association_id', sa.Integer),
        sa.sql.column('key_', sa.String),
        sa.sql.column('value_', sqlalchemy_utils.types.json.JSONType))
    variable_association = sa.sql.table(
        'variable_association',
        sa.sql.column('created_at', sa.DateTime),
        sa.sql.column('id', sa.Integer),
        sa.sql.column('discriminator', sa.String))

    # A smarter query might be possible on Postgres, but I do not
    # believe common table expressions (CTEs) are available on MySQL,
    # and certainly not SQLite. Let's just keep it really simple for
    # now. At least key/values are copied over using select into, and
    # avoid serializing in/out of the database.

    for resource in connection.execute(resources.select()):
        variable_association_id_counter += 1

        # add variable_association_id value...
        connection.execute(
            resources.update().
            where(resources.c.id == resource.id).
            values(
                variable_association_id=sa.literal(
                    variable_association_id_counter)))

        # create specific association - there is an additional level
        # of indirection, hence "polymorphic association"
        connection.execute(
            variable_association.insert().values(
                created_at=timeutils.utcnow(),
                id=variable_association_id_counter,
                discriminator=resource_name))

        # copy over into 'variables'
        connection.execute(
            variables.insert().from_select(
                variables.c.keys(),
                sa.select([
                    resource_variables.c.created_at,
                    resource_variables.c.updated_at,
                    # only insert variables associated with this resource
                    sa.literal(variable_association_id_counter),
                    resource_variables.c.key,
                    resource_variables.c.value]).where(
                        resource_variables.c.parent_id == resource.id)))

    op.drop_table(resource_name + '_variables')


def downgrade():
    raise Exception("downgrade not supported")
