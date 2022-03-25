# Generated by Django 4.0.2 on 2022-03-25 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_page_meta_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parameter',
            name='name',
            field=models.CharField(max_length=50, verbose_name='نام پارامتر (تغییر ندهید)'),
        ),
        migrations.AlterField(
            model_name='parameter',
            name='origin_value',
            field=models.CharField(blank=True, max_length=50000, null=True, verbose_name='مقدار پارامتر'),
        ),
    ]
