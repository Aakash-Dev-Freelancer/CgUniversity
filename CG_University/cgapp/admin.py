from django.contrib import admin
from .models import StudentData, Student, MarkSheets

# Register your models here.

admin.site.register(Student)
admin.site.register(StudentData)
admin.site.register(MarkSheets)

