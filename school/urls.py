
from django import urls
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from . import views
def home(request):
    return HttpResponse('Home page')


def contact(request):
    return HttpResponse('Contact page')

urlpatterns = [
    url(r'login_success/$', views.login_success, name='login_success'),
    path('admin/', admin.site.urls),
    # path('home/', home),
    path('courses/', views.CourseListView.as_view()),
    path('school/', views.school),
    
    path('addAttendace/', views.school),
    path('school2/', views.school_template),
     path('logout/', views.logout),
    path('home/', views.home_template),
    path('student/', views.studentAndCourseView),
    path('teacher/', views.TeacherListView.as_view()),
]
