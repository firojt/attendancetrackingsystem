
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
import datetime


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

class AttendanceRecord:
    courseName : str
    studentName : str
    attendanceDate : date
    isPresent : bool

    

def unitTestMy():
    attendance1 = AttendanceRecord()
    attendance1.courseName = 'course1'
    attendance1.studentName = 'student1'
    attendance1.attendanceDate = date.today()
    attendance1.isPresent = True

    logger.info("object created and x is " )
    attrs = vars(attendance1)
    logger.info(', '.join("%s: %s" % item for item in attrs.items()))
    # logger.info(str(attendance1.attendanceDate))

# 1st start date , 2nd is the end date and 3rd is default that excludes saturday=6 and sunday=7
def workdays(d, end, excluded=(6, 7)):
    days = []
    while d <= end:
        if d.isoweekday() not in excluded:
            days.append(d)
        d += datetime.timedelta(days=1)
    return days

def wasStudentPresentOnthisDay(schoolDay, course, student, list_attendanceList):
    for attendance in list_attendanceList:
        # if (attendance['student'] == student and attendance['course'])
        logger.info("ispresent - attendance total = '{0}' school day is '{1}'".format(attendance['course_id'], schoolDay))
        courseNameInList = Course.objects.get(pk=attendance['course_id']).name
        studentNameInList = Student.objects.get(pk=attendance['student_id']).name
        logger.info("ispresent - attendance course = '{0}' student is  '{1}'".format(courseNameInList, studentNameInList))
        if (courseNameInList == course and studentNameInList == student):
            logger.info("course and student name matches school day is '{0}' and attendanceDate is '{1}'".format(schoolDay , attendance['forDate']))
            if (attendance['forDate'] == schoolDay):
                return attendance['isPresent']
    return False
  

def getListofAttendanceRecord(course, student):
    listofAttendanceRecord = []
    logger.info("getListofAttendanceRecord am called")
    # iterate and create list of attendance record
    attendanceList = Attendance.objects.values()             
    list_attendanceList = [entry for entry in attendanceList]  
    logger.info("total attendance record in db are- ")
    logger.info(len(list_attendanceList))
    courseStartDate = Course.objects.filter(name=course).first().classStartDate
    courseEndDate = Course.objects.filter(name=course).first().classEndDate
    logger.info("course start date and end date are ")
    logger.info(courseStartDate)
    logger.info(courseEndDate)
    logger.info(type(courseStartDate))
    listOfSchoolDays = workdays(courseStartDate, date.today()) 
    logger.info("list of school days are ")
    logger.info(listOfSchoolDays)
    logger.info("total school days is ")
    logger.info(len(listOfSchoolDays))
    for schoolDay in listOfSchoolDays:
        everyDayAttendance = AttendanceRecord()
        logger.info("date = %s" % schoolDay)
        isPresentOnthisDay = wasStudentPresentOnthisDay(schoolDay, course, student, list_attendanceList)
        everyDayAttendance.courseName = course
        everyDayAttendance.studentName = student
        everyDayAttendance.attendanceDate = schoolDay
        everyDayAttendance.isPresent = isPresentOnthisDay
        listofAttendanceRecord.append(everyDayAttendance)
    return listofAttendanceRecord
        
def studentDetailedView(request):
    # unitTestMy() 
    logger.info("************************************")
    # logger.info(workdays(datetime.datetime(2021, 5, 5),
            #    datetime.datetime(2021, 5, 30)))
    logger.info("************************************")
    student = value=request.POST['student']
    course = value=request.POST['course']
    attendances = Attendance.objects.all
    listofAttendanceRecord = getListofAttendanceRecord(course,student)
    context = {'student':student , 'course':course, 'attendances':attendances, 'listofAttendanceRecord':listofAttendanceRecord}
    logger.info("before passing to render")
    logger.info([each.attendanceDate for each in listofAttendanceRecord])
    return render(request, 'viewDetailedAtendance.html', context)

class StudentListView(generic.ListView):
    model = Student
    context_object_name = 'students'   # your own name for the list as a template variable
    queryset = Student.objects.all
    print(queryset)
    print("from 1 ")
    template_name = 'student.html'  # Specify your own template name/location

class StudetClass:
    courseName: str
    courseStartDate : str
    courseEndDate : str
    courseCredit : int
    totalAttendacePercent : float
    uptoTodayAttendancePercent: float
    totalSchoolDays: int
    uptoTodaySchoolDays : int


def getTotalAttendanceForClass(courseNameInList):
    return 5

def getUniqueListofAttendedClassForStudent(student):
    listofClass = []
    student_id = Student.objects.get(name=student).id
    allAttendancesForThisStudent = Attendance.objects.filter(student=student_id).values()
    list_allAttendancesForThisStudent = [entry for entry in allAttendancesForThisStudent]  
    for attendanceForThisStudent in list_allAttendancesForThisStudent:
        courseKey = (attendanceForThisStudent['course_id'])
        courseName = Course.objects.get(pk=courseKey).name
        listofClass.append(courseName)
    setFromList = set(listofClass)
    listFromSet = list(setFromList)
    return listFromSet

def getTotalAttendaceForClass(forClass,forStudent):
    student_id = Student.objects.get(name=forStudent).id
    course_id = Course.objects.get(name=forClass).id
    attendancesForParticularClassAndStudent = Attendance.objects.filter(student=student_id, course=course_id).values()
    list_attendancesForParticularClassAndStudent = [entry for entry in attendancesForParticularClassAndStudent] 
    totalAttendences = 0
    for each in attendancesForParticularClassAndStudent:
        if(each['isPresent']):
            totalAttendences += 1
    return totalAttendences

def getUptoTodayAttendancePercent(forClass,forStudent):
    return 6

def getListofClassForStudent(student):
    # return list of StudetClass
    listofClassForStudent = []
    uniqueListofAttendedClassForStudent = getUniqueListofAttendedClassForStudent(student)
    # for each unique class for student find totalAttendanceDays
    for eachUniqueClass in uniqueListofAttendedClassForStudent:
        studetClass = StudetClass()
        totalAttendaceForClass = getTotalAttendaceForClass(eachUniqueClass,student)
        uptoTodayAttendancePercent = getUptoTodayAttendancePercent(eachUniqueClass,student)
        course = Course.objects.get(name=eachUniqueClass)
        studetClass.courseName = course.name
        studetClass.courseStartDate = course.classStartDate
        studetClass.courseEndDate = course.classEndDate
        studetClass.courseCredit = course.credit
        studetClass.totalAttendacePercent = totalAttendaceForClass
        studetClass.uptoTodayAttendancePercent = uptoTodayAttendancePercent
        studetClass.totalSchoolDays= 33
        studetClass.uptoTodaySchoolDays = 12
        listofClassForStudent.append(studetClass)
    return listofClassForStudent


    

    # attendanceList = Attendance.objects.values()             
    # list_attendanceList = [entry for entry in attendanceList]  
    # totalSchoolDays = 12


    # for attendance in list_attendanceList:
    #     studentNameInList = Student.objects.get(pk=attendance['student_id']).name
    #     if(studentNameInList == student):
            
    #         courseNameInList = Course.objects.get(pk=attendance['course_id']).name
    #         totalAttendanceForClass  = getTotalAttendanceForClass(courseNameInList)
    #         courseStartDate = Course.objects.filter(name=courseNameInList).first().classStartDate
    #         courseEndDate = Course.objects.filter(name=courseNameInList).first().classEndDate
    #         totalSchoolDays = len(workdays(courseStartDate, courseEndDate))

        


# alterante student list view 
def studentAndCourseView(request):
    students = Student.objects.all
    courses = Course.objects.all
    attendaces = Attendance.objects.all
    student = request.user.username
    listofStudentClass = getListofClassForStudent(student)
    return render(request, 'student.html', {'courses': courses, 'students': students, 'attendances': attendaces, 'listofStudentClass':listofStudentClass})

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



 


