from craton import exceptions
from craton.db import api as dbapi
from craton.tests.unit.db import base


root = {'project_id': 1, 'username': 'root', "is_admin": True, "is_root": True}
user1 = {'project_id': 2, 'username': 'user1', "is_admin": True}
user2 = {'project_id': 2, 'username': 'user2', "is_admin": False}


class UsersDBTestCase(base.DBTestCase):

    def make_user(self, user, is_admin=True, is_root=False):
        # Set admin context first
        self.context.is_admin = is_admin
        self.context.is_admin_project = is_root
        user = dbapi.users_create(self.context, user)
        return user

    def test_user_create(self):
        user = self.make_user(user1)
        self.assertEqual(user['username'], 'user1')

    def test_user_create_no_admin_context_fails(self):
        self.assertRaises(exceptions.AdminRequired,
                          self.make_user,
                          user1,
                          is_admin=False)

    def test_users_get_all(self):
        # Ensure context tenant is the same one as the
        # one that will make request, test context has
        # fake-tenant set by default.
        self.context.tenant = user1['project_id']
        dbapi.users_create(self.context, user1)
        dbapi.users_create(self.context, user2)
        res = dbapi.users_get_all(self.context)
        self.assertEqual(len(res), 2)

    def test_user_get_all_no_project_context(self):
        # Ensure when request has no root context and the request
        # is not for the same project no user info is given back.
        self.make_user(user1)
        self.context.tenant = '12345'
        res = dbapi.users_get_all(self.context)
        self.assertEqual(len(res), 0)

    def test_user_get_no_admin_context_raises(self):
        self.make_user(user1)
        self.context.is_admin = False
        self.assertRaises(exceptions.AdminRequired,
                          dbapi.users_get_all,
                          self.context)

    def test_user_get_by_name(self):
        dbapi.users_create(self.context, user1)
        dbapi.users_create(self.context, user2)
        self.context.tenant = user1['project_id']
        res = dbapi.users_get_by_name(self.context, user1['username'])
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]['username'], user1['username'])

    def test_user_get_by_id(self):
        user = self.make_user(user1)
        res = dbapi.users_get_by_id(self.context, user["id"])
        self.assertEqual(res["username"], user["username"])
