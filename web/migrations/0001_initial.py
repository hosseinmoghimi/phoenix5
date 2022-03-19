# Generated by Django 4.0.2 on 2022-03-19 00:50

from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.page')),
            ],
            options={
                'verbose_name': 'Blog',
                'verbose_name_plural': 'Blogs',
            },
            bases=('core.page',),
        ),
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.page')),
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
            ],
            options={
                'verbose_name': 'OurWork',
                'verbose_name_plural': 'OurWorks',
            },
            bases=('core.page',),
        ),
        migrations.CreateModel(
            name='Carousel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_name', models.CharField(max_length=50, verbose_name='app_name')),
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
