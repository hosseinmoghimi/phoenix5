# Generated by Django 4.0.2 on 2022-04-02 14:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0003_alter_appointment_location'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointment',
            name='location',
        ),
    ]
