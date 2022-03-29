# Generated by Django 4.0.2 on 2022-03-28 12:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0009_remove_warehouse_owner_remove_warehouse_page_ptr_and_more'),
        ('guarantee', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='guarantee',
            name='invoice',
            field=models.ForeignKey(default=98, on_delete=django.db.models.deletion.CASCADE, to='accounting.invoice', verbose_name='فاکتور'),
            preserve_default=False,
        ),
    ]
