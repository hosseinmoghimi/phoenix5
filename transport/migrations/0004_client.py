# Generated by Django 4.0.2 on 2022-04-02 21:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0013_alter_financialdocument_color_and_more'),
        ('transport', '0003_trippath_area'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('account_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='accounting.account')),
            ],
            options={
                'verbose_name': 'Client',
                'verbose_name_plural': 'Client',
            },
            bases=('accounting.account',),
        ),
    ]
