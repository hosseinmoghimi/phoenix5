# Generated by Django 4.1.3 on 2022-12-23 02:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0025_financialdocument_status'),
        ('loyaltyclub', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coupon',
            name='amount',
        ),
        migrations.RemoveField(
            model_name='coupon',
            name='id',
        ),
        migrations.RemoveField(
            model_name='coupon',
            name='title',
        ),
        migrations.AddField(
            model_name='coupon',
            name='transaction_ptr',
            field=models.OneToOneField(auto_created=True, default=1, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='accounting.transaction'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='coef',
            name='percentage',
            field=models.IntegerField(default=3, verbose_name='percentage'),
        ),
    ]
