# Generated by Django 3.2.13 on 2022-05-20 00:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='tax_percent',
            field=models.IntegerField(default=0, verbose_name='درصد مالیات'),
        ),
    ]
