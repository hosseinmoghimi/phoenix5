# Generated by Django 4.1.3 on 2022-12-19 22:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loyaltyclub', '0002_payment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='title',
        ),
    ]
