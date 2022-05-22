# Generated by Django 3.2.13 on 2022-05-22 14:05

from django.db import migrations, models
import django.db.models.deletion
import utility.utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authentication', '0001_initial'),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logo_origin', models.ImageField(blank=True, null=True, upload_to='authentication/images/account/', verbose_name='لوگو , تصویر')),
                ('title', models.CharField(blank=True, max_length=500, null=True, verbose_name='عنوان')),
                ('address', models.CharField(blank=True, max_length=50, null=True, verbose_name='آدرس')),
                ('tel', models.CharField(blank=True, max_length=50, null=True, verbose_name='تلفن')),
                ('description', models.CharField(blank=True, max_length=5000, verbose_name='توضیحات')),
                ('class_name', models.CharField(blank=True, max_length=50, verbose_name='class_name')),
                ('app_name', models.CharField(blank=True, max_length=50, verbose_name='app_name')),
                ('profile', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='authentication.profile', verbose_name='profile')),
            ],
            options={
                'verbose_name': 'Account',
                'verbose_name_plural': 'Accounts',
            },
            bases=(models.Model, utility.utils.LinkHelper),
        ),
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.page')),
            ],
            options={
                'verbose_name': 'Asset',
                'verbose_name_plural': 'Assets',
            },
            bases=('core.page', utility.utils.LinkHelper),
        ),
        migrations.CreateModel(
            name='Bank',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='بانک')),
                ('branch', models.CharField(blank=True, max_length=50, null=True, verbose_name='شعبه')),
                ('address', models.CharField(blank=True, max_length=50, null=True, verbose_name='آدرس')),
                ('tel', models.CharField(blank=True, max_length=50, null=True, verbose_name='تلفن')),
            ],
            options={
                'verbose_name': 'Bank',
                'verbose_name_plural': 'Banks',
            },
        ),
        migrations.CreateModel(
            name='FinancialDocumentTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='title')),
            ],
            options={
                'verbose_name': 'FinancialDocumentTag',
                'verbose_name_plural': 'FinancialDocumentTags',
            },
        ),
        migrations.CreateModel(
            name='FinancialYear',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='عنوان')),
                ('year', models.IntegerField(verbose_name='year')),
                ('start_date', models.DateTimeField(verbose_name='start_date')),
                ('end_date', models.DateTimeField(verbose_name='end_date')),
            ],
            options={
                'verbose_name': 'FinancialYear',
                'verbose_name_plural': 'FinancialYears',
            },
        ),
        migrations.CreateModel(
            name='ProductOrService',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.page')),
            ],
            options={
                'verbose_name': 'ProductOrService',
                'verbose_name_plural': 'ProductOrServices',
            },
            bases=('core.page',),
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.page')),
                ('status', models.CharField(choices=[('پیش نویس', 'پیش نویس'), ('در جریان', 'در جریان'), ('تحویل شده', 'تحویل شده'), ('تایید شده', 'تایید شده'), ('کنسل شده', 'کنسل شده'), ('پاس شده', 'پاس شده'), ('مانده حساب از قبل', 'مانده حساب از قبل')], default='پیش نویس', max_length=50, verbose_name='وضعیت')),
                ('amount', models.IntegerField(default=0, verbose_name='مبلغ')),
                ('payment_method', models.CharField(choices=[('پیش نویس', 'پیش نویس'), ('پرداخت نشده', 'پرداخت نشده'), ('همراه بانک', 'همراه بانک'), ('نقدی', 'نقدی'), ('چک', 'چک'), ('کارتخوان', 'کارتخوان'), ('کارت به کارت', 'کارت به کارت'), ('مانده حساب از قبل', 'مانده حساب از قبل')], default='پیش نویس', max_length=50, verbose_name='نوع پرداخت')),
                ('transaction_datetime', models.DateTimeField(verbose_name='تاریخ تراکنش')),
            ],
            options={
                'verbose_name': 'Transaction',
                'verbose_name_plural': 'Transactions',
            },
            bases=('core.page', utility.utils.LinkHelper),
        ),
        migrations.CreateModel(
            name='TransactionCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='title')),
                ('color_origin', models.CharField(blank=True, choices=[('success', 'success'), ('danger', 'danger'), ('warning', 'warning'), ('primary', 'primary'), ('muted', 'muted'), ('secondary', 'secondary'), ('info', 'info'), ('light', 'light'), ('rose', 'rose'), ('dark', 'dark')], max_length=50, null=True, verbose_name='color')),
            ],
            options={
                'verbose_name': 'TransactionCategory',
                'verbose_name_plural': 'TransactionCategories',
            },
        ),
        migrations.CreateModel(
            name='Cheque',
            fields=[
                ('transaction_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='accounting.transaction')),
                ('cheque_date', models.DateField(verbose_name='تاریخ چک')),
            ],
            options={
                'verbose_name': 'چک',
                'verbose_name_plural': 'چک ها',
            },
            bases=('accounting.transaction', utility.utils.LinkHelper),
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('transaction_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='accounting.transaction')),
                ('tax_percent', models.IntegerField(default=0, verbose_name='درصد مالیات')),
                ('invoice_datetime', models.DateTimeField(verbose_name='تاریخ فاکتور')),
                ('ship_fee', models.IntegerField(default=0, verbose_name='هزینه حمل')),
                ('discount', models.IntegerField(default=0, verbose_name='تخفیف')),
            ],
            options={
                'verbose_name': 'Invoice',
                'verbose_name_plural': 'Invoices',
            },
            bases=('accounting.transaction',),
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('transaction_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='accounting.transaction')),
            ],
            options={
                'verbose_name': 'Payment',
                'verbose_name_plural': 'پرداخت ها',
            },
            bases=('accounting.transaction',),
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('productorservice_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='accounting.productorservice')),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
            },
            bases=('accounting.productorservice',),
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('productorservice_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='accounting.productorservice')),
            ],
            options={
                'verbose_name': 'Service',
                'verbose_name_plural': 'Services',
            },
            bases=('accounting.productorservice',),
        ),
        migrations.CreateModel(
            name='Spend',
            fields=[
                ('transaction_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='accounting.transaction')),
                ('spend_type', models.CharField(choices=[('هزینه', 'هزینه'), ('حقوق', 'حقوق')], max_length=50, verbose_name='spend_type')),
            ],
            options={
                'verbose_name': 'Spend',
                'verbose_name_plural': 'Spends',
            },
            bases=('accounting.transaction', utility.utils.LinkHelper),
        ),
        migrations.AddField(
            model_name='transaction',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounting.transactioncategory', verbose_name='دسته بندی'),
        ),
        migrations.AddField(
            model_name='transaction',
            name='creator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='authentication.profile', verbose_name='ثبت شده توسط'),
        ),
        migrations.AddField(
            model_name='transaction',
            name='pay_from',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions_from', to='accounting.account', verbose_name='پرداخت کننده'),
        ),
        migrations.AddField(
            model_name='transaction',
            name='pay_to',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions_to', to='accounting.account', verbose_name='دریافت کننده'),
        ),
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit_name', models.CharField(choices=[('عدد', 'عدد'), ('گرم', 'گرم'), ('کیلوگرم', 'کیلوگرم'), ('تن', 'تن'), ('متر', 'متر'), ('متر مربع', 'متر مربع'), ('متر مکعب', 'متر مکعب'), ('قطعه', 'قطعه'), ('رول', 'رول'), ('شاخه', 'شاخه'), ('دستگاه', 'دستگاه'), ('سرویس', 'سرویس'), ('بسته', 'بسته'), ('کیسه', 'کیسه'), ('شات', 'شات'), ('ست', 'ست'), ('فنجان', 'فنجان'), ('جفت', 'جفت'), ('دست', 'دست')], default='عدد', max_length=50, verbose_name='unit_name')),
                ('sell_price', models.IntegerField(default=0, verbose_name='فروش')),
                ('buy_price', models.IntegerField(default=0, verbose_name='خرید')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='date_added')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounting.account', verbose_name='account')),
                ('product_or_service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounting.productorservice', verbose_name='product_or_service')),
            ],
            options={
                'verbose_name': 'Price',
                'verbose_name_plural': 'Prices',
            },
            bases=(models.Model, utility.utils.LinkHelper),
        ),
        migrations.CreateModel(
            name='FinancialDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bedehkar', models.IntegerField(default=0, verbose_name='bedehkar')),
                ('bestankar', models.IntegerField(default=0, verbose_name='bestankar')),
                ('color', models.CharField(choices=[('success', 'success'), ('danger', 'danger'), ('warning', 'warning'), ('primary', 'primary'), ('muted', 'muted'), ('secondary', 'secondary'), ('info', 'info'), ('light', 'light'), ('rose', 'rose'), ('dark', 'dark')], default='primary', max_length=50, verbose_name='color')),
                ('direction', models.CharField(choices=[('بدهکار', 'بدهکار'), ('بستانکار', 'بستانکار')], default='بستانکار', max_length=50, verbose_name='direction')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounting.account', verbose_name='account')),
                ('tags', models.ManyToManyField(blank=True, to='accounting.FinancialDocumentTag', verbose_name='tags')),
                ('transaction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounting.transaction', verbose_name='transaction')),
            ],
            options={
                'verbose_name': 'FinancialDocument',
                'verbose_name_plural': 'FinancialDocuments',
            },
            bases=(models.Model, utility.utils.LinkHelper),
        ),
        migrations.CreateModel(
            name='FinancialBalance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(choices=[('حساب عادی', 'حساب عادی'), ('سرمایه گذاری', 'سرمایه گذاری'), ('دارایی', 'دارایی'), ('ملک', 'ملک'), ('اثاثیه', 'اثاثیه'), ('مالیات', 'مالیات'), ('هزینه', 'هزینه'), ('حقوق', 'حقوق'), ('فروش', 'فروش'), ('خرید', 'خرید'), ('سایر', 'سایر')], default='سایر', max_length=50, verbose_name='title')),
                ('bestankar', models.IntegerField(default=0, verbose_name='بستانکار')),
                ('bedehkar', models.IntegerField(default=0, verbose_name='بدهکار')),
                ('color_origin', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.color', verbose_name='color')),
                ('financial_document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounting.financialdocument', verbose_name='FinancialDocument')),
            ],
            options={
                'verbose_name': 'FinancialBalance',
                'verbose_name_plural': 'FinancialBalances',
            },
            bases=(models.Model, utility.utils.LinkHelper),
        ),
        migrations.CreateModel(
            name='Cost',
            fields=[
                ('spend_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='accounting.spend')),
                ('cost_type', models.CharField(choices=[('هزینه آب', 'هزینه آب'), ('هزینه خوراک', 'هزینه خوراک'), ('هزینه تلفن', 'هزینه تلفن'), ('هزینه برق', 'هزینه برق'), ('هزینه اینترنت', 'هزینه اینترنت'), ('هزینه گاز', 'هزینه گاز'), ('هزینه حمل ونقل', 'هزینه حمل ونقل'), ('هزینه اجاره', 'هزینه اجاره')], max_length=50, verbose_name='cost')),
            ],
            options={
                'verbose_name': 'Cost',
                'verbose_name_plural': 'Costs',
            },
            bases=('accounting.spend', utility.utils.LinkHelper),
        ),
        migrations.CreateModel(
            name='Salary',
            fields=[
                ('spend_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='accounting.spend')),
                ('month', models.IntegerField(verbose_name='month')),
                ('year', models.IntegerField(verbose_name='year')),
            ],
            options={
                'verbose_name': 'Salary',
                'verbose_name_plural': 'Salaries',
            },
            bases=('accounting.spend', utility.utils.LinkHelper),
        ),
        migrations.CreateModel(
            name='InvoiceLine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='date_added')),
                ('row', models.IntegerField(blank=True, verbose_name='row')),
                ('quantity', models.FloatField(verbose_name='quantity')),
                ('unit_price', models.IntegerField(verbose_name='unit_price')),
                ('unit_name', models.CharField(choices=[('عدد', 'عدد'), ('گرم', 'گرم'), ('کیلوگرم', 'کیلوگرم'), ('تن', 'تن'), ('متر', 'متر'), ('متر مربع', 'متر مربع'), ('متر مکعب', 'متر مکعب'), ('قطعه', 'قطعه'), ('رول', 'رول'), ('شاخه', 'شاخه'), ('دستگاه', 'دستگاه'), ('سرویس', 'سرویس'), ('بسته', 'بسته'), ('کیسه', 'کیسه'), ('شات', 'شات'), ('ست', 'ست'), ('فنجان', 'فنجان'), ('جفت', 'جفت'), ('دست', 'دست')], default='عدد', max_length=50, verbose_name='unit_name')),
                ('description', models.CharField(blank=True, max_length=50, null=True, verbose_name='description')),
                ('product_or_service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounting.productorservice', verbose_name='productorservice')),
                ('invoice', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='lines', to='accounting.invoice', verbose_name='invoice')),
            ],
            options={
                'verbose_name': 'InvoiceLine',
                'verbose_name_plural': 'InvoiceLines',
            },
            bases=(models.Model, utility.utils.LinkHelper),
        ),
        migrations.CreateModel(
            name='BankAccount',
            fields=[
                ('account_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='accounting.account')),
                ('account_no', models.CharField(blank=True, max_length=50, null=True, verbose_name='shomareh')),
                ('card_no', models.CharField(blank=True, max_length=50, null=True, verbose_name='card')),
                ('shaba_no', models.CharField(blank=True, max_length=50, null=True, verbose_name='shaba')),
                ('bank', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounting.bank', verbose_name='bank')),
            ],
            options={
                'verbose_name': 'BankAccount',
                'verbose_name_plural': 'BankAccounts',
            },
            bases=('accounting.account',),
        ),
    ]
