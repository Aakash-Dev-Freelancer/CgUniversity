from django.contrib import admin
# from .models import Courses
from CG_International_University_App.models.courses import Courses
# from CG_International_University_App.models.admin_student_model import StudentInformation


# Register your models here.
admin.site.register(Courses)
# admin.site.register(StudentInformation)