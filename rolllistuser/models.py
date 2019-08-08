from django.db import models

from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from rolllist.utils import time_options_strings

todo_style_choices = [
    ('checkbox', 'Checkbox style'),
    ('kanban', 'Kanban style'),
]


class RollListUser(models.Model):
    """ Model for managing application settings per user.
        Created automatically via user_post_signal when a new User is saved
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    schedule_start_time = models.IntegerField(
        choices=[
            (i, time_options_strings[i]) for i in range(0, len(time_options_strings))
        ],
        default=time_options_strings.index('8:00 AM')
    )
    schedule_end_time = models.IntegerField(
        choices=[
            (i, time_options_strings[i]) for i in range(0, len(time_options_strings))
        ],
        default=time_options_strings.index('6:30 PM')
    )
    todo_style = models.CharField(
        choices=todo_style_choices,
        max_length=120
    )

    def __str__(self):
        if self.user.username:
            return '%s // %s' % (self.user.username, self.user.email)
        return '%s' % (self.user.email)

    @property
    def schedule_start(self):
        """ Front end helper to display human version of start time interval """
        return time_options_strings[self.schedule_start_time]

    @property
    def schedule_end(self):
        """ Front end helper to display human version of end time interval """
        return time_options_strings[self.schedule_end_time]


def user_post_signal(sender, instance, created, **kwargs):
    """ Handler for custom user creation logic - adds new user to the
        public_users group  and creates a new associated RollListUser instance
    """
    if created:
        public_users_group, created = Group.objects.get_or_create(name='public_users')
        instance.groups.add(public_users_group)
        rolllist_user = RollListUser(user=instance)
        rolllist_user.save()
    else:
        pass


post_save.connect(user_post_signal, sender=User)
