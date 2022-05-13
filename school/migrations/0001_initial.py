# Generated by Django 3.2.13 on 2022-05-13 08:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authentication', '0001_initial'),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='نام واحد درسی ')),
                ('level', models.IntegerField(verbose_name='level')),
                ('course_count', models.IntegerField(verbose_name='تعداد واحد')),
            ],
            options={
                'verbose_name': 'Course',
                'verbose_name_plural': 'Courses',
            },
        ),
        migrations.CreateModel(
            name='EducationalYear',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='title')),
                ('start_date', models.DateTimeField(blank=True, null=True, verbose_name='start_date')),
                ('end_date', models.DateTimeField(blank=True, null=True, verbose_name='end_date')),
            ],
            options={
                'verbose_name': 'EducationalYear',
                'verbose_name_plural': 'EducationalYears',
            },
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='نام مدرسه')),
            ],
            options={
                'verbose_name': 'School',
                'verbose_name_plural': 'Schools',
            },
        ),
        migrations.CreateModel(
            name='SchoolPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.page')),
            ],
            bases=('core.page',),
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('schoolpage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='school.schoolpage')),
            ],
            options={
                'verbose_name': 'Book',
                'verbose_name_plural': 'Books',
            },
            bases=('school.schoolpage',),
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.profile', verbose_name='profile')),
            ],
            options={
                'verbose_name': 'Teacher',
                'verbose_name_plural': 'Teachers',
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.profile', verbose_name='profile')),
            ],
            options={
                'verbose_name': 'Student',
                'verbose_name_plural': 'Students',
            },
        ),
        migrations.CreateModel(
            name='ClassRoom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='نام کلاس')),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.school', verbose_name='مدرسه')),
            ],
            options={
                'verbose_name': 'ClassRoom',
                'verbose_name_plural': 'ClassRooms',
            },
        ),
        migrations.CreateModel(
            name='ActiveCourse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='title')),
                ('start_date', models.DateTimeField(verbose_name='start_date')),
                ('end_date', models.DateTimeField(verbose_name='end_date')),
                ('classroom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.classroom', verbose_name='classroom')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.course', verbose_name='course')),
                ('students', models.ManyToManyField(blank=True, to='school.Student', verbose_name='students')),
                ('teachers', models.ManyToManyField(blank=True, to='school.Teacher', verbose_name='teachers')),
                ('year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.educationalyear', verbose_name='سال تحصیلی')),
            ],
            options={
                'verbose_name': 'ActiveCourse',
                'verbose_name_plural': 'ActiveCourses',
            },
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('schoolpage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='school.schoolpage')),
                ('session_no', models.IntegerField(verbose_name='جلسه شماره ؟')),
                ('start_time', models.DateTimeField(verbose_name='start')),
                ('end_time', models.DateTimeField(verbose_name='start')),
                ('active_course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.activecourse', verbose_name='activecourse')),
            ],
            options={
                'verbose_name': 'Session',
                'verbose_name_plural': 'Sessions',
            },
            bases=('school.schoolpage',),
        ),
        migrations.CreateModel(
            name='Major',
            fields=[
                ('schoolpage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='school.schoolpage')),
                ('courses', models.ManyToManyField(blank=True, to='school.Course', verbose_name='واحد های درسی')),
            ],
            options={
                'verbose_name': 'Major',
                'verbose_name_plural': 'Majors',
            },
            bases=('school.schoolpage',),
        ),
        migrations.AddField(
            model_name='course',
            name='books',
            field=models.ManyToManyField(blank=True, to='school.Book', verbose_name='books'),
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('حاضر', 'حاضر'), ('غایب', 'غایب'), ('نا مشخص', 'نا مشخص'), ('تاخیر', 'تاخیر'), ('تشویق', 'تشویق'), ('تنبیه', 'تنبیه')], max_length=50, verbose_name='status')),
                ('enter_time', models.DateTimeField(blank=True, null=True, verbose_name='enter')),
                ('exit_time', models.DateTimeField(blank=True, null=True, verbose_name='exit')),
                ('time_added', models.DateTimeField(auto_now_add=True, null=True, verbose_name='time_added')),
                ('description', models.CharField(max_length=500, verbose_name='description')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.student', verbose_name='student')),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.session', verbose_name='session')),
            ],
            options={
                'verbose_name': 'Attendance',
                'verbose_name_plural': 'Attendances',
            },
        ),
    ]
