from django.contrib import admin
from .models import StudentData, Student, MarkSheets, AdminLogin

# Register your models here.

admin.site.register(Student)
admin.site.register(StudentData)
admin.site.register(MarkSheets)
admin.site.register(AdminLogin)

