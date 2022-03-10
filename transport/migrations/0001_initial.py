# Generated by Django 4.0.2 on 2022-03-10 17:22

from django.db import migrations, models
import django.db.models.deletion
import utility.utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authentication', '0002_profilecontact_membershiprequest'),
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50, verbose_name='code')),
                ('name', models.CharField(max_length=50, verbose_name='area')),
            ],
            options={
                'verbose_name': 'Area',
                'verbose_name_plural': 'Areas',
            },
            bases=(models.Model, utility.utils.LinkHelper),
        ),
        migrations.CreateModel(
            name='ServiceMan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True, verbose_name='نام تعمیرگاه')),
                ('address', models.CharField(blank=True, max_length=50, null=True, verbose_name='address')),
                ('tel', models.CharField(blank=True, max_length=50, null=True, verbose_name='tel')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.profile', verbose_name='profile')),
            ],
            options={
                'verbose_name': 'ServiceMan',
                'verbose_name_plural': 'ServiceMans',
            },
            bases=(models.Model, utility.utils.LinkHelper),
        ),
        migrations.CreateModel(
            name='Passenger',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.profile', verbose_name='profile')),
            ],
            options={
                'verbose_name': 'Passenger',
                'verbose_name_plural': 'Passengers',
            },
            bases=(models.Model, utility.utils.LinkHelper),
        ),
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='title')),
                ('color', models.CharField(choices=[('success', 'success'), ('danger', 'danger'), ('warning', 'warning'), ('primary', 'primary'), ('secondary', 'secondary'), ('info', 'info'), ('light', 'light'), ('rose', 'rose'), ('dark', 'dark')], default='primary', max_length=50, verbose_name='color')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.profile', verbose_name='profile')),
            ],
            options={
                'verbose_name': 'Driver',
                'verbose_name_plural': 'Drivers',
            },
            bases=(models.Model, utility.utils.LinkHelper),
        ),
    ]
