# Generated by Django 4.2.4 on 2024-03-15 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FitMate', '0021_remove_progressdata_notes'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='points',
            field=models.IntegerField(default=0),
        ),
    ]
