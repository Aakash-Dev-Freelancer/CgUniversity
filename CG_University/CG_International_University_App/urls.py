from django.urls import path
from . import views
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

from django.conf.urls import handler404

urlpatterns = [
    path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type='text/plain')),
    
    path('admin_cg/', views.admin, name='admin'),
    path('login/', views.login, name='login'),
    
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('director_message/', views.directorMessage, name='director_message'),
    path('vision_and_mission/', views.visionAndMission,
         name='vision_and_mission'),
    path('courses/', views.courses, name='courses'),
    path('board_members/', views.boardMembers, name='board_members'),
    path('terms_and_conditions/', views.termsAndconditions,
         name='terms_and_conditions'),
    path('rti/', views.rti, name='rti'),
    path('approval/', views.approval, name='approval'),
    path('contact/', views.contact, name='contact'),
    path('student/', views.student, name='student'),
    path('center/', views.center, name='center'),
    
    path('edit_student/', views.editStudent, name='edit-student'),
    path('delete_student/', views.delete_student, name='delete-student'),
    
    
    path('view_student/', views.viewStudent, name='view-student'),
    path('logout/', views.logout_view, name='logout'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = 'CG_International_University_App.views.custom_404'
