# Generated by Django 4.2.4 on 2024-02-28 22:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('FitMate', '0020_remove_progressdata_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='progressdata',
            name='notes',
        ),
    ]