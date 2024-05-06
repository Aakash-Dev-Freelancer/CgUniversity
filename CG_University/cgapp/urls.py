
from django.urls import path
from . import views

from cgapp.views import (StudentListCreate, StudentRetrieveUpdateDestroy, StudentLoginAPIView, StudentDataListCreateAPIView, StudentDataRetrieveUpdateDestroyAPIView, upload_student_data)
from cgapp.views import (MarkSheetListCreateView, MarkSheetRetrieveUpdateDestroyView, AdminLoginListCreateView, AdminLoginUpdateDeleteView)


urlpatterns = [
    path('students/', StudentListCreate.as_view(), name='student-list-create'),
    path('students/<str:pk>/', StudentRetrieveUpdateDestroy.as_view(), name='student-detail'),
    path('login/', StudentLoginAPIView.as_view(), name='student-login'),
    
    path('student-data/', StudentDataListCreateAPIView.as_view(), name='student-data-list-create'),
    path('student-data/<str:student_enrollment_no>/', StudentDataRetrieveUpdateDestroyAPIView.as_view(), name='student-data-retrieve-by-enrollment-no'),
    path('marksheets/', MarkSheetListCreateView.as_view(), name='marksheet-list-create'),
    path('marksheets/<int:pk>/', MarkSheetRetrieveUpdateDestroyView.as_view(), name='marksheet-detail'),

    path('admin/login/', AdminLoginListCreateView.as_view(), name='admin-login-list'),
    path('admin/login/<int:pk>/', AdminLoginUpdateDeleteView.as_view(), name='admin-login-detail'),

]
