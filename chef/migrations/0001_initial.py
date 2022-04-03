# Generated by Django 4.0.2 on 2022-03-31 23:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0009_tag_pagetag'),
    ]

    operations = [
        migrations.CreateModel(
            name='Food',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.page')),
            ],
            options={
                'verbose_name': 'Food',
                'verbose_name_plural': 'Food',
            },
            bases=('core.page',),
        ),
    ]
