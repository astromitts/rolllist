from django.test import TestCase
from django.urls import reverse

from django.contrib.auth.models import User

from project.settings import NON_STAFF_PERMS
from rolllistuser.helpers import TestGroup, TestUser


class BaseUserTest(TestCase):
    """ Base class for running app tests that need an existing user set up """

    def setUp(self):
        user_group = TestGroup(
            group_name='public_users',
            permission_codes=NON_STAFF_PERMS,
        )

        self.user = TestUser('tester', 'asdf1234')
        self.user.set_group(user_group.group)


class TestRollListUser(TestCase):

    def test_user_save_signal(self):
        """ Verify a RollListUser object is created upon saving a new User """
        user = User.objects.create_user(
            username='test',
            email='test@example.com',
            password='asdf1234'
        )
        user.save()
        self.assertTrue(user.rolllistuser)


class TestUserViews(BaseUserTest):
    def test_login_process(self):
        """ Verify login view behavior
        """
        login_url = reverse('login_handler')
        login_data = {
            'email': self.user.email,
            'password': self.user.password,
        }
        response = self.client.post(login_url, login_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('dashboard'))

    def test_login_password_error(self):
        """ Verify succesful login
        """
        login_url = reverse('login_handler')
        login_data = {
            'email': self.user.email,
            'password': 'boourns',
        }
        response = self.client.post(login_url, login_data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('invalid password' in str(response.content))

    def test_login_email_error(self):
        """ Verify succesful login
        """
        login_url = reverse('login_handler')
        login_data = {
            'email': 'boourns@fake.com',
            'password': self.user.password,
        }
        response = self.client.post(login_url, login_data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('invalid email' in str(response.content))


class TestUserRegister(TestCase):
    """ Verify register vew behavior
    """
    def test_register_success(self):
        register_url = reverse('create_user_handler')
        register_data = {
            'username': 'burgerbob',
            'email': 'bob@warfarts.com',
            'password': 'jimmypestosucks',
        }

        response = self.client.post(register_url, register_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('dashboard'))

    def test_register_error(self):
        register_url = reverse('create_user_handler')
        register_data = {
            'email': 'bob@warfarts.com',
            'password': 'jimmypestosucks',
        }

        response = self.client.post(register_url, register_data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('field is required' in str(response.context))

    def test_dupe_user(self):
        existing_user = TestUser('tester', 'asdf1234')
        register_url = reverse('create_user_handler')
        register_data = {
            'username': 'tester',
            'email': 'bob@warfarts.com',
            'password': 'jimmypestosucks',
        }

        response = self.client.post(register_url, register_data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('username already exists' in str(response.context))
