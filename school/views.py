
from school.models import Student
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

def student_template(request):
    return render(request, 'student.html')

from django.views import generic

class StudentListView(generic.ListView):
    model = Student
    context_object_name = 'students'   # your own name for the list as a template variable
    queryset = Student.objects.all
    template_name = 'student.html'  # Specify your own template name/location


    


