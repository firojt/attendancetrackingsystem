
from school.models import Student, Teacher, Course,Attendance
from django.views import generic
from django.shortcuts import render
from django.http import HttpResponse
import sys
import logging


import logging

from django.http import HttpResponse

logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '%(name)-12s %(levelname)-8s %(message)s'
        },
        'file': {
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'file',
            'filename': '/tmp/debug.log'
        }
    },
    'loggers': {
        '': {
            'level': 'DEBUG',
            'handlers': ['console', 'file']
        }
    }
})

# This retrieves a Python logging instance (or creates it)
logger = logging.getLogger(__name__)

# Create your views here.
def school(request):
    return HttpResponse('school page')

def school_template(request):
    context = {
        "first_name" : "Firoj ",
        "last_name"  : "Tml",
    }
    return render(request, 'school.html', context)


def teacher_template(request):
    return render(request, 'teacher.html')

def home_template(request):
    return render(request, 'home.html')


def student_template(request):
    context = {
        "attendace" : "stringval",
    }
    return render(request, 'student.html', context)

def logout(request):
    return render(request, 'logout.html')

from django.views import generic

class StudentListView(generic.ListView):
    model = Student
    context_object_name = 'students'   # your own name for the list as a template variable
    queryset = Student.objects.all
    print(queryset)
    print("from 1 ")
    template_name = 'student.html'  # Specify your own template name/location

def getTotalDays(course,startDate, endDate):
    return 25

# alterante student list view 
def studentAndCourseView(request):
    students = Student.objects.all
    courses = Course.objects.all
    attendaces = Attendance.objects.all
    return render(request, 'student.html', {'courses': courses, 'students': students, 'attendances': attendaces})


class TeacherListView(generic.ListView):
    model = Teacher
    context_object_name = 'teachers'   # your own name for the list as a template variable
    queryset = Teacher.objects.all
    template_name = 'teacher.html'  # Specify your own template name/location



# create separeate view for redirect 
from django.shortcuts import redirect

def login_success(request):
    if request.user.groups.filter(name = 'teacher').exists():
        # user is an admin
        return redirect('/teacher') 
    elif request.user.groups.filter(name = 'student').exists():
        # user is an admin
        # print("from 2")
        # print >>sys.stderr, 'Goodbye, cruel world!'
        logger.info("from logger 1")
        
        return redirect('/student') 

# courses list view 
class CourseListView(generic.ListView):
    model = Course
    context_object_name = 'courses'   # your own name for the list as a template variable
    queryset = Course.objects.all
    print(queryset)
    print("from 1 ")
    template_name = 'courses.html'  # Specify your own template name/location

    


