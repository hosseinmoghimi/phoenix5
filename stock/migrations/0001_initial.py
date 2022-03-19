# Generated by Django 4.0.2 on 2022-03-19 00:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounting', '0001_initial'),
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShareHolder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stock', models.IntegerField(verbose_name='میزان مشارکت')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounting.account', verbose_name='account')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.profile', verbose_name='profile')),
            ],
            options={
                'verbose_name': 'ShareHolder',
                'verbose_name_plural': 'ShareHolders',
            },
        ),
    ]
