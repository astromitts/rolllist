from datetime import timedelta
from django.test import TestCase

from project.settings import NON_STAFF_PERMS

from rolllist.utils import get_relevant_time_id
import datetime
from rolllistuser.helpers import TestGroup, TestUser
from rolllist.models.appmodels import (
    Day,
    ScheduleItem,
    ToDoList,
    ToDoItem,
    Note
)


class TestAlertsMixin():
    def assertMessageSent(self, expected_message, response_object):  # noqa
        self.assertIn(
            expected_message,
            [m.message for m in response_object.context['messages']._loaded_messages]
        )


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

        day, created = Day.get_or_create(date=self._get_next_monday())
        self.day = day
        self.day_url_str = '{0:%Y%m%d}'.format(self.day.date)

    def _get_next_monday(self):
        """ helper function to get the next ocurring monday as a date object """
        today = datetime.date.today()
        weekday_int = today.weekday()
        if weekday_int == 0:
            return today
        next_mon = today + timedelta(7 - weekday_int)
        return next_mon


class TestBaseWithScheduleData(TestCase):
    """ Base class for running app tests that need a user set up
        and appliction data
    """

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

    def _add_todo_items(self):
        """ Helper function adding some known to-do list items for the test user
        """

        todo_list = ToDoList(day=self.day, user=self.user.user.rolllistuser)
        todo_list.save()

        items = [
            'feed the cats',
            'drive to work',
            'read a book',
            'eat some food',
        ]
        todo_items = []
        for item in items:
            new_item = ToDoItem(
                title=item,
                to_do_list=todo_list,
                priority=1
            )
            new_item.save()
            todo_items.append(new_item)
        return todo_items

    def _backfill_todo_items_for_previous_day(self):
        """ Helper function adding some known to-do list items for the test user
            for the previous day
        """
        previous_day_date = self.day.date - timedelta(days=1)
        day, created = Day.get_or_create(date=previous_day_date)

        todo_list = ToDoList(day=day, user=self.user.user.rolllistuser)
        todo_list.save()

        items = [
            'cut the grass',
            'water the plants',
            'take out the trash',
        ]
        todo_items = []
        for item in items:
            new_item = ToDoItem(
                title=item,
                to_do_list=todo_list,
                priority=1
            )
            new_item.save()
            todo_items.append(new_item)
        return todo_items

    def _add_schedule_items(self):
        """ Helper function adding some known schedule items for the test user
        """

        schedules = [
            {
                'start_time': '9:30 AM',
                'end_time': '10:00 AM',
                'title': 'Daily Scrum',
                'location': 'Hogwarts',
                'day': self.day,
                'user': self.user.user.rolllistuser,
            },
            {
                'start_time': '10:30 AM',
                'end_time': '11:00 AM',
                'title': 'Engineering Interview',
                'location': 'Narnia',
                'day': self.day,
                'user': self.user.user.rolllistuser,
            },
            {
                'start_time': '12:00 PM',
                'end_time': '12:30 PM',
                'title': 'Lunch',
                'location': 'Kitchen',
                'day': self.day,
                'user': self.user.user.rolllistuser,
            },
            {
                'start_time': '2:00 PM',
                'end_time': '2:30 PM',
                'title': 'Workout',
                'location': 'Gym',
                'day': self.day,
                'user': self.user.user.rolllistuser,
            },
        ]

        recurring_item_data = {
            'start_time': '3:00 PM',
            'end_time': '3:30 PM',
            'title': 'Recurring thing',
            'location': 'asdf',
            'day': self.day,
            'user': self.user.user.rolllistuser,
        }

        schedule_items = []

        schedule_dict = {i['start_time']: i for i in schedules}

        for schedule in schedules:
            save_data = schedule
            save_data['start_time'] = get_relevant_time_id(schedule['start_time'])
            save_data['end_time'] = get_relevant_time_id(schedule['end_time'])
            new_schedule_item = ScheduleItem(**save_data)
            new_schedule_item.save()
            schedule_items.append(new_schedule_item)

        save_data = recurring_item_data
        save_data['start_time'] = get_relevant_time_id(recurring_item_data['start_time'])
        save_data['end_time'] = get_relevant_time_id(recurring_item_data['end_time'])
        new_schedule_item = ScheduleItem(**save_data)
        new_schedule_item.save()
        new_schedule_item.make_recurring([0])
        schedule_items.append(new_schedule_item)

        return schedule_items, schedule_dict

    def _add_notes(self):
        note_data = [
            (
                'Pop quiz: what is the greatest thing to happen to your mind, '
                'body, and soul in recent history? A cheeseburger, obviously. '
                'Cheeseburgers know that what you want can also be what '
                'you need.'
            ),
            (
                'Some are cheesy, others can be a little dry, and the rare '
                'few are a disaster. There are so many cheeseburgers out '
                'there it can be hard to commit to just one favourite. That '
                'being said, when you know, you just know.'
            )
        ]
        notes = []
        for note in note_data:
            newnote = Note(
                content=note,
                user=self.user.user.rolllistuser,
                day=self.day
            )
            newnote.save()
            notes.append(newnote)
        return notes
