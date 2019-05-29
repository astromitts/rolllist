from project.helpers import TestBase

from django.test import TestCase

from rolllist.models.appmodels import Day, ScheduleItem, RecurringScheduleItem
from rolllist.utils import get_relevant_time_id, DayScheduleDeux


class ScheduleItemTestBase(TestBase):
    """ Create base data for testing schedule item logic
    """

    def setUp(self):
        super(ScheduleItemTestBase, self).setUp()
        self.item_to_recur = ScheduleItem(
            day=self.day,
            user=self.user.user.rolllistuser,
            title='Recurring item',
            start_time=get_relevant_time_id('9:00 AM'),
            end_time=get_relevant_time_id('9:30 AM'),
            location='The Internet'
        )
        self.item_to_recur.save()

        self.item_once = ScheduleItem(
            day=self.day,
            user=self.user.user.rolllistuser,
            title='Single time item morning',
            start_time=get_relevant_time_id('10:00 AM'),
            end_time=get_relevant_time_id('10:30 AM'),
            location='Some place'
        )
        self.item_once.save()

        self.item_once_2 = ScheduleItem(
            day=self.day,
            user=self.user.user.rolllistuser,
            title='Single time item afternoon',
            start_time=get_relevant_time_id('1:00 PM'),
            end_time=get_relevant_time_id('1:30 PM'),
            location='Some other place'
        )
        self.item_once_2.save()


class TestScheduleItems(ScheduleItemTestBase):

    def test_recurrance_relationship(self):
        self.item_to_recur.make_recurring()

        recurrance = RecurringScheduleItem.objects.get(id=self.item_to_recur.recurrance.id)
        self.assertEqual(self.item_to_recur.title, recurrance.title)
        self.assertEqual(self.item_to_recur.start_time, recurrance.start_time)
        self.assertEqual(self.item_to_recur.end_time, recurrance.end_time)
        self.assertEqual(self.item_to_recur.location, recurrance.location)


class TestDayModel(ScheduleItemTestBase):

    def test_get_schedule_items(self):
        self.item_to_recur.make_recurring()
        recurrance = RecurringScheduleItem.objects.get(id=self.item_to_recur.recurrance.id)

        schedule_items = self.day.get_schedule_items(self.user.user.rolllistuser)
        self.assertTrue(recurrance in schedule_items)
        self.assertTrue(self.item_once in schedule_items)
        self.assertTrue(self.item_once_2 in schedule_items)


class TestDayScheduleDeux(ScheduleItemTestBase):

    def test_day_schedule_util(self):
        self.item_to_recur.make_recurring()
        schedule = DayScheduleDeux(
            day=self.day,
            user=self.user.user.rolllistuser
        )
        scheduled_items = self.day.get_schedule_items(self.user.user.rolllistuser)
        scheduled_item_ids = [i.start_time for i in scheduled_items]
        scheduled_items_by_int_id = {i['int_id']: i for i in schedule.schedule}
        for i, data in scheduled_items_by_int_id.items():
            if i in scheduled_item_ids:
                self.assertTrue(len(data['items']) >= 1)
            else:
                self.assertFalse(data['items'])


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
