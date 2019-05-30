from project.helpers import TestBase

from django.test import TestCase

from rolllist.models.appmodels import Day, ScheduleItem, RecurringScheduleItem
from rolllist.utils import get_relevant_time_id, relevant_time_dict, DayScheduleDeux


class ScheduleItemTestBase(TestBase):
    """ Create base data for testing schedule item logic
    """

    def setUp(self):
        super(ScheduleItemTestBase, self).setUp()
        self.expected_intervals = {}
        self.item_to_recur = RecurringScheduleItem(
            user=self.user.user.rolllistuser,
            title='Recurring item',
            start_time=get_relevant_time_id('9:00 AM'),
            end_time=get_relevant_time_id('10:30 AM'),
            location='The Internet'
        )
        self.item_to_recur.save()
        self.expected_intervals[self.item_to_recur] = [
            get_relevant_time_id('9:00 AM'),
            get_relevant_time_id('9:30 AM'),
            get_relevant_time_id('10:00 AM'),

        ]

        self.item_once = ScheduleItem(
            day=self.day,
            user=self.user.user.rolllistuser,
            title='Single time item morning',
            start_time=get_relevant_time_id('12:00 PM'),
            end_time=get_relevant_time_id('2:30 PM'),
            location='Some place'
        )
        self.item_once.save()
        self.expected_intervals[self.item_once] = [
            get_relevant_time_id('12:00 PM'),
            get_relevant_time_id('12:30 PM'),
            get_relevant_time_id('1:00 PM'),
            get_relevant_time_id('1:30 PM'),
            get_relevant_time_id('2:00 PM'),

        ]

        self.item_once_2 = ScheduleItem(
            day=self.day,
            user=self.user.user.rolllistuser,
            title='Single time item afternoon',
            start_time=get_relevant_time_id('3:00 PM'),
            end_time=get_relevant_time_id('3:30 PM'),
            location='Some other place'
        )
        self.item_once_2.save()
        self.expected_intervals[self.item_once_2] = [
            get_relevant_time_id('3:00 PM'),

        ]


class TestDayModel(ScheduleItemTestBase):

    def test_get_schedule_items(self):
        schedule_items = self.day.get_schedule_items(self.user.user.rolllistuser)
        self.assertTrue(self.item_to_recur in schedule_items)
        self.assertTrue(self.item_once in schedule_items)
        self.assertTrue(self.item_once_2 in schedule_items)


class TestDayScheduleDeux(ScheduleItemTestBase):

    def test_day_schedule_util(self):
        day_schedule = DayScheduleDeux(
            day=self.day,
            user=self.user.user.rolllistuser
        )
        used_intervals = []
        for model_object, intervals in self.expected_intervals.items():
            used_intervals += intervals

        for schedule_block in day_schedule.schedule:
            if schedule_block.get('interval'):
                interval_id = schedule_block['interval']
            else:
                interval_id = get_relevant_time_id(schedule_block['start_time_display'])

            if interval_id in used_intervals:
                item = schedule_block['item']
                expected_data = {
                    'intervals': self.expected_intervals[item],
                }
                for key, expected in expected_data.items():
                    self.assertEqual(expected, schedule_block[key])
            else:
                expected_data = {
                    'start_time_display': relevant_time_dict[schedule_block['interval']],
                    'intervals': None,
                    'item': None,
                    'interval': schedule_block['interval']
                }
                for key, expected in expected_data.items():
                    self.assertEqual(expected, schedule_block[key])


class TestGetOrCreate(TestCase):

    def test_create_day(self):
        new_day, created = Day.get_or_create()
        self.assertTrue(created)
        self.assertTrue(isinstance(new_day, Day))

    def test_get_day(self):
        new_day = Day.objects.create()
        new_day.save()

        old_day, created = Day.get_or_create()
        self.assertFalse(created)
        self.assertEqual(new_day, old_day)
