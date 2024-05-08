from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('', views.home, name='home'),
    path('admin_cg/', views.admin, name='admin'),
    path('login/', views.login, name='login'),
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
    path('center/', views.student, name='center'),
    path('edit_student/', views.editStudent, name='edit-student'),

    
    path('logout/', views.logout_view, name='logout'),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
