# Generated by Django 3.2.13 on 2022-05-01 05:03

from django.db import migrations, models
import django.db.models.deletion
import tinymce.models
import utility.utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounting', '0001_initial'),
        ('authentication', '0001_initial'),
        ('core', '0001_initial'),
        ('organization', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='WareHouse',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.page')),
                ('address', models.CharField(blank=True, max_length=50, null=True, verbose_name='address')),
                ('tel', models.CharField(blank=True, max_length=50, null=True, verbose_name='tel')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounting.account', verbose_name='account')),
            ],
            options={
                'verbose_name': 'WareHouse',
                'verbose_name_plural': 'WareHouses',
            },
            bases=('core.page',),
        ),
        migrations.CreateModel(
            name='WareHouseSheet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='date_added')),
                ('date_registered', models.DateTimeField(verbose_name='date_registered')),
                ('quantity', models.IntegerField(verbose_name='quantity')),
                ('unit_name', models.CharField(choices=[('عدد', 'عدد'), ('گرم', 'گرم'), ('کیلوگرم', 'کیلوگرم'), ('تن', 'تن'), ('متر', 'متر'), ('متر مربع', 'متر مربع'), ('متر مکعب', 'متر مکعب'), ('قطعه', 'قطعه'), ('شاخه', 'شاخه'), ('دستگاه', 'دستگاه'), ('سرویس', 'سرویس'), ('بسته', 'بسته'), ('کیسه', 'کیسه'), ('شات', 'شات'), ('ست', 'ست'), ('فنجان', 'فنجان'), ('جفت', 'جفت'), ('دست', 'دست')], default='عدد', max_length=50, verbose_name='unit_name')),
                ('direction', models.CharField(choices=[('ورود به انبار', 'ورود به انبار'), ('خروج از انبار', 'خروج از انبار')], max_length=50, verbose_name='direction')),
                ('status', models.CharField(choices=[('تعریف اولیه', 'تعریف اولیه'), ('در جریان', 'در جریان'), ('تمام شده', 'تمام شده')], default='تعریف اولیه', max_length=50, verbose_name='status')),
                ('description', tinymce.models.HTMLField(blank=True, max_length=50000, null=True, verbose_name='description')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.profile', verbose_name='creator')),
                ('invoice_line', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounting.invoiceline', verbose_name='invoice_line')),
                ('ware_house', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='warehouse.warehouse', verbose_name='ware_house')),
            ],
            options={
                'verbose_name': 'WareHouseSheet',
                'verbose_name_plural': 'WareHouseSheets',
            },
            bases=(models.Model, utility.utils.LinkHelper),
        ),
        migrations.CreateModel(
            name='WareHouseSheetSignature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='date_added')),
                ('description', models.CharField(max_length=200, verbose_name='description')),
                ('status', models.CharField(choices=[('DEFAULT', 'DEFAULT'), ('تحویل شده', 'تحویل شده'), ('در حال بررسی', 'درحال بررسی'), ('رد شده', 'ردشده'), ('پذیرفته شده', 'پذیرفته شده'), ('درحال خرید', 'درحال خرید'), ('درخواست شده', 'درخواست شده'), ('تسویه شده', 'تسویه شده')], default='درخواست شده', max_length=200, verbose_name='status')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='organization.employee', verbose_name='organization.employee')),
                ('request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='warehouse.warehousesheet', verbose_name='ware_house_sheet')),
            ],
            options={
                'verbose_name': 'WareHouseSheetSignature',
                'verbose_name_plural': 'WareHouseSheetSignature',
            },
            bases=(models.Model, utility.utils.LinkHelper),
        ),
    ]
