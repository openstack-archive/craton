from oslo_config import cfg

from craton.db.sqlalchemy import migration


CONF = cfg.CONF


class DBCommand(object):

    def upgrade(self):
        migration.upgrade(CONF.command.revision)

    def revision(self):
        migration.revision(CONF.command.message, CONF.command.autogenerate)

    def stamp(self):
        migration.stamp(CONF.command.revision)

    def version(self):
        print(migration.version())

    def create_schema(self):
        migration.create_schema()

    def project_create(self):
        project = migration.create_project(CONF.command.projectname,
                                           CONF.database.connection)
        print("\nProject ID: {}\nProject Name: {}".format(project.id,
                                                          project.name))

    def user_create(self):
        user = migration.create_user(CONF.command.project,
                                     CONF.command.username,
                                     admin=CONF.command.admin,
                                     root=CONF.command.root,
                                     db_uri=CONF.database.connection)

        msg = ("\nProject Id: %s\nUsername: %s\nAPI Key: %s"
               %(user.project_id, user.username, user.api_key))
        print(msg)


def add_command_parsers(subparsers):
    command_object = DBCommand()

    parser = subparsers.add_parser(
        'upgrade',
        help=("Upgrade the database schema to the latest version. "
              "Optionally, use --revision to specify an alembic revision "
              "string to upgrade to."))
    parser.set_defaults(func=command_object.upgrade)
    parser.add_argument('--revision', nargs='?')

    parser = subparsers.add_parser('stamp')
    parser.add_argument('--revision', nargs='?')
    parser.set_defaults(func=command_object.stamp)

    parser = subparsers.add_parser(
        'revision',
        help=("Create a new alembic revision. "
              "Use --message to set the message string."))
    parser.add_argument('-m', '--message')
    parser.add_argument('--autogenerate', action='store_true')
    parser.set_defaults(func=command_object.revision)

    parser = subparsers.add_parser(
        'version',
        help=("Print the current version information and exit."))
    parser.set_defaults(func=command_object.version)

    parser = subparsers.add_parser(
        'create_schema',
        help=("Create the database schema."))
    parser.set_defaults(func=command_object.create_schema)


    parser = subparsers.add_parser('bootstrap-project')
    parser.add_argument('--projectname', nargs='?', required=True)
    parser.set_defaults(func=command_object.project_create)

    parser = subparsers.add_parser('bootstrap-user')
    parser.add_argument('--username', nargs='?', required=True)
    parser.add_argument('--project', nargs='?', required=True)
    parser.add_argument('--admin', nargs='?')
    parser.add_argument('--root', nargs='?')
    parser.set_defaults(func=command_object.user_create)


def main():
    command_opt = cfg.SubCommandOpt('command',
                                    title='Command',
                                    help=('Available commands'),
                                    handler=add_command_parsers)

    CONF.register_cli_opt(command_opt)
    CONF(project='craton-api')
    CONF.command.func()
