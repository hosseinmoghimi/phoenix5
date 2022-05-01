# Generated by Django 3.2.13 on 2022-05-01 05:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500, verbose_name='title')),
                ('description', models.CharField(blank=True, max_length=50000, null=True, verbose_name='description')),
                ('app_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='app_name')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='date_added')),
            ],
            options={
                'verbose_name': 'Log',
                'verbose_name_plural': 'Logs',
            },
        ),
    ]
