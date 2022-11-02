# Generated by Django 4.1 on 2022-11-02 08:58

from django.db import migrations, models
import django.db.models.deletion
import utility.utils


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0024_alter_invoiceline_row'),
        ('health', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Disease',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('level', models.IntegerField(verbose_name='level')),
                ('color', models.CharField(choices=[('success', 'success'), ('danger', 'danger'), ('warning', 'warning'), ('primary', 'primary'), ('muted', 'muted'), ('secondary', 'secondary'), ('info', 'info'), ('light', 'light'), ('rose', 'rose'), ('dark', 'dark')], default='primary', max_length=50, verbose_name='color')),
                ('drugs', models.ManyToManyField(blank=True, to='health.drug', verbose_name='drugs')),
            ],
            options={
                'verbose_name': 'Disease',
                'verbose_name_plural': 'Diseases',
            },
            bases=(models.Model, utility.utils.LinkHelper),
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounting.account', verbose_name='account')),
            ],
            options={
                'verbose_name': 'Doctor',
                'verbose_name_plural': 'Doctors',
            },
            bases=(models.Model, utility.utils.LinkHelper),
        ),
        migrations.CreateModel(
            name='Visit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('visit_datetime', models.DateTimeField(verbose_name='visit')),
                ('description', models.CharField(blank=True, max_length=500, null=True, verbose_name='description')),
                ('diseases', models.ManyToManyField(blank=True, to='health.disease', verbose_name='diseases')),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='health.doctor', verbose_name='doctor')),
                ('drugs', models.ManyToManyField(blank=True, to='health.drug', verbose_name='drug')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='health.patient', verbose_name='patient')),
            ],
            options={
                'verbose_name': 'Visit',
                'verbose_name_plural': 'Visits',
            },
            bases=(models.Model, utility.utils.LinkHelper),
        ),
    ]
