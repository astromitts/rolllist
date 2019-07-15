from bs4 import BeautifulSoup

from django.urls import reverse

from project.helpers import TestBaseWithScheduleData
from rolllist.utils import get_relevant_time_id


class TestDashboardViews(TestBaseWithScheduleData):
    """ Test Cases that use the django test client to go to specific views
        and verify their content based on known data

        TODO this is pretty brittle and will need to be updated with any
        HTML / template changes but whatcha gonna do?
    """

    def test_dashboard_loads(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_schedule_table(self):
        """ Verify the appearance of scheduled items in the schedule table view
        """
        schedule_items, schedule_dict = self._add_schedule_items()
        schedule_table = self.client.get(reverse('get_schedule', kwargs={'datestr': self.day_url_str}))
        schedule_contents = BeautifulSoup(schedule_table.content, features='html.parser')
        schedule_rows = schedule_contents.find_all('div', {'class': 'schedulerow'})
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

    def test_todo_table(self):
        """ Verify the appearance of the to do list table
        """
        todo_items = self._add_todo_items()
        todo_titles = [item.title for item in todo_items]
        todo_response = self.client.get(reverse('get_todo', kwargs={'datestr': self.day_url_str}))
        todo_content = BeautifulSoup(todo_response.content, features='html.parser')
        rows = todo_content.find_all('div', {'class': 'helper_todoitem'})
        # there should be exactly one row per item
        # the contents of the rows should contain the item titles
        self.assertEqual(len(rows), len(todo_items))
        for row in rows:
            title = row.find('span', {'class': 'helper_todoitem--title'})
            self.assertTrue(title.text.strip() in todo_titles)

    def test_todo_table_rollover(self):
        """ Verify the appearance of the to do list table
        """

        new_todo_items = self._add_todo_items()
        rollover_todo_items = self._backfill_todo_items_for_previous_day()

        rollover_response = self.client.get(reverse('rollover_todo', kwargs={'datestr': self.day_url_str}))
        self.assertEqual(rollover_response.status_code, 200)

        todo_response = self.client.get(reverse('get_todo', kwargs={'datestr': self.day_url_str}))
        todo_content = BeautifulSoup(todo_response.content, features='html.parser')
        todo_titles = [node.text for node in todo_content.find_all('span', {'class': 'helper_todoitem--title'})]

        # there should be exactly one row per item
        # the contents of the rows should contain the item titles
        self.assertEqual(len(todo_titles), len(new_todo_items) + len(rollover_todo_items))
        for todo in new_todo_items:
            self.assertTrue(todo.title in todo_titles)

        for todo in rollover_todo_items:
            self.assertTrue(todo.title in todo_titles)

    def test_notes_view(self):
        test_notes = self._add_notes()
        note_view = self.client.get(reverse('get_notes', kwargs={'datestr': self.day_url_str}))
        notes_content = BeautifulSoup(note_view.content, features='html.parser')
        rendered_notes = [node.text for node in notes_content.find_all('div', {'class': 'helper_notescontent'})]
        for note in test_notes:
            self.assertTrue(note.content in rendered_notes)
