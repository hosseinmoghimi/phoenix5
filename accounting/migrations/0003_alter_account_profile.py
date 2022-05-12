# Generated by Django 3.2.13 on 2022-05-12 07:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
        ('accounting', '0002_auto_20220511_1142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='profile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='authentication.profile', verbose_name='profile'),
        ),
    ]
