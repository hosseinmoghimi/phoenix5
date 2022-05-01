# Generated by Django 3.2.13 on 2022-05-01 05:03

from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authentication', '0001_initial'),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.page')),
                ('for_home', models.BooleanField(default=False, verbose_name='for_home')),
            ],
            options={
                'verbose_name': 'Blog',
                'verbose_name_plural': 'Blogs',
            },
            bases=('core.page',),
        ),
        migrations.CreateModel(
            name='CountDownItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=500, null=True, verbose_name='Title')),
                ('pretitle', models.CharField(blank=True, max_length=500, null=True, verbose_name='Pre Title')),
                ('for_home', models.BooleanField(default=False, verbose_name='نمایش در صفحه اصلی')),
                ('image_origin', models.ImageField(blank=True, null=True, upload_to='web/images/CountDownItem/', verbose_name='تصویر')),
                ('counter', models.IntegerField(default=100, verbose_name='شمارنده')),
                ('priority', models.IntegerField(default=100, verbose_name='ترتیب')),
            ],
            options={
                'verbose_name': 'CountDownItem',
                'verbose_name_plural': 'شمارنده ها',
            },
        ),
        migrations.CreateModel(
            name='FAQ',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('for_home', models.BooleanField(default=False, verbose_name='نمایش در صفحه خانه')),
                ('color', models.CharField(choices=[('success', 'success'), ('danger', 'danger'), ('warning', 'warning'), ('primary', 'primary'), ('muted', 'muted'), ('secondary', 'secondary'), ('info', 'info'), ('light', 'light'), ('rose', 'rose'), ('dark', 'dark')], default='primary', max_length=50, verbose_name='رنگ')),
                ('priority', models.IntegerField(verbose_name='ترتیب')),
                ('question', models.CharField(max_length=200, verbose_name='سوال')),
                ('answer', models.CharField(max_length=5000, verbose_name='پاسخ')),
            ],
            options={
                'verbose_name': 'FAQ',
                'verbose_name_plural': 'پرسش های متداول',
            },
        ),
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.page')),
                ('for_home', models.BooleanField(default=False, verbose_name='for_home')),
            ],
            options={
                'verbose_name': 'Feature',
                'verbose_name_plural': 'Features',
            },
            bases=('core.page',),
        ),
        migrations.CreateModel(
            name='OurWork',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.page')),
                ('for_home', models.BooleanField(default=False, verbose_name='for_home')),
            ],
            options={
                'verbose_name': 'OurWork',
                'verbose_name_plural': 'OurWorks',
            },
            bases=('core.page',),
        ),
        migrations.CreateModel(
            name='Technology',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.page')),
            ],
            options={
                'verbose_name': 'Technology',
                'verbose_name_plural': 'تکنولوژی',
            },
            bases=('core.page',),
        ),
        migrations.CreateModel(
            name='Testimonial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('for_home', models.BooleanField(default=False, verbose_name='نمایش در صفحه خانه')),
                ('title', models.CharField(blank=True, max_length=2000, null=True, verbose_name='عنوان')),
                ('body', tinymce.models.HTMLField(blank=True, max_length=20000, null=True, verbose_name='متن')),
                ('footer', models.CharField(max_length=200, verbose_name='پانوشت')),
                ('priority', models.IntegerField(default=100, verbose_name='ترتیب')),
                ('profile', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='authentication.profile', verbose_name='profile')),
            ],
            options={
                'verbose_name': 'Testimonial',
                'verbose_name_plural': 'گفته های مشتریان',
            },
        ),
        migrations.CreateModel(
            name='OurTeam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='app_name')),
                ('job', models.CharField(max_length=100, verbose_name='سمت')),
                ('description', tinymce.models.HTMLField(blank=True, max_length=50000, null=True, verbose_name='توضیحات')),
                ('priority', models.IntegerField(default=1000, verbose_name='ترتیب')),
                ('for_home', models.BooleanField(default=False, verbose_name='for_home')),
                ('links', models.ManyToManyField(blank=True, to='core.Link', verbose_name='links')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.profile', verbose_name='پروفایل')),
            ],
            options={
                'verbose_name': 'OurTeam',
                'verbose_name_plural': 'تیم ما',
                'db_table': 'OurTeam',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Carousel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_banner', models.ImageField(upload_to='web/images/Banner/', verbose_name='تصویر اسلایدر  1333*2000 ')),
                ('title', models.CharField(blank=True, max_length=500, null=True, verbose_name='عنوان')),
                ('body', tinymce.models.HTMLField(blank=True, max_length=2000, null=True, verbose_name='بدنه')),
                ('text_color', models.CharField(default='#fff', max_length=20, verbose_name='رنگ متن')),
                ('height', models.IntegerField(default=350, verbose_name='height')),
                ('priority', models.IntegerField(default=100, verbose_name='ترتیب')),
                ('archive', models.BooleanField(default=False, verbose_name='بایگانی شود؟')),
                ('tag_number', models.IntegerField(default=100, verbose_name='عدد برچسب')),
                ('tag_text', models.CharField(blank=True, max_length=100, null=True, verbose_name='متن برچسب')),
                ('links', models.ManyToManyField(blank=True, to='core.Link', verbose_name='links')),
            ],
            options={
                'verbose_name': 'Carousel',
                'verbose_name_plural': 'اسلایدر های صفحه اصلی',
            },
        ),
    ]
