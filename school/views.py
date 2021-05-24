
from school.models import Student, Teacher
from django.views import generic
from django.shortcuts import render
from django.http import HttpResponse

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
    return render(request, 'student.html')

from django.views import generic

class StudentListView(generic.ListView):
    model = Student
    context_object_name = 'students'   # your own name for the list as a template variable
    queryset = Student.objects.all
    template_name = 'student.html'  # Specify your own template name/location

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
        return redirect('/student') 
    


