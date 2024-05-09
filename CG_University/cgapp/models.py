# in myapp/models.py
from django.db import models

class Student(models.Model):
    password = models.CharField(max_length=100, null=False)
    enrollment_no = models.CharField(max_length=100, null=False, primary_key=True)
    # profile_pic = models.CharField(max_length=100)
    full_name = models.CharField(max_length=100, null=False)
    father_name = models.CharField(max_length=100)
    mother_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    date_of_birth = models.DateField()
    category = models.CharField(max_length=20)
    email = models.EmailField()
    mobile_number = models.CharField(max_length=15)
    address = models.CharField(max_length=255)

class StudentData(models.Model):
    student_enrollment_no = models.CharField(max_length=100, null=False, primary_key=True)
    student_provision = models.FileField(upload_to='images/students/provision/', null=True)
    student_admit_card = models.FileField(upload_to='images/students/admit_card/', null=True)
    student_affidevit = models.FileField(upload_to='images/students/affidevit/', null=True)
    student_photo = models.ImageField(upload_to='images/students/photos/', null=True)
    student_migrations = models.FileField(upload_to='images/students/migrations/' ,null=True)

class MarkSheets(models.Model):
    student_enrollment_no = models.CharField(max_length=100, null=False)
    session = models.CharField(max_length=100)
    semester = models.CharField(max_length=100)
    sgpa = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    result = models.CharField(max_length=100)
    file = models.FileField(upload_to='images/students/marksheet/', null=True)


class StudentLogin(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

class AdminLogin(models.Model):
    full_name = models.CharField(max_length=100)
    contact_no = models.CharField(max_length=100)
    email = models.EmailField()
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100) 