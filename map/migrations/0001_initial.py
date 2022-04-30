# Generated by Django 3.2.13 on 2022-04-30 00:10

from django.db import migrations, models
import django.db.models.deletion
import utility.utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authentication', '0001_initial'),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='title')),
                ('code', models.CharField(max_length=50, verbose_name='code')),
                ('area', models.CharField(blank=True, max_length=1000, null=True, verbose_name='area')),
                ('color', models.CharField(choices=[('success', 'success'), ('danger', 'danger'), ('warning', 'warning'), ('primary', 'primary'), ('muted', 'muted'), ('secondary', 'secondary'), ('info', 'info'), ('light', 'light'), ('rose', 'rose'), ('dark', 'dark')], default='primary', max_length=50, verbose_name='color')),
            ],
            options={
                'verbose_name': 'Area',
                'verbose_name_plural': 'Areas',
            },
            bases=(models.Model, utility.utils.LinkHelper),
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='عنوان نقطه')),
                ('location', models.CharField(max_length=1000, verbose_name='لوکیشن')),
                ('latitude', models.CharField(blank=True, max_length=50, null=True, verbose_name='latitude')),
                ('longitude', models.CharField(blank=True, max_length=50, null=True, verbose_name='longitude')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='date_added')),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='maplocation_set', to='authentication.profile', verbose_name='profile')),
            ],
            options={
                'verbose_name': 'لوکیشن',
                'verbose_name_plural': 'لوکیشن ها',
            },
            bases=(models.Model, utility.utils.LinkHelper),
        ),
        migrations.CreateModel(
            name='PageLocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='date_added')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='map.location', verbose_name='location')),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.page', verbose_name='page')),
            ],
            options={
                'verbose_name': 'PageLocation',
                'verbose_name_plural': 'PageLocations',
            },
            bases=(models.Model, utility.utils.LinkHelper),
        ),
    ]
