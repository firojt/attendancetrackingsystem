from django.contrib import admin

from .models import Attendance, Course, Student, Teacher


class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('id','totalAttendanceUptoToday', 'course', 'student', 'isPresent', 'created_date', 'modified_date')

admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Course)
admin.site.register(Attendance, AttendanceAdmin)