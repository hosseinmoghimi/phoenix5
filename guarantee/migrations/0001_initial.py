# Generated by Django 4.0.2 on 2022-04-03 21:59

from django.db import migrations, models
import django.db.models.deletion
import tinymce.models
import utility.utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounting', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Guarantee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(verbose_name='شروع گارانتی')),
                ('end_date', models.DateField(verbose_name='پابان گارانتی')),
                ('status', models.CharField(choices=[('معتبر', 'معتبر'), ('نامعتبر', 'نامعتبر'), ('پایان یافته', 'پایان یافته'), ('در جریان', 'در جریان'), ('تعویض شده', 'تعویض شده'), ('تعمیر شده', 'تعمیر شده'), ('برگشت داده شده', 'برگشت داده شده')], default='معتبر', max_length=50, verbose_name='وضعیت')),
                ('type', models.CharField(choices=[('تعمیر', 'تعمیر'), ('تعویض', 'تعویض')], default='تعمیر', max_length=50, verbose_name='نوع گارانتی')),
                ('serial_no', models.CharField(max_length=50, verbose_name='شماره سریال')),
                ('conditions', models.CharField(blank=True, max_length=5000, null=True, verbose_name='شرایط')),
                ('description', tinymce.models.HTMLField(blank=True, max_length=50000, null=True, verbose_name='توضیحات')),
                ('invoice_line', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounting.invoiceline', verbose_name='ردیف فاکتور')),
            ],
            options={
                'verbose_name': 'Guarantee',
                'verbose_name_plural': 'Guarantees',
            },
            bases=(models.Model, utility.utils.LinkHelper),
        ),
    ]
