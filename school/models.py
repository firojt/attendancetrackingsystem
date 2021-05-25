from django.db import models
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
    name = models.CharField(max_length=200, help_text='Enter a student name')
    className = models.CharField(max_length=200, help_text='Enter a student name')
    sectionName = models.CharField(max_length=200, help_text='Enter a student name')
    # attendance = models.DecimalField(max_digits = 5, decimal_places = 2)
    attendance = models.CharField(max_length=200, help_text='Enter a student name')
    attendance2 = models.CharField(max_length=200, help_text='Enter a student name')

# Metadata
    class Meta:
        ordering = ['name']

    def __str__(self):
        """String for representing the Model object."""
        return self.name

class Teacher(models.Model):
    """Model representing a campus name"""
    name = models.CharField(max_length=200, help_text='Enter a student name')
    className = models.CharField(max_length=200, help_text='Enter a student name')
    sectionName = models.CharField(max_length=200, help_text='Enter a student name')

    def __str__(self):
        """String for representing the Model object."""
        return self.name

class Course(models.Model):
    Department = models.ForeignKey(Department, on_delete=models.CASCADE)
    id = models.CharField(primary_key='True', max_length=50)
    name = models.CharField(max_length=50)
    shortname = models.CharField(max_length=50, default='X')

    def __str__(self):
        return self.name

