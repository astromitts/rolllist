import datetime

from project.helpers import TestBase

from django.test import TestCase

from rolllist.models.appmodels import (
    Day,
    ScheduleItem,
    RecurringScheduleItem,
    ToDoList,
    ToDoItem,
)
from rolllist.utils import get_relevant_time_id, relevant_time_dict, DayScheduleDeux


class ScheduleItemTestBase(TestBase):
    """ Create base data for testing schedule item logic
    """

    def setUp(self):
        super(ScheduleItemTestBase, self).setUp()
        self._get_next_monday()
        self.expected_intervals = {}
        self.item_to_recur = RecurringScheduleItem(
            user=self.user.user.rolllistuser,
            title='Recurring item',
            start_time=get_relevant_time_id('9:00 AM'),
            end_time=get_relevant_time_id('10:30 AM'),
            location='The Internet',
            recurrance_0=True,
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

    def _set_up_past_instances(self, amount=3):
        """ Helper function to run set_for_day for a RecurringItem X amount
            of days into the future
        """
        for i in range(1, amount+1):
            date = datetime.date.today() - datetime.timedelta(i)
            day, created = Day().get_or_create(date=date)
            self.item_to_recur.set_for_day(day)

    def _set_up_today_and_future_instances(self, amount=3):
        """ Helper function to run set_for_day for a RecurringItem X amount
            of days in the past
        """
        for i in range(0, amount+1):
            date = datetime.date.today() + datetime.timedelta(i)
            day, created = Day().get_or_create(date=date)
            self.item_to_recur.set_for_day(day)


class TestRecurringItem(ScheduleItemTestBase):

    def setUp(self):
        super(TestRecurringItem, self).setUp()
        self.item_to_recur.recurrance_0 = True
        self.item_to_recur.recurrance_1 = True
        self.item_to_recur.recurrance_2 = True
        self.item_to_recur.recurrance_3 = True
        self.item_to_recur.recurrance_4 = True
        self.item_to_recur.recurrance_5 = True
        self.item_to_recur.recurrance_6 = True
        self.item_to_recur.save()

        self.init_title = self.item_to_recur.title
        self.init_location = self.item_to_recur.location

        self.today, created = Day.get_or_create(date=datetime.date.today())

    def test_recurring_item_set_for_day(self):
        """ Verify the logic that a recurring item should not generate schedule
            instances for days that occurred in the past, relative to the day
            the Recurring Item was created
        """
        self._set_up_past_instances()
        self._set_up_today_and_future_instances()

        scheduled_instances = ScheduleItem.objects.filter(recurrance=self.item_to_recur)

        scheduled_instances = ScheduleItem.objects.filter(title=self.init_title)
        self.assertIsNotNone(scheduled_instances)

        for instance in scheduled_instances:
            self.assertTrue(instance.day.date >= self.today.date)

    def test_edit_recurring_item(self):
        """ Test that editing a recurring item updates today's instance of that
            item and future instances, but leaves past instances as-is
        """
        self._set_up_today_and_future_instances(7)
        date_in_three_days = datetime.date.today() + datetime.timedelta(3)
        day_in_three_days, created = Day().get_or_create(date=date_in_three_days)

        new_title = "New Title"
        new_location = "New Location"

        self.item_to_recur.update_current_and_future(day_in_three_days, {'title': new_title, 'location': new_location})
        scheduled_instances = ScheduleItem.objects.filter(recurrance=self.item_to_recur)
        # flags to prevent false positive test passes
        flag_found_past = False
        flag_found_future = False
        for instance in scheduled_instances:
            if instance.day.date < day_in_three_days.date:
                flag_found_past = True
                self.assertEqual(instance.title, self.init_title)
                self.assertEqual(instance.location, self.init_location)
            else:
                flag_found_future = True
                self.assertEqual(instance.title, new_title)
                self.assertEqual(instance.location, new_location)
        self.assertTrue(flag_found_future)
        self.assertTrue(flag_found_past)

    def test_delete_recurring_item(self):
        """ Test that deleting a recurring item deletes today's instance of that
            item and future instances, but leaves past instances as-is
        """
        self._set_up_today_and_future_instances(7)

        date_in_three_days = datetime.date.today() + datetime.timedelta(3)
        day_in_three_days, created = Day().get_or_create(date=date_in_three_days)

        self.item_to_recur.delete_current_and_future(day_in_three_days)
        scheduled_instances = ScheduleItem.objects.filter(title=self.init_title)

        self.assertIsNotNone(scheduled_instances)
        for instance in scheduled_instances:
            self.assertTrue(instance.day.date < date_in_three_days)


class TestDayModel(ScheduleItemTestBase):

    def test_get_schedule_items(self):
        """ Verify that scheduled items for a day are returned in recurrance_instances
            This includes recurring and non-recurring items
        """
        schedule_items = self.day.get_schedule_items(self.user.user.rolllistuser)
        recurrance_instances = []
        for item in schedule_items:
            recurrance_instances.append(item.recurrance)

        self.assertTrue(self.item_to_recur in recurrance_instances)
        self.assertFalse(self.item_once in recurrance_instances)
        self.assertFalse(self.item_once_2 in recurrance_instances)
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
                if item.recurrance:
                    item = item.recurrance
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


class TestToDoListItems(TestBase):
    def setUp(self):
        super(TestToDoListItems, self).setUp()
        self.yesterday, created = Day.get_or_create(date=datetime.date.today() - datetime.timedelta(1))
        self.yesterday_todo_list, created = ToDoList.get_or_create(
            day=self.yesterday,
            user=self.user.user.rolllistuser
        )

        to_do_items = [
            # should not rollover because it is complete
            ('Make the bed', 1, True, False),
            # should not rollover because it is complete
            ('Feed the cats', 2, True, True),
            # should rollover because it is not complete and not rolled over already
            ('Smash the patriarchy', 3, False, False),
            # should rollover because it is not complete and not rolled over already
            ('Catch a Rainbow', 3, False, False),
            # should NOT rollover because it is rolled over already - avoids dupes
            ('Make a million dollars', 3, False, True),
        ]

        self.expected_rollover_items = [to_do_items[2], to_do_items[3]]

        for item in to_do_items:
            title = item[0]
            priority = item[1]
            completed = item[2]
            rolled_over = item[3]
            tdi = ToDoItem(
                title=title,
                priority=priority,
                to_do_list=self.yesterday_todo_list,
                completed=completed,
                rolled_over=rolled_over
            )
            tdi.save()

    def test_to_do_rollover(self):
        """ Verify that only incomplete, not yet rolled over items get rolled over to today """
        today, created = Day.get_or_create(date=datetime.date.today())
        todo_list, created = ToDoList.get_or_create(day=today, user=self.user.user.rolllistuser)
        created_items = todo_list.rollover_items()
        self.assertEqual(len(created_items), len(self.expected_rollover_items))
        for item in created_items:
            self.assertTrue(item.title in [i[0] for i in self.expected_rollover_items])


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
