# Generated by Django 4.2.6 on 2023-10-29 20:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('FitMate', '0002_userprofile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='date_of_birth',
        ),
    ]
