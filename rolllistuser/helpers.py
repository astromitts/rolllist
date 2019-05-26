from django.contrib.auth.models import User, Group, Permission


class TestGroup(object):
    def __init__(self, group_name, permission_codes=None):
        self.name = group_name
        if permission_codes is None:
            permission_codes = []
        group, created = Group.objects.get_or_create(name=group_name)

        permission_objs = Permission.objects.filter(codename__in=permission_codes)
        for permission in permission_objs.all():
            group.permissions.add(permission)
        group.save()
        self.group = group


class TestUser(object):
    def __init__(self, username, password, is_superuser=False):
        self.username = username
        self.password = password
        self.email = '%s@example.com' % username
        self.is_superuser = is_superuser

        if is_superuser:
            self.user = User.objects.create_superuser(
                username,
                self.email,
                password
            )
            self.user.save()
        else:
            self.user = User.objects.create_user(
                username,
                self.email,
                password
            )
            self.user.save()

    def set_group(self, group):
        self.user.groups.add(group)
