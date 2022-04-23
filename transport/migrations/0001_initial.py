# Generated by Django 3.2.13 on 2022-04-22 23:51

from django.db import migrations, models
import django.db.models.deletion
import utility.utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('map', '0001_initial'),
        ('accounting', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100, null=True, verbose_name='title')),
                ('color', models.CharField(choices=[('success', 'success'), ('danger', 'danger'), ('warning', 'warning'), ('primary', 'primary'), ('muted', 'muted'), ('secondary', 'secondary'), ('info', 'info'), ('light', 'light'), ('rose', 'rose'), ('dark', 'dark')], default='primary', max_length=50, verbose_name='color')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounting.account', verbose_name='account')),
            ],
            options={
                'verbose_name': 'Driver',
                'verbose_name_plural': 'Drivers',
            },
            bases=(models.Model, utility.utils.LinkHelper),
        ),
        migrations.CreateModel(
            name='Passenger',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100, null=True, verbose_name='title')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounting.account', verbose_name='account')),
            ],
            options={
                'verbose_name': 'Passenger',
                'verbose_name_plural': 'Passengers',
            },
            bases=(models.Model, utility.utils.LinkHelper),
        ),
        migrations.CreateModel(
            name='TripCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='عنوان')),
                ('color', models.CharField(choices=[('success', 'success'), ('danger', 'danger'), ('warning', 'warning'), ('primary', 'primary'), ('muted', 'muted'), ('secondary', 'secondary'), ('info', 'info'), ('light', 'light'), ('rose', 'rose'), ('dark', 'dark')], default='primary', max_length=50, verbose_name='رنگ')),
            ],
            options={
                'verbose_name': 'TripCategory',
                'verbose_name_plural': 'TripCategorys',
            },
            bases=(models.Model, utility.utils.LinkHelper),
        ),
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('asset_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='accounting.asset')),
                ('vehicle_type', models.CharField(choices=[('وانت', 'وانت'), ('سواری', 'سواری'), ('اتوبوس', 'اتوبوس'), ('تاکسی', 'تاکسی'), ('گریدر', 'گریدر'), ('لودر', 'لودر'), ('تریلی', 'تریلی'), ('کانتینر', 'کانتینر'), ('سپراتور', 'سپراتور'), ('خاور', 'خاور')], default='سواری', max_length=50, verbose_name='نوع وسیله ')),
                ('brand', models.CharField(choices=[('تویوتا', 'تویوتا'), ('پژو', 'پژو'), ('بنز', 'بنز'), ('ایسوزو', 'ایسوزو'), ('اسکانیا', 'اسکانیا'), ('مزدا', 'مزدا'), ('ولوو', 'ولوو'), ('کاترپیلار', 'کاترپیلار'), ('هیوندای', 'هیوندای'), ('هووو', 'هووو'), ('دانگ فنگ', 'دانگ فنگ'), ('سایپا', 'سایپا'), ('ایران خودرو', 'ایران خودرو'), ('XCMG', 'XCMG')], default='تویوتا', max_length=50, verbose_name='برند')),
                ('model_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='مدل')),
                ('plaque', models.CharField(blank=True, max_length=50, null=True, verbose_name='پلاک')),
                ('driver', models.CharField(blank=True, max_length=50, null=True, verbose_name='راننده')),
                ('color', models.CharField(choices=[('سفید', 'سفید'), ('سیاه', 'سیاه'), ('نوک مدادی', 'نوک مدادی'), ('دلفینی', 'دلفینی'), ('بژ', 'بژ'), ('قرمز', 'قرمز')], default='سفید', max_length=50, verbose_name='رنگ')),
                ('kilometer', models.IntegerField(default=0, verbose_name='کیلومتر')),
            ],
            options={
                'verbose_name': 'Vehicle',
                'verbose_name_plural': 'Vehicles',
            },
            bases=('accounting.asset',),
        ),
        migrations.CreateModel(
            name='VehicleEvent',
            fields=[
                ('transaction_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='accounting.transaction')),
                ('kilometer', models.IntegerField(blank=True, null=True, verbose_name='کارکرد')),
                ('vehicle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transport.vehicle', verbose_name='ماشین')),
            ],
            options={
                'verbose_name': 'VehicleEvent',
                'verbose_name_plural': 'VehicleEvents',
            },
            bases=('accounting.transaction',),
        ),
        migrations.CreateModel(
            name='Maintenance',
            fields=[
                ('vehicleevent_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='transport.vehicleevent')),
                ('maintenance_type', models.CharField(choices=[('شستشو', 'شستشو'), ('آب رادیات جدید', 'آب رادیات جدید'), ('سوخت جدید', 'سوخت جدید'), ('تعمیر موتور', 'تعمیر موتور'), ('تعمیر گیربکس', 'تعمیر گیربکس'), ('بیمه جدید', 'بیمه جدید'), ('لاستیک جدید', 'لاستیک جدید'), ('زنجیر جدید', 'زنجیر جدید'), ('شیشه جدید', 'شیشه جدید'), ('تعویض روغن', 'تعویض روغن'), ('فیلتر هوای جدید', 'فیلتر هوای جدید'), ('فیلتر روغن جدید', 'فیلتر روغن جدید')], max_length=100, verbose_name='سرویس')),
            ],
            options={
                'verbose_name': 'Maintenance',
                'verbose_name_plural': 'Maintenances',
            },
            bases=('transport.vehicleevent',),
        ),
        migrations.CreateModel(
            name='WorkShift',
            fields=[
                ('transaction_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='accounting.transaction')),
                ('start_time', models.DateTimeField(verbose_name='start_time')),
                ('end_time', models.DateTimeField(verbose_name='end_date')),
                ('wage', models.IntegerField(default=0, verbose_name='اجرت راننده')),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='map.area', verbose_name='area')),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transport.driver', verbose_name='driver')),
                ('vehicle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transport.vehicle', verbose_name='vehicle')),
            ],
            options={
                'verbose_name': 'WorkShift',
                'verbose_name_plural': 'WorkShifts',
            },
            bases=('accounting.transaction',),
        ),
        migrations.CreateModel(
            name='TripPath',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cost', models.IntegerField(default=0, verbose_name='هزینه')),
                ('distance', models.IntegerField(default=0, verbose_name='فاصله')),
                ('duration', models.IntegerField(default=0, verbose_name='مدت زمان تقریبی')),
                ('area', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='map.area', verbose_name='area')),
                ('destination', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trip_destination_set', to='map.location', verbose_name='مقصد')),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trip_source_set', to='map.location', verbose_name='مبدا')),
            ],
            options={
                'verbose_name': 'TripPath',
                'verbose_name_plural': 'TripPaths',
            },
            bases=(models.Model, utility.utils.LinkHelper),
        ),
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('transaction_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='accounting.transaction')),
                ('distance', models.IntegerField(verbose_name='distance')),
                ('duration', models.IntegerField(verbose_name='duration')),
                ('date_started', models.DateTimeField(blank=True, null=True, verbose_name='شروع سرویس')),
                ('date_ended', models.DateTimeField(blank=True, null=True, verbose_name='پایان سرویس')),
                ('delay', models.IntegerField(default=0, verbose_name='تاخیر')),
                ('passengers', models.ManyToManyField(blank=True, to='transport.Passenger', verbose_name='مسافر ها')),
                ('trip_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='transport.tripcategory', verbose_name='نوع سفر')),
                ('trip_paths', models.ManyToManyField(blank=True, to='transport.TripPath', verbose_name='مسیر های سرویس')),
                ('vehicle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transport.vehicle', verbose_name='vehicle')),
            ],
            options={
                'verbose_name': 'Trip',
                'verbose_name_plural': 'Trips',
            },
            bases=('accounting.transaction',),
        ),
        migrations.CreateModel(
            name='ServiceMan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100, null=True, verbose_name='title')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounting.account', verbose_name='account')),
            ],
            options={
                'verbose_name': 'ServiceMan',
                'verbose_name_plural': 'ServiceMans',
            },
            bases=(models.Model, utility.utils.LinkHelper),
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100, null=True, verbose_name='title')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounting.account', verbose_name='account')),
            ],
            options={
                'verbose_name': 'Client',
                'verbose_name_plural': 'Client',
            },
            bases=(models.Model, utility.utils.LinkHelper),
        ),
        migrations.CreateModel(
            name='VehicleWorkEvent',
            fields=[
                ('vehicleevent_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='transport.vehicleevent')),
                ('event_type', models.CharField(choices=[('لاستیک پنچر', 'لاستیک پنچر'), ('شیشه شکسته', 'شیشه شکسته'), ('خسارت مالی', 'خسارت مالی'), ('خسارت جانی', 'خسارت جانی')], max_length=50, verbose_name='event_type')),
                ('work_shift', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transport.workshift', verbose_name='شیفت کاری')),
            ],
            options={
                'verbose_name': 'VehicleWorkEvent',
                'verbose_name_plural': 'VehicleWorkEvents',
            },
            bases=('transport.vehicleevent',),
        ),
    ]
