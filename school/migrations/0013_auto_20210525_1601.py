# Generated by Django 3.2.3 on 2021-05-25 16:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0012_course_student'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='className',
        ),
        migrations.RemoveField(
            model_name='student',
            name='sectionName',
        ),
        migrations.RemoveField(
            model_name='teacher',
            name='className',
        ),
        migrations.RemoveField(
            model_name='teacher',
            name='sectionName',
        ),
        migrations.AddField(
            model_name='course',
            name='sectionName',
            field=models.CharField(default='A', help_text='Enter a section name', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='course',
            name='teacher',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='school.teacher'),
            preserve_default=False,
        ),
    ]