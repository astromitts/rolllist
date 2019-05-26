from django.test import TestCase

from rolllist.models.appmodels import Day


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
