# Generated by Django 4.2.4 on 2023-11-23 21:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FitMate', '0009_userprofile_age_userprofile_allergies_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='suggested_workout',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]