from django.db import models

from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from rolllist.utils import time_options_strings


class RollListUser(models.Model):
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
    """ Handler for custom user creation logic
    """
    if created:
        instance.groups.add(Group.objects.get(name='public_users'))
        rolllist_user = RollListUser(user=instance)
        rolllist_user.save()
    else:
        pass


post_save.connect(user_post_signal, sender=User)
