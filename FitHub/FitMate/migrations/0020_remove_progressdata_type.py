# Generated by Django 4.2.4 on 2024-02-28 18:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('FitMate', '0019_progressdata_remove_workout_user_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='progressdata',
            name='type',
        ),
    ]
