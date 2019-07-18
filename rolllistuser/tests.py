from django.test import TestCase
from django.urls import reverse

from django.contrib.auth.models import User

from project.settings import NON_STAFF_PERMS
from project.helpers import TestAlertsMixin
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


class TestUserViews(BaseUserTest, TestAlertsMixin):
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
        self.assertMessageSent('Invalid password.', response)

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
        self.assertMessageSent('Invalid email.', response)


class TestUserRegister(TestCase, TestAlertsMixin):
    """ Verify register vew behavior
    """
    def test_register_success(self):
        register_url = reverse('create_user_handler')
        register_data = {
            'email': 'bob@warfarts.com',
            'password': 'jimmypestosucks',
            'verify_password': 'jimmypestosucks',
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
        existing_user = TestUser('bob@warfarts.com', 'asdf1234')  # noqa
        register_url = reverse('create_user_handler')
        register_data = {
            'email': existing_user.email,
            'password': 'jimmypestosucks',
            'verify_password': 'jimmypestosucks',
        }

        response = self.client.post(register_url, register_data)
        self.assertEqual(response.status_code, 200)
        self.assertMessageSent('This email address is already in use.', response)


class TestUserProfileEdit(BaseUserTest, TestAlertsMixin):
    def setUp(self):
        super(TestUserProfileEdit, self).setUp()
        self.user.login(self.client)
        self.bad_password = 'notmypassword'
        self.init_start_schedule_time = self.user.user.rolllistuser.schedule_start_time
        self.init_end_schedule_time = self.user.user.rolllistuser.schedule_end_time

        self.new_schedule_start_time = self.user.user.rolllistuser.schedule_start_time + 3
        self.new_schedule_end_time = self.user.user.rolllistuser.schedule_start_time - 2

        self.new_email = 'tester2@example.com'

    def test_bad_password(self):
        result = self.client.post(
            reverse('user_profile'),
            {
                'password': self.bad_password,
                'email': self.new_email,
                'schedule_start_time': self.new_schedule_start_time,
                'schedule_end_time': self.new_schedule_end_time,
            }
        )
        self.assertEqual(result.status_code, 200)
        self.assertMessageSent('Current correct password required to make user profile changes.', result)
        user_obj = User.objects.get(pk=1)

        # nothing changed....
        self.assertEqual(user_obj.rolllistuser.schedule_start_time, self.init_start_schedule_time)
        self.assertEqual(user_obj.rolllistuser.schedule_end_time, self.init_end_schedule_time)
        self.assertEqual(user_obj.email, self.user.email)

    def test_profile_update(self):
        result = self.client.post(
            reverse('user_profile'),
            {
                'password': self.user.password,
                'email': self.new_email,
                'schedule_start_time': self.new_schedule_start_time,
                'schedule_end_time': self.new_schedule_end_time,
            }
        )
        self.assertEqual(result.status_code, 200)
        expected_message = 'Updated user information.'
        self.assertIn(expected_message, [m.message for m in result.context['messages']._loaded_messages])
        user_obj = User.objects.get(pk=1)

        # nothing changed....
        self.assertEqual(user_obj.rolllistuser.schedule_start_time, self.new_schedule_start_time)
        self.assertEqual(user_obj.rolllistuser.schedule_end_time, self.new_schedule_end_time)
        self.assertEqual(user_obj.email, self.new_email)


class TestUserChangePassword(BaseUserTest, TestAlertsMixin):
    def setUp(self):
        super(TestUserChangePassword, self).setUp()
        self.user.login(self.client)
        self.bad_password = 'notmypassword'
        self.new_password = 'thisismypassword'
        self.mismatched_password = 'thisisnotmypassword'

    def test_bad_password_error(self):
        result = self.client.post(
            reverse('user_change_password'),
            {
                'password': self.bad_password
            }
        )
        self.assertEqual(result.status_code, 200)
        self.assertMessageSent('Current correct password required to make user profile changes.', result)

    def test_bad_password_match(self):
        result = self.client.post(
            reverse('user_change_password'),
            {
                'password': self.user.password,
                'new_password': self.new_password,
                'verify_password': self.mismatched_password
            }
        )
        self.assertEqual(result.status_code, 200)
        self.assertMessageSent('New password fields must match.', result)

    def test_change_password_works(self):
        change_password_post = self.client.post(
            reverse('user_change_password'),
            {
                'password': self.user.password,
                'new_password': self.new_password,
                'verify_password': self.new_password
            }
        )
        self.assertEqual(change_password_post.status_code, 302, 'redirect to login page')
        self.assertTrue('login' in change_password_post.url)
        login_post = self.client.post(
            reverse('login_handler'),
            {
                'email': self.user.email,
                'password': self.new_password,
            }
        )
        self.assertEqual(login_post.status_code, 302, 'redirect to dashboard')
        self.assertEqual(login_post.url, reverse('dashboard'))
