from django.db import models
from django.db.models.deletion import CASCADE
from django.urls import reverse

# Create your models here.

class Campus(models.Model):
    """Model representing a campus name"""
    name = models.CharField(max_length=200, help_text='Enter a campus name')

    def __str__(self):
        """String for representing the Model object."""
        return self.name


class Department(models.Model):
    """Model representing a campus name"""
    name = models.CharField(max_length=200, help_text='Enter a department name')

    campus = models.ManyToManyField(Campus, help_text='Select a Campus for this dep. note many to many mapping between campus and department')

    def __str__(self):
        """String for representing the Model object."""
        return self.name

class Student(models.Model):
    """Model representing a campus name"""
    id = models.AutoField(primary_key='True', max_length=50)
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
    
    id = models.AutoField(primary_key='True', max_length=50)
    name = models.CharField(max_length=50)
    credit = models.CharField(max_length=50)
    sectionName = models.CharField(max_length=200, help_text='Enter a section name')
    student = models.ForeignKey(Student, on_delete=CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=CASCADE)
    
    def __str__(self):
        return self.name
