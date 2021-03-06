
import abc
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
from django.contrib.auth.decorators import login_required


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


def signout(request):
    return render(request, 'registration/signout.html')
    
def home_template(request):
    return render(request, 'home.html')

class AttendanceRecord:
    courseName : str
    studentName : str
    attendanceDate : date
    isPresent : bool
    schooloff: bool

    

def unitTestMy():
    attendance1 = AttendanceRecord()
    attendance1.courseName = 'course1'
    attendance1.studentName = 'student1'
    attendance1.attendanceDate = date.today()
    attendance1.isPresent = True


    attrs = vars(attendance1)

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
        courseNameInList = Course.objects.get(pk=attendance['course_id']).name
        studentNameInList = Student.objects.get(pk=attendance['student_id']).name
        if (courseNameInList == course and studentNameInList == student):
            if (attendance['forDate'] == schoolDay):
                return attendance['isPresent']
    return False
  
def alldays(d, end, excluded=(9,10)):
    days = []
    while d <= end:
        if d.isoweekday() not in excluded:
            days.append(d)
        d += datetime.timedelta(days=1)
    return days

def getListofAttendanceRecord(course, student):
    listofAttendanceRecord = []
    # iterate and create list of attendance record
    attendanceList = Attendance.objects.values()             
    list_attendanceList = [entry for entry in attendanceList]  


    courseStartDate = Course.objects.filter(name=course).first().classStartDate
    courseEndDate = Course.objects.filter(name=course).first().classEndDate
    listOfSchoolDays = workdays(courseStartDate, date.today()) 
    allSchoolDays = alldays(courseStartDate, date.today()) 
    for schoolDay in allSchoolDays:
        everyDayAttendance = AttendanceRecord()
        isPresentOnthisDay = wasStudentPresentOnthisDay(schoolDay, course, student, list_attendanceList)
        everyDayAttendance.courseName = course
        everyDayAttendance.studentName = student
        everyDayAttendance.attendanceDate = schoolDay
        everyDayAttendance.isPresent = isPresentOnthisDay
        if (schoolDay not in listOfSchoolDays):
            everyDayAttendance.schooloff = True
        listofAttendanceRecord.append(everyDayAttendance)
    return listofAttendanceRecord

@login_required(login_url='/accounts/login/')    
def studentDetailedView(request):
    # unitTestMy() 
    student = value=request.POST['student']
    course = value=request.POST['course']
    attendances = Attendance.objects.all
    listofAttendanceRecord = getListofAttendanceRecord(course,student)
    context = {'student':student , 'course':course, 'attendances':attendances, 'listofAttendanceRecord':listofAttendanceRecord}
    return render(request, 'viewDetailedAtendance.html', context)

@login_required(login_url='/accounts/login/')
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
    totalAttendaceDays : float
    uptoTodayAttendancePercent: float
    totalSchoolDays: int
    uptoTodaySchoolDays : int
    isTodaysAttendanceDone : bool


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

def getTotalSchoolDays(className):
    classStartDate = Course.objects.get(name=className).classStartDate
    classEndDate = Course.objects.get(name=className).classEndDate
    list_totalSchoolDays = workdays(classStartDate, classEndDate) 
    return len(list_totalSchoolDays)

def getUptoTodayTotalSchoolDays(className):
    classStartDate = Course.objects.get(name=className).classStartDate
    list_totalSchoolDaysUptoToday = workdays(classStartDate, date.today()) 
    return len(list_totalSchoolDaysUptoToday)
    
def retrieveTodaysAttendanceDone(forClass,forStudent):
    student_id = Student.objects.get(name=forStudent).id
    course_id = Course.objects.get(name=forClass).id
    attendancesForParticularClassAndStudent = Attendance.objects.filter(student=student_id, course=course_id).values()
    for each in attendancesForParticularClassAndStudent:
        if(each['forDate'] == date.today()):
            return True
    return False
    
    

def getListofClassForStudent(student):
    # return list of StudetClass
    listofClassForStudent = []
    uniqueListofAttendedClassForStudent = getUniqueListofAttendedClassForStudent(student)
    # for each unique class for student find totalAttendanceDays
    for eachUniqueClass in uniqueListofAttendedClassForStudent:
        studetClass = StudetClass()
        totalAttendaceForClass = getTotalAttendaceForClass(eachUniqueClass,student)
        isTodaysAttendanceDone = retrieveTodaysAttendanceDone(eachUniqueClass,student)
        uptoTodayAttendancePercent = getUptoTodayAttendancePercent(eachUniqueClass,student)

        totalSchoolDays = getTotalSchoolDays(eachUniqueClass)
        uptoTodaySchoolDays = getUptoTodayTotalSchoolDays(eachUniqueClass)
        course = Course.objects.get(name=eachUniqueClass)

        studetClass.courseName = course.name
        studetClass.courseStartDate = course.classStartDate
        studetClass.courseEndDate = course.classEndDate
        studetClass.courseCredit = course.credit
        studetClass.totalAttendaceDays = totalAttendaceForClass
        studetClass.uptoTodayAttendancePercent = uptoTodayAttendancePercent
        studetClass.totalSchoolDays= totalSchoolDays
        studetClass.uptoTodaySchoolDays = uptoTodaySchoolDays
        studetClass.isTodaysAttendanceDone = isTodaysAttendanceDone

        listofClassForStudent.append(studetClass)

    return listofClassForStudent

@login_required(login_url='/accounts/login/')
def studentAndCourseView(request):
    students = Student.objects.all
    courses = Course.objects.all
    attendaces = Attendance.objects.all
    student = request.user.username
    listofStudentClass = getListofClassForStudent(student)
    weekno = datetime.datetime.today().weekday()

    if weekno < 5:
        isSchoolDayToday = True  
    else:
        isSchoolDayToday = False #todo need to change back to False later - frontend validation
    return render(request, 'student.html', {'courses': courses, 'students': students, 'attendances': attendaces, 'listofStudentClass':listofStudentClass, 'isSchoolDayToday':isSchoolDayToday})

def getAllStudentsForThisCourse(course):
    allAttendancesForThisCourse = Attendance.objects.filter(course=course['id']).values()
    list_allAttendancesForThisCourse = [entry for entry in allAttendancesForThisCourse]  
    listOfStudentsForThisCourse = []
    for each in list_allAttendancesForThisCourse:
        listOfStudentsForThisCourse.append(each['student_id'])
    unique_listOfStudentsForThisCourse = list(set(listOfStudentsForThisCourse))
    return unique_listOfStudentsForThisCourse

def getListofStudentsforCourses(courses):
    allCoursesAndStudentsEnrolled = {}
    for eachCourse in courses:
        allStudentsForThisCourse = getAllStudentsForThisCourse(eachCourse)
        eachCourseName = eachCourse['name']
        allCoursesAndStudentsEnrolled[eachCourseName] = allStudentsForThisCourse
    return allCoursesAndStudentsEnrolled

def getTotalAttendanceofStudentForCourse(courseid, studentid):
    attendances = Attendance.objects.filter(course=courseid , student = studentid).values()
    uptoTodayTotalSchoolDays = getUptoTodayTotalSchoolDays(Course.objects.get(id=courseid).name)
    totalAttendancePercent = len(attendances)/uptoTodayTotalSchoolDays * 100
    return totalAttendancePercent


def getTotalAttendancePercentForStudentsForCourse(listofStudentsforCourses):
    courseAndAggregatePercent = {}
    for each in listofStudentsforCourses:
        allStudentPercentage = []
        for eachStudent in listofStudentsforCourses[each]:
            totalAttendanceofStudentForCourse = getTotalAttendanceofStudentForCourse(Course.objects.get(name=each).id, eachStudent)
            allStudentPercentage.append(totalAttendanceofStudentForCourse)
        aggregatePercentageForEachCourse = sum(allStudentPercentage) / len(allStudentPercentage)
        courseAndAggregatePercent[each] = round(aggregatePercentageForEachCourse,2)
    return courseAndAggregatePercent


@login_required(login_url='/accounts/login/')
def teacherPageView(request):
    
     # find assigned courses 
    teacherName = request.user.username
    teacherId = Teacher.objects.get(name=teacherName).id
    assignedCourses = Course.objects.filter(teacher=teacherId).values()

    # for each course find the list of all students enrolled 
    listofStudentsforCourses = getListofStudentsforCourses(assignedCourses)

    # for each course find total percentage
    courseAndAggregatePercent = getTotalAttendancePercentForStudentsForCourse(listofStudentsforCourses)

    # for each student find total attendance percentage 
    # find aggregate percentage
    context= {'teacherName':teacherName, 'courseAndAggregatePercent': courseAndAggregatePercent}
    return render(request, 'teacherPage.html', context)


# alterante student list view 
@login_required(login_url='/accounts/login/')
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

def retrieveAllStudentsForThisCourse(courseName):
    allAttendancesForThisCourse = Attendance.objects.filter(course=Course.objects.get(name=courseName).id).values()
    list_allAttendancesForThisCourse = [entry for entry in allAttendancesForThisCourse]  
    listOfStudentsForThisCourse = []
    for each in list_allAttendancesForThisCourse:
        listOfStudentsForThisCourse.append(each['student_id'])
    unique_listOfStudentsForThisCourse = list(set(listOfStudentsForThisCourse))
    return unique_listOfStudentsForThisCourse


class CourseDetailedViewTeacher:
    student: str
    totalAttendanceUptoToday : int


def viewCourse(request):
    
    submitbutton= request.POST.get("submit")
    course=''
    form= UserForm(request.POST or None)
    attendaces = Attendance.objects.all
    courses = Course.objects.all
    if form.is_valid():
        course= form.cleaned_data.get("course")
    
    courseName =request.POST['course']
    allStudentsForThisCourse = retrieveAllStudentsForThisCourse(courseName)

    # finduptoattendancepercentage for each student
    list_courseDetailedViewTeacher = []
    for eachStudent in allStudentsForThisCourse:
        courseDetailedViewTeacher = CourseDetailedViewTeacher()
        studentName = Student.objects.get(pk=eachStudent).name
        totalAttendaceForClass = getTotalAttendaceForClass(courseName,studentName)
        courseDetailedViewTeacher.student = studentName
        courseDetailedViewTeacher.totalAttendanceUptoToday = totalAttendaceForClass
        list_courseDetailedViewTeacher.append(courseDetailedViewTeacher)

    totalSchoolDays = getTotalSchoolDays(courseName)
    uptoTodaySchoolDays = getUptoTodayTotalSchoolDays(courseName)

    context= {'form': form, 'course': request.POST.get("viewCourse"),
              'submitbutton': submitbutton, 'attendances': attendaces, 'courses':courses, 'courseName':courseName, 'uptoTodaySchoolDays':uptoTodaySchoolDays, 'list_courseDetailedViewTeacher':list_courseDetailedViewTeacher, 'totalSchoolDays':totalSchoolDays}
    
    return render(request, 'viewCourse.html', context)


def retrieveIfTodaysAttendanceNotAlreadyAdded(course, student):
    return True

@login_required(login_url='/accounts/login/')
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

    student =request.POST['student']
    course =request.POST['course']
    isTodaysAttendanceDone = request.POST['istodaysattendanceDoneis']

    courseInstance = Course.objects.get(name=course)
    studentInstance = Student.objects.get(name=student)
    weekno = datetime.datetime.today().weekday()
    todaysAttendanceNotAlreadyAdded = retrieveIfTodaysAttendanceNotAlreadyAdded(course, student)
    if (weekno < 5 and isTodaysAttendanceDone == 'False'): #todo need to change to 5 later  - backend validation
        # then add attendance to the db
        attendance = Attendance()
        attendance.totalAttendanceUptoToday = 12
        attendance.course = courseInstance
        attendance.student = studentInstance
        attendance.isPresent = True
        attendance.forDate = date.today()
        attendance.save()

    studentModel = Student.objects.filter(name=student).first()
    courseModel = Course.objects.filter(name=course).first()
    attendace = Attendance.objects.filter(course=courseModel.id, student=studentModel.id).first()
    attendace.totalAttendanceUptoToday = attendace.totalAttendanceUptoToday + 1
    attendace.save()

    context= {'form': form, 'course': course, 'student':student,
              'submitbutton': submitbutton, 'todaysDate': date.today(), 'todaysAttendanceNotAlreadyAdded':todaysAttendanceNotAlreadyAdded}
    
    return render(request, 'attendanceAdded.html', context)

@login_required(login_url='/accounts/login/')
class TeacherListView(generic.ListView):
    model = Teacher
    context_object_name = 'teachers'   
    queryset = Teacher.objects.all
    template_name = 'teacher.html'  

@login_required(login_url='/accounts/login/')
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



 


