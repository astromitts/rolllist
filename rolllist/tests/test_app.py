from django.test import TestCase
from django.urls import reverse

from project.settings import NON_STAFF_PERMS
from rolllistuser.helpers import TestGroup, TestUser
from rolllist.utils import get_relevant_time_id
from rolllist.models.appmodels import Day, ScheduleItem


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


class TestViewsCase(TestBase):
    def _add_schedule_items(self, day):

        schedules = [
            {
                'start_time': get_relevant_time_id('9:30 AM'),
                'end_time': get_relevant_time_id('10:00 AM'),
                'title': 'Daily Scrum',
                'location': 'Hogwarts',
                'day': day,
                'user': self.user.user.rolllistuser,
            },
            {
                'start_time': get_relevant_time_id('10:30 AM'),
                'end_time': get_relevant_time_id('11:30 AM'),
                'title': 'Engineering Interview',
                'location': 'Narnia',
                'day': day,
                'user': self.user.user.rolllistuser,
            },
            {
                'start_time': get_relevant_time_id('12:00 PM'),
                'end_time': get_relevant_time_id('1:00 PM'),
                'title': 'Lunch',
                'location': 'Kitchen',
                'day': day,
                'user': self.user.user.rolllistuser,
            },
            {
                'start_time': get_relevant_time_id('2:00 PM'),
                'end_time': get_relevant_time_id('3:30 PM'),
                'title': 'Workout',
                'location': 'Gym',
                'day': day,
                'user': self.user.user.rolllistuser,
            },
        ]

        schedule_items = []

        for schedule in schedules:
            new_schedule_item = ScheduleItem(**schedule)
            new_schedule_item.save()
            schedule_items.append(new_schedule_item)
        return schedule_items

    def test_dashboard_loads(self):
        response = self.client.get(reverse('dashboard'))
        self.assertTrue('your schedule for' in str(response.content))

    def test_schedule_table(self):
        schedule_items = self._add_schedule_items(self.day)
        import pdb
        pdb.set_trace()
