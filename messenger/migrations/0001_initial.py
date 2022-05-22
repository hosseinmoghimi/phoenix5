# Generated by Django 3.2.13 on 2022-05-22 14:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='title')),
                ('image_origin', models.ImageField(blank=True, null=True, upload_to='messenger/images/channel/', verbose_name='image')),
                ('description', models.CharField(blank=True, max_length=500, null=True, verbose_name='description')),
                ('channel_name', models.CharField(max_length=20, verbose_name='channel_name')),
                ('app_id', models.CharField(max_length=20, verbose_name='app_id')),
                ('key', models.CharField(max_length=50, verbose_name='key')),
                ('secret', models.CharField(max_length=50, verbose_name='secret')),
                ('cluster', models.CharField(default='us2', max_length=20, verbose_name='cluster')),
            ],
            options={
                'verbose_name': 'Channel',
                'verbose_name_plural': 'Channels',
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='title')),
                ('body', models.CharField(max_length=50, verbose_name='body')),
                ('event', models.CharField(max_length=50, verbose_name='event')),
                ('date_send', models.DateTimeField(auto_now_add=True, verbose_name='date send')),
                ('channel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='messenger.channel', verbose_name='channel')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.profile', verbose_name='sender')),
            ],
            options={
                'verbose_name': 'Message',
                'verbose_name_plural': 'Messages',
            },
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event', models.CharField(default='DEFAULT', max_length=50, verbose_name='event')),
                ('date_join', models.DateTimeField(verbose_name='date join')),
                ('channel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='messenger.channel', verbose_name='channel')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.profile', verbose_name='profile')),
            ],
            options={
                'verbose_name': 'Member',
                'verbose_name_plural': 'Members',
            },
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('message_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='messenger.message')),
                ('read', models.BooleanField(default=False, verbose_name='read')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='messenger.member', verbose_name='member')),
            ],
            bases=('messenger.message',),
        ),
    ]
