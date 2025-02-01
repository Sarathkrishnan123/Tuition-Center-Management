from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User

class CustomUser(AbstractUser):
    user_type=models.CharField(default=1,max_length=200)
    status=models.IntegerField(default=0)

class Course(models.Model):
    course_name=models.CharField(max_length=255)
    Duration=models.CharField(max_length=255)
    fee=models.IntegerField()
    syllabus=models.FileField(upload_to='files/',blank=True,null=True)

class Teacher(models.Model):
    course=models.ForeignKey(Course,on_delete=models.CASCADE,null=True)
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True)
    Age=models.IntegerField()
    Phone_number=models.CharField(max_length=255)
    Image=models.ImageField(upload_to='image/',null=True,blank=True)

class Student(models.Model):
    course=models.ForeignKey(Course,on_delete=models.CASCADE,null=True)
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True,related_name='student_assignment')
    Age=models.IntegerField()
    Phone_number=models.CharField(max_length=255)
    Image=models.ImageField(upload_to='simage/',null=True,blank=True)
    teacher=models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True,related_name='teacher_assignment')

class Teacherattendence(models.Model):
    teacher_name=models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True)
    Date=models.DateField()
    Attendance=models.CharField(max_length=20)

class Studentattendence(models.Model):
    student_name=models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True)
    Date=models.DateField()
    Attendance=models.CharField(max_length=20)

class Task(models.Model):
    task_name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True)

class TaskSubmission(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Assuming User model is used for students
    file = models.FileField(upload_to='task_submissions/')
    description = models.TextField(blank=True)
    submission_date = models.DateTimeField(auto_now_add=True)





