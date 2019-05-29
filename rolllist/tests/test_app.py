from bs4 import BeautifulSoup

from django.urls import reverse

from project.helpers import TestBase
from rolllist.utils import get_relevant_time_id
from rolllist.models.appmodels import ScheduleItem, ToDoList, ToDoItem


class TestViewsCase(TestBase):
    """ Test Cases that use the django test client to go to specific views
        and verify their content based on known data

        TODO this is pretty brittle and will need to be updated with any
        HTML / template changes but whatcha gonna do?
    """
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
                to_do_list=todo_list
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

        schedule_items = []

        schedule_dict = {i['start_time']: i for i in schedules}

        for schedule in schedules:
            save_data = schedule
            save_data['start_time'] = get_relevant_time_id(schedule['start_time'])
            save_data['end_time'] = get_relevant_time_id(schedule['end_time'])
            new_schedule_item = ScheduleItem(**schedule)
            new_schedule_item.save()
            schedule_items.append(new_schedule_item)
        return schedule_items, schedule_dict

    def test_dashboard_loads(self):
        response = self.client.get(reverse('dashboard'))
        self.assertTrue('your schedule for' in str(response.content))

    def test_schedule_table(self):
        """ Verify the appearance of scheduled items in the schedule table view
        """
        schedule_items, schedule_dict = self._add_schedule_items()
        schedule_table = self.client.get(reverse('get_schedule', kwargs={'datestr': self.day_url_str}))
        schedule_contents = BeautifulSoup(schedule_table.content, features='html.parser')
        schedule_rows = schedule_contents.find_all('div',  {'class': 'schedulerow'})
        row_count = 1
        for row in schedule_rows:
            time_start = row.find('div', {'class': 'schedulecell-sm'}).text

            # if an item was scheduled for this interval verify the contents
            if time_start in schedule_dict:
                time_id = get_relevant_time_id(time_start)
                links = row.find_all('a', {'id': time_id})
                delete_link = links[0]
                edit_link = links[1]
                self.assertTrue('/deletescheduleitemform/' in delete_link['href'])
                self.assertTrue('/editscheduleitem/' in edit_link['href'])
                self.assertTrue(
                    '%s (%s)' % (
                        schedule_dict[time_start]['title'],
                        schedule_dict[time_start]['location']
                    )
                )
            # if no item was scheduled for this interval verify the contents
            else:
                # the last row doesn't get an add item option until I figure that out
                if row_count < len(schedule_rows):
                    time_id = get_relevant_time_id(time_start)
                    add_link = row.find('a', {'id': time_id})
                    self.assertTrue('/addscheduleitem/' in add_link['href'])
            row_count += 1

    def test_delete_schedule_item(self):
        """ Verify the delete schedule item workflow
        """
        schedule_items, schedule_dict = self._add_schedule_items()
        item_to_delete = schedule_items[1]
        self.client.post(
            reverse('delete_item_form', kwargs={'item_id': item_to_delete.id}),
            {
                'item_id': item_to_delete.id
            }
        )
        schedule_table = self.client.get(reverse('get_schedule', kwargs={'datestr': self.day_url_str}))
        schedule_contents = BeautifulSoup(schedule_table.content, features='html.parser')
        for item in schedule_items:
            if item == item_to_delete:
                self.assertFalse(item.title in schedule_contents.text)
            else:
                self.assertTrue(item.title in schedule_contents.text)

    def test_add_schedule_item(self):
        """ Verify the add schedule item workflow
        """

        item_data = {
            'title': 'escape',
            'start_time': get_relevant_time_id('8:00 AM'),
            'end_time': get_relevant_time_id('8:30 AM'),
            'location': 'LA'
        }
        self.client.post(
            reverse('add_item', kwargs={'datestr': self.day_url_str, 'start_time_int': get_relevant_time_id('8:00 AM')}),
            item_data
        )
        schedule_table = self.client.get(reverse('get_schedule', kwargs={'datestr': self.day_url_str}))
        schedule_contents = BeautifulSoup(schedule_table.content, features='html.parser')
        self.assertTrue(item_data['title'] in schedule_contents.text)

    def test_edit_schedule_item(self):
        """ Verify the edit schedule item workflow
        """
        schedule_items, schedule_dict = self._add_schedule_items()
        item_to_change = schedule_items[1]
        change_data = {
            'title': 'escape',
            'start_time': get_relevant_time_id('8:00 AM'),
            'end_time': get_relevant_time_id('8:30 AM'),
            'location': 'LA'
        }
        self.client.post(
            reverse('edit_item', kwargs={'item_id': item_to_change.id}),
            change_data
        )
        schedule_table = self.client.get(reverse('get_schedule', kwargs={'datestr': self.day_url_str}))
        schedule_contents = BeautifulSoup(schedule_table.content, features='html.parser')
        for item in schedule_items:
            self.assertTrue(change_data['title'] in schedule_contents.text)

    def test_todo_table(self):
        """ Verify the appearance of the to do list table
        """
        todo_items = self._add_todo_items()
        todo_titles = [item.title for item in todo_items]
        todo_response = self.client.get(reverse('get_todo', kwargs={'datestr': self.day_url_str}))
        todo_content = BeautifulSoup(todo_response.content, features='html.parser')
        rows = todo_content.find_all('tr')
        # there should be exactly one row per item
        # the contents of the rows should contain the item titles
        self.assertEqual(len(rows), len(todo_items))
        for row in rows:
            self.assertTrue(row.find_all('td')[1].text in todo_titles)

    def test_delete_todo_item(self):
        """ Verify the delete view functions for todo items
        """
        todo_items = self._add_todo_items()
        item_to_delete = todo_items[2]

        self.client.get(reverse('delete_todo_item', kwargs={'item_id': item_to_delete.id}))

        todo_response = self.client.get(reverse('get_todo', kwargs={'datestr': self.day_url_str}))
        todo_content = BeautifulSoup(todo_response.content, features='html.parser')
        for item in todo_items:
            if item == item_to_delete:
                self.assertFalse(item.title in todo_content.text)
            else:
                self.assertTrue(item.title in todo_content.text)

    def test_add_todo_item_view(self):
        """ Verify the delete todo item workflow
        """
        todo_list, created = ToDoList.get_or_create(day=self.day, user=self.user.user.rolllistuser)
        test_title = 'make sure this worrrrrrks'
        self.client.post(
            reverse('add_todo_item', kwargs={'list_id': todo_list.id}),
            {
                'title': test_title
            }
        )

        todo_response = self.client.get(reverse('get_todo', kwargs={'datestr': self.day_url_str}))
        todo_content = BeautifulSoup(todo_response.content, features='html.parser')
        self.assertTrue(test_title in todo_content.text)
