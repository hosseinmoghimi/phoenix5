# Generated by Django 4.0.2 on 2022-03-04 21:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile', models.CharField(blank=True, max_length=50, null=True, verbose_name='mobile')),
                ('bio', models.CharField(blank=True, max_length=50, null=True, verbose_name='bio')),
                ('address', models.CharField(blank=True, max_length=50, null=True, verbose_name='address')),
                ('image_origin', models.ImageField(blank=True, null=True, upload_to='authentication/images/profile/', verbose_name='image')),
                ('header_origin', models.ImageField(blank=True, null=True, upload_to='authentication/images/profile/header/', verbose_name='header_origin')),
                ('enabled', models.BooleanField(default=True, verbose_name='enabled')),
                ('can_login', models.BooleanField(default=False, verbose_name='can login ?')),
                ('status', models.CharField(choices=[('AAA', 'AAA'), ('BBB', 'BBB')], default='AAA', max_length=50, verbose_name='status')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Profile',
                'verbose_name_plural': 'Profiles',
            },
        ),
    ]
