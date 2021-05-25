from django.contrib import admin

from .models import Attendance, Campus, Course, Department, Student, Teacher

admin.site.register(Campus)
admin.site.register(Department)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Course)
admin.site.register(Attendance)