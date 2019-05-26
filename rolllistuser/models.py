from django.db import models

from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save


class RollListUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)

    def __str__(self):
        return self.user.username


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
