# Generated by Django 3.2.3 on 2021-05-29 21:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0022_attendance_fordate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='forDate',
            field=models.DateField(blank=True, default=None, null=True),
        ),
    ]