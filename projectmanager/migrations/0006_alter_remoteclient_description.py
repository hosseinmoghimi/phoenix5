# Generated by Django 4.1.7 on 2023-05-27 02:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projectmanager', '0005_remoteclient_project_remote_clients'),
    ]

    operations = [
        migrations.AlterField(
            model_name='remoteclient',
            name='description',
            field=models.TextField(blank=True, max_length=2000, null=True, verbose_name='description'),
        ),
    ]
