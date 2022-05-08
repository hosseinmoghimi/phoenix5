# Generated by Django 3.2.13 on 2022-05-06 19:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mafia', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GameAct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('night', models.IntegerField(verbose_name='night?')),
                ('act', models.CharField(max_length=50, verbose_name='act')),
                ('acted', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mafia.roleplayer', verbose_name='acted_acts')),
                ('actor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='actor_acts', to='mafia.roleplayer', verbose_name='role_player')),
            ],
            options={
                'verbose_name': 'GameAct',
                'verbose_name_plural': 'GameActs',
            },
        ),
    ]
