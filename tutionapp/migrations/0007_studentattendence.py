# Generated by Django 5.1.1 on 2024-11-05 09:54

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutionapp', '0006_student_teacher_alter_student_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Studentattendence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Date', models.DateField()),
                ('Attendance', models.CharField(max_length=20)),
                ('student_name', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
