
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
from django.views import generic
from django import forms
from django.shortcuts import redirect

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

def logout(request):
    return render(request, 'logout.html')
    
def home_template(request):
    return render(request, 'home.html')


class StudentListView(generic.ListView):
    model = Student
    context_object_name = 'students'   # your own name for the list as a template variable
    queryset = Student.objects.all
    print(queryset)
    print("from 1 ")
    template_name = 'student.html'  # Specify your own template name/location

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

    attendanceList = Attendance.objects.values()             
    list_attendanceList = [entry for entry in attendanceList]  

    my_attendance_dict = {}
    listofPercentage = []
    for attendace in list_attendanceList:
        currentKeyInt = (attendace['course_id'])
        currentKey = Course.objects.get(pk=currentKeyInt).name
        currentValue= (attendace['totalAttendanceUptoToday'])
        totalSchoolDaysForCurrentClass = Course.objects.get(pk=currentKeyInt).totalClassDay
        if currentKey in my_attendance_dict:
            currentPercent = currentValue / totalSchoolDaysForCurrentClass * 100
            listofPercentage.append(currentPercent)
            averagePercentIs = sum(listofPercentage) / len(listofPercentage)
            averagePercentIs = round(averagePercentIs, 2)
            my_attendance_dict[currentKey] = averagePercentIs      
        else:
            currentPercent = currentValue / totalSchoolDaysForCurrentClass * 100
            listofPercentage.append(currentPercent)
            currentPercent = round(currentPercent, 2)
            my_attendance_dict[currentKey] = currentPercent

    return render(request, 'teacher.html', {'courses': courses, 'students': students, 'attendances': attendaces, 'teachers':teachers, 'my_attendance_dict':my_attendance_dict})

class UserForm(forms.Form):
    course= forms.CharField(max_length=100)
    student= forms.CharField(max_length=100)
    course11=forms.CharField
    
def viewCourse(request):
    submitbutton= request.POST.get("submit")
    course=''
    form= UserForm(request.POST or None)
    attendaces = Attendance.objects.all
    courses = Course.objects.all
    if form.is_valid():
        course= form.cleaned_data.get("course")
    context= {'form': form, 'course': request.POST.get("viewCourse"),
              'submitbutton': submitbutton, 'attendances': attendaces, 'courses':courses}
    
    return render(request, 'viewCourse.html', context)


def studentAndCourseAddView(request):
    # form handling 
    submitbutton= request.POST.get("submit")
    course=''
    student=''
    course11=''

    form= UserForm(request.POST or None)
    if form.is_valid():
        course= form.cleaned_data.get("course")
        student= form.cleaned_data.get("student")

    studentModel = Student.objects.filter(name=student).first()
    courseModel = Course.objects.filter(name=course).first()
    attendace = Attendance.objects.filter(course=courseModel.id, student=studentModel.id).first()
    attendace.totalAttendanceUptoToday = attendace.totalAttendanceUptoToday + 1
    attendace.save()

    context= {'form': form, 'course': course, 'student':student,
              'submitbutton': submitbutton}
    
    return render(request, 'attendanceAdded.html', context)


class TeacherListView(generic.ListView):
    model = Teacher
    context_object_name = 'teachers'   
    queryset = Teacher.objects.all
    template_name = 'teacher.html'  

def login_success(request):
    if request.user.groups.filter(name = 'teacher').exists():
        return redirect('/teacher') 
    elif request.user.groups.filter(name = 'student').exists():
        return redirect('/student') 

class CourseListView(generic.ListView):
    model = Course
    context_object_name = 'courses'   # your own name for the list as a template variable
    queryset = Course.objects.all
    template_name = 'courses.html'  # Specify your own template name/location

    


