from django.contrib import admin

from .models import Campus, Department, Student, Teacher

admin.site.register(Campus)
admin.site.register(Department)
admin.site.register(Student)
admin.site.register(Teacher)