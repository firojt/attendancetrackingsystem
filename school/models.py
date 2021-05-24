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

# Metadata
    class Meta:
        ordering = ['-name']

    def __str__(self):
        """String for representing the Model object."""
        return self.name

class Teacher(models.Model):
    """Model representing a campus name"""
    name = models.CharField(max_length=200, help_text='Enter a Teacher name')

    def __str__(self):
        """String for representing the Model object."""
        return self.name
