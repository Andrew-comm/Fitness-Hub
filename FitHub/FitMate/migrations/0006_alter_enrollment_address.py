# Generated by Django 4.2.4 on 2023-11-20 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FitMate', '0005_membershipplan_trainer_enrollment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enrollment',
            name='address',
            field=models.CharField(max_length=30),
        ),
    ]