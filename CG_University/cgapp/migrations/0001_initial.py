# Generated by Django 5.0.4 on 2024-05-19 03:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdminLogin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=100)),
                ('contact_no', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('username', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('password', models.CharField(max_length=100)),
                ('enrollment_no', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('profile_pic', models.FileField(null=True, upload_to='images/students/profile-pic/')),
                ('full_name', models.CharField(max_length=100)),
                ('father_name', models.CharField(max_length=100)),
                ('mother_name', models.CharField(max_length=100)),
                ('gender', models.CharField(max_length=10)),
                ('date_of_birth', models.DateField()),
                ('category', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('mobile_number', models.CharField(max_length=15)),
                ('address', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='StudentLogin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='MarkSheets',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session', models.CharField(max_length=100)),
                ('semester', models.CharField(max_length=100)),
                ('sgpa', models.CharField(max_length=100)),
                ('status', models.CharField(max_length=100)),
                ('result', models.CharField(max_length=100)),
                ('file', models.FileField(null=True, upload_to='images/students/marksheet/')),
                ('student_enrollment_no', models.ForeignKey(db_column='student_enrollment_no', on_delete=django.db.models.deletion.CASCADE, related_name='marksheets', to='cgapp.student')),
            ],
        ),
        migrations.CreateModel(
            name='StudentData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_provision', models.FileField(blank=True, null=True, upload_to='images/students/provision/')),
                ('student_admit_card', models.FileField(blank=True, null=True, upload_to='images/students/admit_card/')),
                ('student_affidavit', models.FileField(blank=True, null=True, upload_to='images/students/affidavit/')),
                ('student_migrations', models.FileField(blank=True, null=True, upload_to='images/students/migrations/')),
                ('student_enrollment_no', models.ForeignKey(db_column='student_enrollment_no', on_delete=django.db.models.deletion.CASCADE, related_name='data', to='cgapp.student')),
            ],
        ),
    ]
