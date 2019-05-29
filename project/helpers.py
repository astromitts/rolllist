from django.test import TestCase

from project.settings import NON_STAFF_PERMS
from rolllist.models.appmodels import Day
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
        self.client.login(username=self.user.username, password=self.user.password)

        day, created = Day.get_or_create()
        self.day = day
        self.day_url_str = '{0:%Y%m%d}'.format(self.day.date)