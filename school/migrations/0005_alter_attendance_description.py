# Generated by Django 4.1 on 2022-11-01 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0004_alter_attendance_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='description',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='description'),
        ),
    ]
