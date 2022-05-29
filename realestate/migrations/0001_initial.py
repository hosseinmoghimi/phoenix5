# Generated by Django 3.2.13 on 2022-05-29 13:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounting', '0003_asset_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='Property',
            fields=[
                ('asset_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='accounting.asset')),
                ('floor', models.CharField(choices=[('زیر زمین', 'زیر زمین'), ('همکف', 'همکف'), ('اول', 'اول'), ('دوم', 'دوم'), ('سوم', 'سوم'), ('چهارم', 'چهارم')], default='همکف', max_length=50, verbose_name='طبقه')),
                ('garage', models.IntegerField(default=0, verbose_name='تعداد گاراژ')),
                ('elevator', models.BooleanField(default=False, verbose_name='آسانسور دارد؟')),
                ('bed_rooms', models.IntegerField(default=1, verbose_name='تعداد خواب')),
                ('bath_rooms', models.IntegerField(default=1, verbose_name='تعداد سرویس بهداشتی')),
                ('kitchen_type', models.CharField(choices=[('معمولی', 'معمولی'), ('جزیره', 'جزیره')], default='معمولی', max_length=50, verbose_name='نوع آشپزخانه')),
                ('area', models.IntegerField(verbose_name='مساحت')),
                ('address', models.CharField(blank=True, max_length=500, null=True, verbose_name='آدرس')),
                ('agent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounting.account', verbose_name='مسئول فروش')),
            ],
            options={
                'verbose_name': 'Property',
                'verbose_name_plural': 'Propertys',
            },
            bases=('accounting.asset',),
        ),
    ]
