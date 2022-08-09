# Generated by Django 3.2.13 on 2022-08-09 23:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0004_alter_warehousesheetsignature_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='warehousesheetsignature',
            name='status',
            field=models.CharField(choices=[('پیش نویس', 'پیش نویس'), ('DEFAULT', 'DEFAULT'), ('تعریف اولیه در سیستم', 'تعریف اولیه در سیستم'), ('تحویل شده', 'تحویل شده'), ('در حال تست', 'در حال تست'), ('در حال انجام', 'در حال انجام'), ('رد شده', 'رد شده'), ('پذیرفته شده', 'پذیرفته شده'), ('درخواست شده', 'درخواست شده'), ('آماده برای خرید', 'آماده برای خرید'), ('در حال خرید', 'در حال خرید'), ('متعلق به کارفرما', 'متعلق به کارفرما'), ('موجود در انبار', 'موجود در انبار'), ('خارج شده از انبار', 'خارج شده از انبار'), ('وارد شده به انبار', 'وارد شده به انبار'), ('تحویل گرفته شده از کارفرما', 'تحویل گرفته شده از کارفرما'), ('پرداخت شده', 'پرداخت شده')], default='درخواست شده', max_length=200, verbose_name='status'),
        ),
    ]
