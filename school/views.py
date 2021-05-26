
from school.models import Student, Teacher, Course,Attendance
from django.views import generic
from django.shortcuts import render
from django.http import HttpResponse, response
import sys
import logging
from datetime import date
from datetime import timedelta


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

# alterante student list view 
def teacherView(request):
    students = Student.objects.all
    courses = Course.objects.all
    attendaces = Attendance.objects.all
    teachers = Teacher.objects.all
    # attendacesList = Attendance.objects.all().values_list(flat=True)
    # attendacesList = Attendance.objects.filter(id!=0)
    logger.info(type(Attendance.objects.all().values_list(flat=True) ))


    attendanceList = Attendance.objects.values()             # return ValuesQuerySet object
    list_attendanceList = [entry for entry in attendanceList]  # converts ValuesQuerySet into Python list

    # for key, value in attendaces.items():
    #     logger.info(" loop: {}: {}".format(key, value))

    for attendace in list_attendanceList:
        logger.info("attendance for class ")
        logger.info(attendace)
        logger.info("attendance is ")
        logger.info(attendace)

    
    return render(request, 'teacher.html', {'courses': courses, 'students': students, 'attendances': attendaces, 'teachers':teachers})


from django import forms

class UserForm(forms.Form):
    course= forms.CharField(max_length=100)
    student= forms.CharField(max_length=100)
    course11=forms.CharField
    


def studentAndCourseAddView(request):
    logger.info("add attendance is called and the comparable date is ")
   
    logger.info(date.today() + timedelta(days=1))

    # form handling 
    submitbutton= request.POST.get("submit")
    course=''
    student=''
    course11=''

    form= UserForm(request.POST or None)
    # form.save()
    if form.is_valid():
        course= form.cleaned_data.get("course")
        student= form.cleaned_data.get("student")
        course11 = form.cleaned_data.get("course11")

    logger.info("from form data received is course and student ")
    logger.info(course)
    logger.info(request.POST.get('course', ''))
    logger.info(student)
    logger.info("post request is ")
    logger.info(request.POST)
    studentModel = Student.objects.filter(name=student).first()
    courseModel = Course.objects.filter(name=course).first()
    logger.info("studentmodel is ")
    logger.info(studentModel)
    logger.info("coursemodel is ")
    logger.info(courseModel)
    logger.info(courseModel)
    # science id =2 , ram id = 6, current attendance =3
    attendace = Attendance.objects.filter(course=courseModel.id, student=studentModel.id).first()
    logger.info("attendance is ")
    # logger.info(attendace)
    attendace.totalAttendanceUptoToday = attendace.totalAttendanceUptoToday + 1
    attendace.save()
    # attendace
#    attendaces = Attendance.objects.all
# t.value = 999  # change field
# t.save() # this will update only

    context= {'form': form, 'course': course, 'student':student,
              'submitbutton': submitbutton}
    
    return render(request, 'attendanceAdded.html', context)


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

    


