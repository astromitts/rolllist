# Generated by Django 2.2.1 on 2019-07-02 14:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rolllist', '0009_auto_20190604_1834'),
    ]

    operations = [
        migrations.AddField(
            model_name='scheduleitem',
            name='recurrance',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='rolllist.RecurringScheduleItem'),
        ),
    ]
