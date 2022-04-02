# Generated by Django 4.0.2 on 2022-04-02 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0012_alter_account_app_name_alter_account_class_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='financialdocument',
            name='color',
            field=models.CharField(choices=[('success', 'success'), ('danger', 'danger'), ('warning', 'warning'), ('primary', 'primary'), ('muted', 'muted'), ('secondary', 'secondary'), ('info', 'info'), ('light', 'light'), ('rose', 'rose'), ('dark', 'dark')], default='primary', max_length=50, verbose_name='color'),
        ),
        migrations.AlterField(
            model_name='transactioncategory',
            name='color_origin',
            field=models.CharField(blank=True, choices=[('success', 'success'), ('danger', 'danger'), ('warning', 'warning'), ('primary', 'primary'), ('muted', 'muted'), ('secondary', 'secondary'), ('info', 'info'), ('light', 'light'), ('rose', 'rose'), ('dark', 'dark')], max_length=50, null=True, verbose_name='color'),
        ),
    ]
