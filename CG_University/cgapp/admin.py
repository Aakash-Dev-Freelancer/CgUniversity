from django.contrib import admin
from .models import StudentData, Student, MarkSheets, AdminLogin, StudentLogin, Center

# Register your models here.

admin.site.register(Student)
admin.site.register(StudentData)
admin.site.register(MarkSheets)
admin.site.register(AdminLogin)
admin.site.register(StudentLogin)
admin.site.register(Center)

