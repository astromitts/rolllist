# Generated by Django 2.2.1 on 2019-05-26 17:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rolllistuser', '0002_make_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rolllistuser',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]