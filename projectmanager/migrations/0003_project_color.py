# Generated by Django 3.2.13 on 2022-05-08 22:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projectmanager', '0002_alter_project_parent'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='color',
            field=models.CharField(choices=[('success', 'success'), ('danger', 'danger'), ('warning', 'warning'), ('primary', 'primary'), ('muted', 'muted'), ('secondary', 'secondary'), ('info', 'info'), ('light', 'light'), ('rose', 'rose'), ('dark', 'dark')], default='primary', max_length=50, verbose_name='color'),
        ),
    ]
