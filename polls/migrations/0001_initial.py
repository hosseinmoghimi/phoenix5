# Generated by Django 3.2.13 on 2022-05-22 14:05

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
            name='Option',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='title')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.profile', verbose_name='creator')),
            ],
            options={
                'verbose_name': 'Option',
                'verbose_name_plural': 'Options',
            },
            bases=(models.Model, utility.utils.LinkHelper),
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('option', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.option', verbose_name='option')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.profile', verbose_name='profile')),
            ],
            options={
                'verbose_name': 'Vote',
                'verbose_name_plural': 'Votes',
            },
            bases=(models.Model, utility.utils.LinkHelper),
        ),
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.page')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.profile', verbose_name='creator')),
            ],
            options={
                'verbose_name': 'Poll',
                'verbose_name_plural': 'Polls',
            },
            bases=('core.page',),
        ),
        migrations.AddField(
            model_name='option',
            name='poll',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.poll', verbose_name='poll'),
        ),
    ]
