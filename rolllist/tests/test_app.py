from django.test import TestCase

from project.settings import NON_STAFF_PERMS
from rolllistuser.helpers import TestGroup, TestUser


class TestBase(TestCase):
    """ Base class for running app tests that need a user set up """

    def setUp(self):
        user_group = TestGroup(
            group_name='public_users',
            permission_codes=NON_STAFF_PERMS,
        )

        self.user = TestUser('tester', 'asdf1234')
        self.user.set_group(user_group.group)
