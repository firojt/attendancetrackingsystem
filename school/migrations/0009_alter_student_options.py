# Generated by Django 3.2.3 on 2021-05-25 15:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0008_course'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='student',
            options={'ordering': ['name']},
        ),
    ]