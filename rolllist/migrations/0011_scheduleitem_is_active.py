# Generated by Django 2.2.1 on 2019-07-02 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rolllist', '0010_scheduleitem_recurrance'),
    ]

    operations = [
        migrations.AddField(
            model_name='scheduleitem',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
