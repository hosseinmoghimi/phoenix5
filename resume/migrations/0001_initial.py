# Generated by Django 3.2.13 on 2022-04-30 00:10

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
            name='ResumeIndex',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.CharField(choices=[('english', 'english'), ('dutch', 'dutch'), ('farsi', 'farsi'), ('russian', 'russian'), ('arabic', 'arabic')], default='english', max_length=50, verbose_name='language')),
                ('image_header_origin', models.ImageField(blank=True, null=True, upload_to='resume/img/Resume/Header/', verbose_name='تصویر سربرگ')),
                ('title', models.CharField(blank=True, max_length=100, null=True, verbose_name='title')),
                ('typing_text', models.CharField(blank=True, default='Developer,Designer,Programmer', max_length=500, null=True, verbose_name='typing_text')),
                ('about_top', tinymce.models.HTMLField(blank=True, null=True, verbose_name='about_top')),
                ('image_main_origin', models.ImageField(blank=True, null=True, upload_to='resume/img/Resume/Main/', verbose_name='تصویر اصلی')),
                ('job_title', models.CharField(blank=True, max_length=300, null=True, verbose_name='job_title')),
                ('about_middle', tinymce.models.HTMLField(blank=True, null=True, verbose_name='about_middle')),
                ('birth_day', models.DateField(blank=True, null=True, verbose_name='birth_day')),
                ('website', models.CharField(blank=True, max_length=500, null=True, verbose_name='website')),
                ('city', models.CharField(blank=True, max_length=50, null=True, verbose_name='city')),
                ('age', models.IntegerField(blank=True, null=True, verbose_name='age')),
                ('degree', models.CharField(blank=True, max_length=100, null=True, verbose_name='degree')),
                ('email', models.CharField(blank=True, max_length=100, null=True, verbose_name='email')),
                ('freelance', models.CharField(blank=True, max_length=100, null=True, verbose_name='freelance')),
                ('about_bottom', tinymce.models.HTMLField(blank=True, null=True, verbose_name='about_bottom')),
                ('facts_top', tinymce.models.HTMLField(blank=True, null=True, verbose_name='facts_top')),
                ('skills_top', tinymce.models.HTMLField(blank=True, null=True, verbose_name='skills_top')),
                ('resume_top', tinymce.models.HTMLField(blank=True, null=True, verbose_name='resume_top')),
                ('portfolio_top', tinymce.models.HTMLField(blank=True, null=True, verbose_name='portfolio_top')),
                ('services_top', tinymce.models.HTMLField(blank=True, null=True, verbose_name='services_top')),
                ('location', models.CharField(blank=True, max_length=200, null=True, verbose_name='location')),
                ('call', models.CharField(blank=True, max_length=50, null=True, verbose_name='call')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.profile', verbose_name='profile')),
            ],
            options={
                'verbose_name': 'ResumeIndex',
                'verbose_name_plural': 'ResumeIndexs',
            },
        ),
        migrations.CreateModel(
            name='ResumePage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.page')),
            ],
            bases=('core.page',),
        ),
        migrations.CreateModel(
            name='ResumeTestimonial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('teller', models.CharField(max_length=2000, verbose_name='teller')),
                ('teller_description', models.CharField(max_length=2000, verbose_name='teller_description')),
                ('title', models.CharField(max_length=2000, verbose_name='عنوان')),
                ('body', models.CharField(blank=True, max_length=2000, null=True, verbose_name='متن')),
                ('footer', models.CharField(max_length=200, verbose_name='پانوشت')),
                ('priority', models.IntegerField(default=100, verbose_name='ترتیب')),
                ('date_added', models.DateField(verbose_name='date_added')),
                ('image_origin', models.ImageField(blank=True, null=True, upload_to='resume/img/Testimonial/', verbose_name='تصویر')),
                ('resume_index', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resume.resumeindex', verbose_name='resume')),
            ],
            options={
                'verbose_name': 'Testimonial',
                'verbose_name_plural': 'Testimonial',
            },
        ),
        migrations.CreateModel(
            name='ResumeSocialLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(choices=[('twitter', 'Twitter'), ('facebook', 'Facebook'), ('instagram', 'Instagram'), ('skype', 'Google Plus'), ('linkedin', 'Linkedin')], max_length=50, verbose_name='title')),
                ('href', models.CharField(max_length=5000, verbose_name='href')),
                ('link_class', models.CharField(choices=[('twitter', 'Twitter'), ('facebook', 'Facebook'), ('instagram', 'Instagram'), ('skype', 'Google Plus'), ('linkedin', 'Linkedin')], max_length=50, verbose_name='link_class')),
                ('icon', models.CharField(choices=[('<i class="bx bxl-twitter"></i>', 'Twitter'), ('<i class="bx bxl-facebook"></i>', 'Facebook'), ('<i class="bx bxl-instagram"></i>', 'Instagram'), ('<i class="bx bxl-skype"></i>', 'Google Plus'), ('<i class="bx bxl-linkedin"></i>', 'Linkedin'), ('<i class="bi bi-journal-richtext"></i>', 'Journal'), ('<i class="bi bi-emoji-smile"></i>', 'Emoji'), ('<i class="bi bi-headset"></i>', 'Headset'), ('<i class="bi bi-award"></i>', 'Award')], max_length=50, verbose_name='icon')),
                ('resume_index', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resume.resumeindex', verbose_name='resumeindex')),
            ],
            options={
                'verbose_name': 'ResumeSocialLink',
                'verbose_name_plural': 'ResumeSocialLinks',
            },
        ),
        migrations.CreateModel(
            name='ResumeSkill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='title')),
                ('percentage', models.IntegerField(default=10, verbose_name='percentage')),
                ('priority', models.IntegerField(default=10, verbose_name='priority')),
                ('resume_index', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resume.resumeindex', verbose_name='resume')),
            ],
            options={
                'verbose_name': 'ResumeSkill',
                'verbose_name_plural': 'ResumeSkills',
            },
        ),
        migrations.CreateModel(
            name='ResumeFact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500, verbose_name='title')),
                ('color', models.CharField(blank=True, max_length=50, null=True, verbose_name='color')),
                ('priority', models.IntegerField(default=10, verbose_name='priority')),
                ('icon', models.CharField(blank=True, choices=[('<i class="bx bxl-twitter"></i>', 'Twitter'), ('<i class="bx bxl-facebook"></i>', 'Facebook'), ('<i class="bx bxl-instagram"></i>', 'Instagram'), ('<i class="bx bxl-skype"></i>', 'Google Plus'), ('<i class="bx bxl-linkedin"></i>', 'Linkedin'), ('<i class="bi bi-journal-richtext"></i>', 'Journal'), ('<i class="bi bi-emoji-smile"></i>', 'Emoji'), ('<i class="bi bi-headset"></i>', 'Headset'), ('<i class="bi bi-award"></i>', 'Award')], max_length=100, null=True, verbose_name='icon')),
                ('count', models.IntegerField(default=10, verbose_name='count')),
                ('resume_index', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resume.resumeindex', verbose_name='resume')),
            ],
            options={
                'verbose_name': 'ResumeFact',
                'verbose_name_plural': 'ResumeFacts',
            },
        ),
        migrations.CreateModel(
            name='ResumeCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='title')),
                ('resume_index', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resume.resumeindex', verbose_name='resume')),
            ],
            options={
                'verbose_name': 'ResumeCategory',
                'verbose_name_plural': 'ResumeCategorys',
            },
        ),
        migrations.CreateModel(
            name='ContactMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=50, verbose_name='نام کامل')),
                ('mobile', models.CharField(max_length=50, verbose_name='شماره تماس')),
                ('email', models.EmailField(max_length=254, verbose_name='ایمیل')),
                ('subject', models.CharField(max_length=50, verbose_name='عنوان پیام')),
                ('message', models.CharField(max_length=50, verbose_name='متن پیام')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='افزوده شده در')),
                ('resume_index', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resume.resumeindex', verbose_name='resume')),
            ],
            options={
                'verbose_name': 'ContactMessage',
                'verbose_name_plural': 'پیام های ارتباط با ما',
            },
        ),
        migrations.CreateModel(
            name='ResumeService',
            fields=[
                ('resumepage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='resume.resumepage')),
                ('resume_index', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resume.resumeindex', verbose_name='resume')),
            ],
            options={
                'verbose_name': 'ResumeService',
                'verbose_name_plural': 'ResumeServices',
            },
            bases=('resume.resumepage',),
        ),
        migrations.CreateModel(
            name='ResumePortfolio',
            fields=[
                ('resumepage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='resume.resumepage')),
                ('filter', models.CharField(choices=[('app', 'app'), ('card', 'card'), ('web', 'web')], default='web', max_length=50, verbose_name='filter')),
                ('category', models.CharField(max_length=500, verbose_name='category')),
                ('resume_index', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resume.resumeindex', verbose_name='resume')),
            ],
            options={
                'verbose_name': 'Portfolio',
                'verbose_name_plural': 'Portfolios',
            },
            bases=('resume.resumepage',),
        ),
        migrations.CreateModel(
            name='Resume',
            fields=[
                ('resumepage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='resume.resumepage')),
                ('start_date', models.DateField(blank=True, null=True, verbose_name='start_date')),
                ('end_date', models.DateField(blank=True, null=True, verbose_name='end_date')),
                ('location', models.CharField(blank=True, max_length=50, null=True, verbose_name='location')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resume.resumecategory', verbose_name='category')),
            ],
            options={
                'verbose_name': 'Resume',
                'verbose_name_plural': 'Resumes',
            },
            bases=('resume.resumepage',),
        ),
    ]
