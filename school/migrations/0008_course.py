# Generated by Django 3.2.3 on 2021-05-24 18:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0007_auto_20210524_1743'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.CharField(max_length=50, primary_key='True', serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('shortname', models.CharField(default='X', max_length=50)),
                ('Department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.department')),
            ],
        ),
    ]
