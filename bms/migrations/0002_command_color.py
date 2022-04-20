# Generated by Django 4.0.2 on 2022-04-20 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bms', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='command',
            name='color',
            field=models.CharField(choices=[('success', 'success'), ('danger', 'danger'), ('warning', 'warning'), ('primary', 'primary'), ('muted', 'muted'), ('secondary', 'secondary'), ('info', 'info'), ('light', 'light'), ('rose', 'rose'), ('dark', 'dark')], default='primary', max_length=50, verbose_name='color'),
        ),
    ]
