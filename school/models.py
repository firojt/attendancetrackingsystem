from django.db import models
from django.db.models.deletion import CASCADE
from django.urls import reverse

class Student(models.Model):
    """Model representing a campus name"""
    id = models.IntegerField(primary_key='True', max_length=50)
    name = models.CharField(max_length=200, help_text='Enter a student name')
    dob = models.DateField(max_length=200, help_text='Enter a dob ')
    phone = models.CharField(max_length=200, help_text='Enter a student phone no')
    # attendance = models.DecimalField(max_digits = 5, decimal_places = 2)
    # attendance = models.CharField(max_length=200, help_text='Enter a student name')
    # attendance2 = models.CharField(max_length=200, help_text='Enter a student name')

# Metadata
    class Meta:
        ordering = ['-name']

    def __str__(self):
        """String for representing the Model object."""
        return self.name

class Teacher(models.Model):
    """Model representing a campus name"""
    id = models.AutoField(primary_key='True', max_length=50)
    name = models.CharField(max_length=200, help_text='Enter a student name')

    def __str__(self):
        """String for representing the Model object."""
        return self.name

# class is course for us- class is a reserved keyword
class Course(models.Model):
    
    id = models.IntegerField(primary_key='True', max_length=50)
    name = models.CharField(max_length=50)
    classStartDate = models.DateField(default='2021-05-18')
    classEndDate = models.DateField(default='2021-08-10')
    totalClassDay = models.IntegerField(default=30)
    credit = models.CharField(max_length=50)
    sectionName = models.CharField(max_length=200, help_text='Enter a section name')
    student = models.ForeignKey(Student, on_delete=CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=CASCADE)
    
    def __str__(self):
        return self.name


class Attendance(models.Model):
    """Model representing a campus name"""
    id = models.IntegerField(primary_key='True', max_length=50)
    totalAttendanceUptoToday = models.IntegerField(max_length=200, help_text='Enter a student attendance')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    isPresent = models.BooleanField(default='True')
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        sname = Student.objects.get(name=self.student)
        cname = Course.objects.get(name=self.course)
        return '%s : %s: %d' % (sname.name, cname.name, self.totalAttendanceUptoToday)
