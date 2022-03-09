# Generated by Django 4.0.2 on 2022-03-09 09:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0007_financialbalance_misc_financialsubaccount_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='title')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounting.subaccount', verbose_name='Parent')),
            ],
            options={
                'verbose_name': 'SubAccount',
                'verbose_name_plural': 'SubAccounts',
            },
        ),
        migrations.RemoveField(
            model_name='financialbalance',
            name='sub_account',
        ),
        migrations.DeleteModel(
            name='FinancialSubAccount',
        ),
        migrations.AddField(
            model_name='financialdocument',
            name='sub_account',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounting.subaccount', verbose_name='Sub Account'),
        ),
    ]
