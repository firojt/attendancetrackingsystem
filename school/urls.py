
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
    path('home/', views.home_template),
    path('courses/', views.CourseListView.as_view()),
    path('signout/', views.signout, name='signout'),
    path('student/', views.studentAndCourseView),
    path('student/add/', views.studentAndCourseAddView),
    path('student/view/', views.studentDetailedView),
    path('teacher/course/view', views.viewCourse),
    path('teacher/', views.teacherPageView),
]
