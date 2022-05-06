# Generated by Django 3.2.13 on 2022-05-06 11:13

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
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='date_added')),
            ],
            options={
                'verbose_name': 'Game',
                'verbose_name_plural': 'Games',
            },
            bases=(models.Model, utility.utils.LinkHelper),
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.profile', verbose_name='profile')),
            ],
            options={
                'verbose_name': 'Player',
                'verbose_name_plural': 'Players',
            },
            bases=(models.Model, utility.utils.LinkHelper),
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.page')),
                ('side', models.CharField(choices=[('مافیا', 'مافیا'), ('شهروند', 'شهروند'), ('مستقل', 'مستقل')], max_length=50, verbose_name='side')),
            ],
            options={
                'verbose_name': 'Role',
                'verbose_name_plural': 'Roles',
            },
            bases=('core.page',),
        ),
        migrations.CreateModel(
            name='RolePlayer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mafia.game', verbose_name='game')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mafia.player', verbose_name='player')),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mafia.role', verbose_name='role')),
            ],
            options={
                'verbose_name': 'RolePlayer',
                'verbose_name_plural': 'RolePlayers',
            },
        ),
        migrations.CreateModel(
            name='Leage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='title')),
                ('games', models.ManyToManyField(to='mafia.Game', verbose_name='game')),
            ],
            options={
                'verbose_name': 'Leage',
                'verbose_name_plural': 'Leages',
            },
            bases=(models.Model, utility.utils.LinkHelper),
        ),
        migrations.CreateModel(
            name='God',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.profile', verbose_name='profile')),
            ],
            options={
                'verbose_name': 'God',
                'verbose_name_plural': 'Gods',
            },
            bases=(models.Model, utility.utils.LinkHelper),
        ),
        migrations.CreateModel(
            name='GameScenario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='title')),
                ('description', models.CharField(blank=True, max_length=5000, null=True, verbose_name='description')),
                ('roles', models.ManyToManyField(to='mafia.Role', verbose_name='roles')),
            ],
            options={
                'verbose_name': 'GameScenario',
                'verbose_name_plural': 'GameScenarios',
            },
            bases=(models.Model, utility.utils.LinkHelper),
        ),
        migrations.AddField(
            model_name='game',
            name='game_scenario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mafia.gamescenario', verbose_name='scenario'),
        ),
        migrations.AddField(
            model_name='game',
            name='god',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mafia.god', verbose_name='god'),
        ),
    ]
