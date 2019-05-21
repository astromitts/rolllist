# Generated by Django 2.2.1 on 2019-05-21 15:37

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timelord', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='scheduleitem',
            name='location',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='day',
            name='date',
            field=models.DateField(default=datetime.datetime.today),
        ),
    ]