# Generated by Django 3.2.3 on 2021-05-24 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0005_alter_student_attendance'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='attendance2',
            field=models.CharField(default=22, help_text='Enter a student name', max_length=200),
            preserve_default=False,
        ),
    ]