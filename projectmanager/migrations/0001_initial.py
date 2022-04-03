# Generated by Django 4.0.2 on 2022-04-03 21:59

from django.db import migrations, models
import django.db.models.deletion
import utility.utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
        ('accounting', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('account_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='accounting.account')),
                ('job_title', models.CharField(default='سرپرست', max_length=50, verbose_name='job title')),
            ],
            options={
                'verbose_name': 'Employee',
                'verbose_name_plural': 'Employees',
            },
            bases=('accounting.account',),
        ),
        migrations.CreateModel(
            name='Letter',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.page')),
            ],
            options={
                'verbose_name': 'Letter',
                'verbose_name_plural': 'Letters',
            },
            bases=('core.page',),
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('product_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='accounting.product')),
            ],
            options={
                'verbose_name': 'Material',
                'verbose_name_plural': 'Materials',
            },
            bases=('accounting.product',),
        ),
        migrations.CreateModel(
            name='OrganizationUnit',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.page')),
                ('pre_title', models.CharField(blank=True, max_length=50, null=True, verbose_name='pre_title')),
                ('account', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounting.account', verbose_name='account')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='childs', to='projectmanager.organizationunit', verbose_name='parent')),
            ],
            options={
                'verbose_name': 'OrganizationUnit',
                'verbose_name_plural': 'واحد های سازمانی',
            },
            bases=('core.page',),
        ),
        migrations.CreateModel(
            name='PM_Service',
            fields=[
                ('service_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='accounting.service')),
            ],
            options={
                'verbose_name': 'Service',
                'verbose_name_plural': 'Services',
            },
            bases=('accounting.service',),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.page')),
                ('status', models.CharField(choices=[('تعریف اولیه', 'تعریف اولیه'), ('پیش نویس', 'پیش نویس'), ('تحویل شده', 'تحویل شده'), ('در حال اجرا', 'درحال اجرا'), ('رد شده', 'ردشده'), ('پذیرفته شده', 'پذیرفته شده'), ('درخواست شده', 'درخواست شده'), ('کنسل شده', 'کنسل شده'), ('تسویه شده', 'تسویه شده')], default='پیش نویس', max_length=50, verbose_name='status')),
                ('percentage_completed', models.IntegerField(default=0, verbose_name='درصد تکمیل پروژه')),
                ('start_date', models.DateTimeField(blank=True, null=True, verbose_name='زمان شروع پروژه')),
                ('end_date', models.DateTimeField(blank=True, null=True, verbose_name='زمان پایان پروژه')),
                ('weight', models.IntegerField(default=10, verbose_name='ضریب و وزن پروژه')),
                ('contractor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='projects_contracted', to='projectmanager.organizationunit', verbose_name='پیمانکار')),
                ('employer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='projects_employed', to='projectmanager.organizationunit', verbose_name='کارفرما')),
                ('organization_units', models.ManyToManyField(blank=True, to='projectmanager.OrganizationUnit', verbose_name='واحد های سازمانی')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='projectmanager.project', verbose_name='parent')),
            ],
            options={
                'verbose_name': 'Project',
                'verbose_name_plural': 'Projects',
            },
            bases=('core.page',),
        ),
        migrations.CreateModel(
            name='ProjectInvoice',
            fields=[
                ('invoice_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='accounting.invoice')),
                ('project_id', models.IntegerField(verbose_name='project_id')),
            ],
            options={
                'verbose_name': 'ProjectInvoice',
                'verbose_name_plural': 'ProjectInvoices',
            },
            bases=('accounting.invoice',),
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('invoiceline_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='accounting.invoiceline')),
                ('date_delivered', models.DateTimeField(blank=True, null=True, verbose_name='date_delivered')),
                ('date_requested', models.DateTimeField(blank=True, null=True, verbose_name='date_requested')),
                ('status', models.CharField(choices=[('پیش نویس', 'پیش نویس'), ('DEFAULT', 'DEFAULT'), ('تعریف اولیه در سیستم', 'تعریف اولیه در سیستم'), ('تحویل شده', 'تحویل شده'), ('در حال انجام', 'در حال انجام'), ('رد شده', 'رد شده'), ('پذیرفته شده', 'پذیرفته شده'), ('درخواست شده', 'درخواست شده'), ('در حال خرید', 'در حال خرید'), ('متعلق به کارفرما', 'متعلق به کارفرما'), ('موجود در انبار', 'موجود در انبار'), ('خارج شده از انبار', 'خارج شده از انبار'), ('وارد شده به انبار', 'وارد شده به انبار')], max_length=50, verbose_name='status')),
                ('type', models.CharField(choices=[('درخواست متریال', 'درخواست متریال'), ('درخواست سرویس', 'درخواست سرویس')], default='درخواست متریال', max_length=50, verbose_name='type')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projectmanager.employee', verbose_name='employee')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projectmanager.project', verbose_name='project')),
            ],
            options={
                'verbose_name': 'Request',
                'verbose_name_plural': 'Requests',
            },
            bases=('accounting.invoiceline', utility.utils.LinkHelper),
        ),
        migrations.CreateModel(
            name='SampleForm',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.page')),
            ],
            options={
                'verbose_name': 'SampleForm',
                'verbose_name_plural': 'فرم های اداری نمونه',
            },
            bases=('core.page',),
        ),
        migrations.CreateModel(
            name='MaterialInvoice',
            fields=[
                ('projectinvoice_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='projectmanager.projectinvoice')),
            ],
            options={
                'verbose_name': 'MaterialInvoice',
                'verbose_name_plural': 'MaterialInvoices',
            },
            bases=('projectmanager.projectinvoice',),
        ),
        migrations.CreateModel(
            name='MaterialRequest',
            fields=[
                ('request_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='projectmanager.request')),
            ],
            options={
                'verbose_name': 'MaterialRequest',
                'verbose_name_plural': 'درخواست های متریال',
            },
            bases=('projectmanager.request', utility.utils.LinkHelper),
        ),
        migrations.CreateModel(
            name='ServiceInvoice',
            fields=[
                ('projectinvoice_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='projectmanager.projectinvoice')),
            ],
            options={
                'verbose_name': 'ServiceInvoice',
                'verbose_name_plural': 'ServiceInvoices',
            },
            bases=('projectmanager.projectinvoice',),
        ),
        migrations.CreateModel(
            name='ServiceRequest',
            fields=[
                ('request_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='projectmanager.request')),
            ],
            options={
                'verbose_name': 'ServiceRequest',
                'verbose_name_plural': 'درخواست های سرویس',
            },
            bases=('projectmanager.request', utility.utils.LinkHelper),
        ),
        migrations.CreateModel(
            name='WareHouse',
            fields=[
                ('organizationunit_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='projectmanager.organizationunit')),
            ],
            options={
                'verbose_name': 'WareHouse',
                'verbose_name_plural': 'WareHouses',
            },
            bases=('projectmanager.organizationunit',),
        ),
        migrations.CreateModel(
            name='RequestSignature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='date_added')),
                ('description', models.CharField(max_length=200, verbose_name='description')),
                ('status', models.CharField(choices=[('DEFAULT', 'DEFAULT'), ('تحویل شده', 'تحویل شده'), ('در حال بررسی', 'درحال بررسی'), ('رد شده', 'ردشده'), ('پذیرفته شده', 'پذیرفته شده'), ('درحال خرید', 'درحال خرید'), ('درخواست شده', 'درخواست شده'), ('تسویه شده', 'تسویه شده')], default='درخواست شده', max_length=200, verbose_name='status')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='projectmanager.employee', verbose_name='employee')),
                ('request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projectmanager.request', verbose_name='request')),
            ],
            options={
                'verbose_name': 'RequestSignature',
                'verbose_name_plural': 'RequestSignatures',
            },
            bases=(models.Model, utility.utils.LinkHelper),
        ),
        migrations.CreateModel(
            name='letterSent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_sent', models.DateTimeField(verbose_name='date sent')),
                ('letter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projectmanager.letter', verbose_name='letter')),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inbox_letters', to='projectmanager.organizationunit', verbose_name='گیرنده')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_letters', to='projectmanager.organizationunit', verbose_name='فرستنده')),
            ],
            options={
                'verbose_name': 'letterSent',
                'verbose_name_plural': 'letterSents',
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.page')),
                ('event_datetime', models.DateTimeField(verbose_name='event_datetime')),
                ('start_datetime', models.DateTimeField(verbose_name='start_datetime')),
                ('end_datetime', models.DateTimeField(verbose_name='end_datetime')),
                ('project_related', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projectmanager.project', verbose_name='project')),
            ],
            options={
                'verbose_name': 'Event',
                'verbose_name_plural': 'رویداد ها',
            },
            bases=('core.page',),
        ),
        migrations.AddField(
            model_name='employee',
            name='organization_unit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='projectmanager.organizationunit', verbose_name='organization_unit'),
        ),
    ]
