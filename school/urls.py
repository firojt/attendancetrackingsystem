
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from . import views
def home(request):
    return HttpResponse('Home page')


def contact(request):
    return HttpResponse('Contact page')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', home),
    path('contact/', contact),
    path('school/', views.school),
    path('school2/', views.school_template),
    # path('student/', views.student_template),
    path('teacher/', views.teacher_template),
    path('student/', views.StudentListView.as_view(), name='students'),
]
