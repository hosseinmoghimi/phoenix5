# Generated by Django 4.0.2 on 2022-04-01 10:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0012_alter_account_app_name_alter_account_class_name'),
        ('guarantee', '0002_guarantee_invoice'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='guarantee',
            name='invoice',
        ),
        migrations.AddField(
            model_name='guarantee',
            name='invoice_line',
            field=models.ForeignKey(default=52, on_delete=django.db.models.deletion.CASCADE, to='accounting.invoiceline', verbose_name='ردیف فاکتور'),
            preserve_default=False,
        ),
    ]
