# Generated by Django 2.2.1 on 2019-05-22 19:57

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Day',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.datetime.today, unique=True)),
            ],
            options={
                'ordering': ['date'],
            },
        ),
        migrations.CreateModel(
            name='ToDoList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rolled_over', models.BooleanField(default=False)),
                ('day', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rolllist.Day')),
            ],
        ),
        migrations.CreateModel(
            name='ToDoItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('completed', models.BooleanField(default=False)),
                ('to_do_list', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rolllist.ToDoList')),
            ],
        ),
        migrations.CreateModel(
            name='ScheduleItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('start_time', models.IntegerField(choices=[(0, '12:00 AM'), (1, '12:30 AM'), (2, '1:00 AM'), (3, '1:30 AM'), (4, '2:00 AM'), (5, '2:30 AM'), (6, '3:00 AM'), (7, '3:30 AM'), (8, '4:00 AM'), (9, '4:30 AM'), (10, '5:00 AM'), (11, '5:30 AM'), (12, '6:00 AM'), (13, '6:30 AM'), (14, '7:00 AM'), (15, '7:30 AM'), (16, '8:00 AM'), (17, '8:30 AM'), (18, '9:00 AM'), (19, '9:30 AM'), (20, '10:00 AM'), (21, '10:30 AM'), (22, '11:00 AM'), (23, '11:30 AM'), (24, '12:00 PM'), (25, '12:30 PM'), (26, '1:00 PM'), (27, '1:30 PM'), (28, '2:00 PM'), (29, '2:30 PM'), (30, '3:00 PM'), (31, '3:30 PM'), (32, '4:00 PM'), (33, '4:30 PM'), (34, '5:00 PM'), (35, '5:30 PM'), (36, '6:00 PM'), (37, '6:30 PM'), (38, '7:00 PM'), (39, '7:30 PM'), (40, '8:00 PM'), (41, '8:30 PM'), (42, '9:00 PM'), (43, '9:30 PM'), (44, '10:00 PM'), (45, '10:30 PM'), (46, '11:00 PM'), (47, '11:30 PM')])),
                ('end_time', models.IntegerField(choices=[(0, '12:00 AM'), (1, '12:30 AM'), (2, '1:00 AM'), (3, '1:30 AM'), (4, '2:00 AM'), (5, '2:30 AM'), (6, '3:00 AM'), (7, '3:30 AM'), (8, '4:00 AM'), (9, '4:30 AM'), (10, '5:00 AM'), (11, '5:30 AM'), (12, '6:00 AM'), (13, '6:30 AM'), (14, '7:00 AM'), (15, '7:30 AM'), (16, '8:00 AM'), (17, '8:30 AM'), (18, '9:00 AM'), (19, '9:30 AM'), (20, '10:00 AM'), (21, '10:30 AM'), (22, '11:00 AM'), (23, '11:30 AM'), (24, '12:00 PM'), (25, '12:30 PM'), (26, '1:00 PM'), (27, '1:30 PM'), (28, '2:00 PM'), (29, '2:30 PM'), (30, '3:00 PM'), (31, '3:30 PM'), (32, '4:00 PM'), (33, '4:30 PM'), (34, '5:00 PM'), (35, '5:30 PM'), (36, '6:00 PM'), (37, '6:30 PM'), (38, '7:00 PM'), (39, '7:30 PM'), (40, '8:00 PM'), (41, '8:30 PM'), (42, '9:00 PM'), (43, '9:30 PM'), (44, '10:00 PM'), (45, '10:30 PM'), (46, '11:00 PM'), (47, '11:30 PM')])),
                ('location', models.CharField(max_length=150, null=True)),
                ('day', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rolllist.Day')),
            ],
            options={
                'ordering': ['start_time'],
            },
        ),
    ]
