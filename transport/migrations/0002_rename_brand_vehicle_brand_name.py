# Generated by Django 3.2.13 on 2022-06-01 20:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transport', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vehicle',
            old_name='brand',
            new_name='brand_name',
        ),
    ]
