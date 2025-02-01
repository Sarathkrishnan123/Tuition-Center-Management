from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import login, authenticate
from .models import Course
from .models import CustomUser
from .models import Teacher
from .models import Student
from .models import Teacherattendence
from .models import Studentattendence
from django.db.models import Q
import random
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
import re
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import update_session_auth_hash
from .models import Task,TaskSubmission


def home(request):
    return render(request,'home.html')

def log(request):
    return render(request,'log.html')

def teacher(request):
    courses=Course.objects.all()
    return render(request,'teacher.html',{'course':courses})

def student(request):
   courses=Course.objects.all()
   return render(request,'student.html',{'course':courses})

def add_teacher(request):
    if request.method == "POST":
        firstname = request.POST['Fname']
        lastname = request.POST['Lname']
        username = request.POST['Uname']
        Age = request.POST['age']
        email = request.POST['email']
        contact = request.POST['Pno']
        user_type = request.POST['text']
        sel1 = request.POST['sel']
        Image = request.FILES.get('file')

        # Check if username already exists
        if CustomUser.objects.filter(username=username).exists():
            messages.success(request, 'Username already exists. Please choose another.')
            return redirect('teacher')

        # Check if email already exists
        if CustomUser.objects.filter(email=email).exists():
            messages.success(request, 'Email already exists. Please choose another.')
            return render(request, 'teacher.html')

        # Validate email format
        try:
            validate_email(email)
            if not email.endswith('.com'):
                raise ValidationError("Invalid email format.")
        except ValidationError:
            messages.success(request, 'Enter a valid email ID.')
            return render(request, 'teacher.html')

        # Validate mobile number format (exactly 10 digits)
        if not re.match(r'^\d{10}$', contact):
            messages.success(request, 'Enter a valid Mobile number.')
            return render(request, 'teacher.html')

        # Get course object
        try:
            course2 = Course.objects.get(id=sel1)
        except Course.DoesNotExist:
            messages.success(request, 'Selected course does not exist.')
            return render(request, 'teacher.html')
        
        
        

        # Create user and teacher entries after all validations pass
        user = CustomUser.objects.create_user(
            username=username,
            first_name=firstname,
            last_name=lastname,
            email=email,
            user_type=user_type
        )
        user.save()

        teacher = Teacher(
            user=user,
            course=course2,
            Age=Age,
            Phone_number=contact,
            Image=Image
        )
        teacher.save()
        messages.success(request, 'Teacher added successfully.')
        return render(request, 'teacher.html')

        
        
    return redirect('log')  # Redirect after successful creation

    
def add_student(request):
    if request.method == "POST":
        firstname = request.POST['Fname']
        lastname = request.POST['Lname']
        username = request.POST['Uname']
        Age = request.POST['age']
        email = request.POST['email']
        contact = request.POST['Pno']
        user_type=request.POST['text']
        sel1 = request.POST['sel']
        course2 = Course.objects.get(id=sel1)
        Image = request.FILES.get('file')

         # Check if username already exists
        if CustomUser.objects.filter(username=username).exists():
            messages.success(request, 'Username already exists. Please choose another.')
            return render(request, 'student.html')

        # Check if email already exists
        if CustomUser.objects.filter(email=email).exists():
            messages.success(request, 'Email already exists. Please choose another.')
            return render(request, 'student.html')

        # Validate email format
        try:
            validate_email(email)
            if not email.endswith('.com'):
                raise ValidationError("Invalid email format.")
        except ValidationError:
            messages.success(request, 'Enter a valid email ID.')
            return render(request, 'student.html')

        # Validate mobile number format (exactly 10 digits)
        if not re.match(r'^\d{10}$', contact):
            messages.success(request, 'Enter a valid Mobile number.')
            return render(request, 'student.html')

        # Get course object
        try:
            course2 = Course.objects.get(id=sel1)
        except Course.DoesNotExist:
            messages.success(request, 'Selected course does not exist.')
            return render(request, 'student.html')
        

        user = CustomUser.objects.create_user(
            username=username,
            first_name=firstname,
            last_name=lastname,
            email=email,
            user_type=user_type)

        user.save()

        student = Student(
            user=user,
            course=course2,
            Age=Age,
            Phone_number=contact,
            Image=Image
        )
        student.save()
        messages.success(request, 'Student added successfully.')
        return render(request, 'student.html')

        
        
    return redirect('log')  # Redirect after successful creation
    


    



def admin(request):
    return render(request,'admin.html')

def add_course(request):
    return render(request,'add_course.html')

def add_coursedb(request):
    if request.method=="POST":
        course_name=request.POST['cname']
        fee=request.POST['cfee']
        syllabus=request.FILES.get('syllabus')
        duration=request.POST['duration']
        course=Course(course_name=course_name,fee=fee,Duration=duration,syllabus=syllabus)
        course.save()
        messages.success(request, 'Course added successfully.')
        return redirect('add_course')
    
def approvedisapprove(request):
    users = CustomUser.objects.filter(~Q(user_type=1))

    user_data = []
    for user in users:
        if user.user_type == "2":  # Teacher
            teacher = Teacher.objects.filter(user=user).first()
            if teacher:
                user_data.append({
                    'user': user,
                    'course': teacher.course.course_name if teacher.course else 'N/A',
                    'age': teacher.Age,
                    'phone_number': teacher.Phone_number,
                    'image': teacher.Image.url if teacher.Image else None,
                })
        elif user.user_type == "3":  # Student
            student = Student.objects.filter(user=user).first()
            if student:
                user_data.append({
                    'user': user,
                    'course': student.course.course_name if student.course else 'N/A',
                    'age': student.Age,
                    'phone_number': student.Phone_number,
                    'image': student.Image.url if student.Image else None,
                })

    return render(request, 'approvedisapprove.html', {'user_data': user_data})

from django.db.models import Q

def admin_view(request):
    # Count of unapproved users (status = 0)
    unapproved_count=CustomUser.objects.filter(status=0).count()
    count=unapproved_count-1
    print(count)
    return render(request,'admin.html',{'unapproved_count':count})


def approve(request, k):
    usr = CustomUser.objects.get(id=k)
    usr.status = 1
    usr.save()

    if usr.user_type == '2':
        tea = Teacher.objects.get(user=k)
        password = str(random.randint(100000, 999999))
        print(password)
        usr.set_password(password)
        usr.save()

        send_mail(
            'Admin approved',
            f'Username: {tea.user.username}\nPassword: {password}\nEmail: {tea.user.email}',
            settings.EMAIL_HOST_USER,
            [tea.user.email]
        )
        messages.info(request, 'Teacher approved.')
    elif usr.user_type == '3':
        stu = Student.objects.get(user=k)
        password = str(random.randint(100000, 999999))
        usr.set_password(password)
        usr.save()

        send_mail(
            'Admin approved',
            f'Username: {stu.user.username}\nPassword: {password}\nEmail: {stu.user.email}',
            settings.EMAIL_HOST_USER,
            [usr.email]
        )
        messages.info(request, 'Student approved.')
    
    return redirect('approvedisapprove')

def disapprove(request, k):
    usr = CustomUser.objects.get(id=k)
    if usr.user_type == '2':
        Teacher.objects.filter(user=k).delete()
    elif usr.user_type == '3':
        Student.objects.filter(user=k).delete()
    
    usr.delete()
    messages.info(request, 'User disapproved.')
    return redirect('approvedisapprove')

def login1(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(username=username,password=password)

        if user is not None:
            if user.user_type=='1':
                login(request,user)
                return redirect('admin_view')
            elif user.user_type=='2':
                auth.login(request,user)
                return redirect('T_admin')
            elif user.user_type=='3':
                auth.login(request,user)
                return redirect('S_admin')

            
def managecourse(request):
    course=Course.objects.all()
    return render(request,'managecourse.html',{'crs':course})

@login_required
def tcr_table(request):
    teacher = Teacher.objects.all()
    return render(request, 'tcr_table.html', {'tcr': teacher})

def dlt(request,lk):
    tcr2=Teacher.objects.get(id=lk)
    tcr2.delete()
    tcr2.user.delete()
    return redirect('tcr_table')

def std_table(request):
    student=Student.objects.all()
    return render(request,'std_table.html',{'std':student})

def sdlt(request,sk):
    std2=Student.objects.get(id=sk)
    std2.delete()
    std2.user.delete()
    return redirect('std_table')

def t_attend(request):
    tcr=CustomUser.objects.filter(user_type='2')
    return render(request,'t_attend.html',{'tcr':tcr})

def t_attenddb(request):
    if request.method=='POST':
        tname=request.POST['tsa']
        tn=CustomUser.objects.get(id=tname)
        tdate=request.POST['date']
        tatt=request.POST['Attendance']
        teach=Teacherattendence(teacher_name=tn,Date=tdate,Attendance=tatt)
        teach.save()
        messages.info(request,'Attendance added')
        return redirect('t_attend')

def vta(request):
    tename=CustomUser.objects.filter(user_type='2')
    return render(request,'view_tattend.html',{'te':tename})

def vtadb(request):
    if request.method=='POST':
        opt=request.POST['tse']
        tec=Teacher.objects.get(user=opt)
        teach=tec.user
        startdate=request.POST['sdate']
        enddate=request.POST['edate']
        attend=Teacherattendence.objects.filter(teacher_name=teach,Date__range=[startdate,enddate])
        return render(request,'show_tattend.html',{'tea':teach, 'atd':attend})
def sta(request):
    return render(request,'show_tattend.html')

def logout(request):
    return render(request,'log.html')

def assign(request):
    course=Course.objects.all()
    teacher=Teacher.objects.all()
    student=Student.objects.all()
    return render(request,'assign_teacher.html',{'teacher':teacher,'course':course,'student':student})

def assign_teacher(request, student_id, teacher_id):
    student = CustomUser.objects.get(id=student_id)
    teacher = CustomUser.objects.get(id=teacher_id)
    user=Student.objects.get(user=student)
    user.teacher=teacher
    user.save()
    return redirect('assign')

def T_admin(request):
    return render(request,'T_admin.html')

@login_required
def mark_attendance(request):
    # Ensure only teachers can access this page
    if request.user.user_type == '2':  # Assuming '2' indicates a teacher
        # Retrieve students assigned to the logged-in teacher
        students = Student.objects.filter(teacher=request.user)
        return render(request, 'student_attendance.html', {'students': students})
    else:
        return redirect('T_admin')  # Redirect non-teachers to a different page

@login_required
def save_attendance(request):
    if request.method == 'POST':
        student_id = request.POST.get('student')
        attendance_date = request.POST.get('date')
        attendance_status = request.POST.get('attendance')

        # Check if student_id is provided
        if not student_id:
            return HttpResponse("Student ID not provided.", status=400)

        # Verify that the student is assigned to the logged-in teacher
        try:
            student = Student.objects.get(id=student_id, teacher=request.user)
        except Student.DoesNotExist:
            return HttpResponse("Student does not exist or is not assigned to you.", status=404)

        # Save the attendance record for the specified student
        Studentattendence.objects.create(
            student_name=student.user,  # Using CustomUser instance of the student
            Date=attendance_date,
            Attendance=attendance_status
        )

        # Redirect back to the attendance marking page
        messages.success(request, "Attendance marked successfully!")
        return redirect('mark_attendance')
    
    return redirect('mark_attendance')

@login_required
def view_attendance(request):
    form_submitted = False  # Variable to track if form is submitted
    attendance_records = []  # Initialize an empty list for attendance records

    # Check if the logged-in user is a teacher
    if request.user.user_type == '2':  # Assuming '2' indicates a teacher
        # Retrieve students assigned to the logged-in teacher
        students = Student.objects.filter(teacher=request.user)
    else:
        # If not a teacher, return no students
        students = Student.objects.none()

    if request.method == 'POST':
        form_submitted = True  # Set form_submitted to True on form submission
        student_id = request.POST.get('tse')  # Student selection input name
        start_date = request.POST.get('sdate')  # Start date input name
        end_date = request.POST.get('edate')  # End date input name

        # Ensure all fields are provided
        if student_id and start_date and end_date:
            # Convert dates from string to date format
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

            # Filter attendance records for the selected student's CustomUser ID and date range
            attendance_records = Studentattendence.objects.filter(
                student_name_id=Student.objects.get(id=student_id).user.id,
                Date__range=(start_date, end_date)
            )

    # Render the template with the list of students, attendance records, and form submission status
    return render(request, 'view_attendance.html', {
        'students': students,
        'attendance_records': attendance_records,
        'form_submitted': form_submitted
    })
def view_syllabus(request):
    if request.user.is_authenticated:
        # Get the teacher instance for the logged-in user
        teacher = Teacher.objects.get(user=request.user)
        # Get all courses taught by this teacher
        courses = Course.objects.filter(teacher=teacher)  # Adjusted line
        return render(request, 'view_syllabus.html', {'courses': courses})
    else:
        return render(request, 'T_admin.html')  # or redirect to login page
    
from django.shortcuts import render
from .models import Student

def view_students(request):
    if request.user.is_authenticated and request.user.user_type == '2':  # Assuming '2' is the user type for teachers
        teacher = request.user
        students = Student.objects.filter(teacher=teacher)

        return render(request, 'view_students.html', {'students': students})
    else:
        return render(request, 'access_denied.html')  # Handle unauthorized access
    
@login_required
def name_view(request):
    context = {
        'username': request.user.first_name  # or request.user.username if you prefer
    }
    return render(request, 'T_admin.html', context)

@login_required
def reset_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        # Check if the current password is correct
        if not request.user.check_password(current_password):
            messages.error(request, "Current password is incorrect.")
            return redirect('reset_password')

        # Check if the new password and confirmation match
        if new_password != confirm_password:
            messages.error(request, "New passwords do not match.")
            return redirect('reset_password')

        # Password complexity check
        if not is_password_valid(new_password):
            messages.error(request, "Password must be at least 6 characters long and contain at least one uppercase letter, one digit, and one special character.")
            return redirect('reset_password')

        # Update the password if validations pass
        request.user.set_password(new_password)
        request.user.save()

        # Update the session so the user remains logged in
        update_session_auth_hash(request, request.user)
        messages.success(request, "Your password has been reset successfully.")
        return redirect('reset_password')  # Replace with the page you want to redirect to
    
    return render(request, 'reset_password.html')

def is_password_valid(password):
    # Check the password against the complexity requirements
    if (len(password) >= 6 and
        re.search(r'[A-Z]', password) and     # At least one uppercase letter
        re.search(r'\d', password) and        # At least one digit
        re.search(r'[!@#$%^&*(),.?":{}|<>]', password)):  # At least one special character
        return True
    return False

def S_admin(request):
    return render(request,'S_admin.html')   

@login_required
def student_view_own_attendance(request):
    # Check if the logged-in user is a student
    if request.user.user_type == '3':  # Assuming '1' indicates a student
        # Retrieve attendance records for the logged-in student
        attendance_records = Studentattendence.objects.filter(student_name=request.user)

        return render(request, 'student_view_attendance.html', {
            'attendance_records': attendance_records
        })
    else:
        return redirect('S_admin')  # Redirect non-students to the home page
    
def syllabus(request):
    if request.user.is_authenticated:
        # Get the student instance for the logged-in user
        student = request.user.student_assignment.first()  # Get the first student related to the user
        
        if student:
            # Get the course for this student
            course = student.course
            syllabus = course.syllabus  # Get the syllabus file for the course
            return render(request, 'syllabus.html', {'course': course, 'syllabus': syllabus})
        else:
            return render(request, 'error.html', {'message': 'Student not found'})
    else:
        return render(request, 'login.html')  # or redirect to login page
    
from django.shortcuts import render
from .models import Student

def student_profile(request):
    if request.user.is_authenticated:
        # Retrieve the Student instance for the logged-in user
        student = Student.objects.get(user=request.user)
        return render(request, 'student_profile.html', {'student': student})
    else:
        return redirect('login')  # Redirect to login if not authenticated
    
@login_required
def reset_password2(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        # Check if the current password is correct
        if not request.user.check_password(current_password):
            messages.error(request, "Current password is incorrect.")
            return redirect('reset_password2')

        # Check if the new password and confirmation match
        if new_password != confirm_password:
            messages.error(request, "New passwords do not match.")
            return redirect('reset_password2')

        # Password complexity check
        if not is_password_valid(new_password):
            messages.error(request, "Password must be at least 6 characters long and contain at least one uppercase letter, one digit, and one special character.")
            return redirect('reset_password2')

        # Update the password if validations pass
        request.user.set_password(new_password)
        request.user.save()

        # Update the session so the user remains logged in
        update_session_auth_hash(request, request.user)
        messages.success(request, "Your password has been reset successfully.")
        return redirect('reset_password2')  # Replace with the page you want to redirect to
    
    return render(request, 'reset_password2.html')

def is_password_valid(password):
    # Check the password against the complexity requirements
    if (len(password) >= 6 and
        re.search(r'[A-Z]', password) and     # At least one uppercase letter
        re.search(r'\d', password) and        # At least one digit
        re.search(r'[!@#$%^&*(),.?":{}|<>]', password)):  # At least one special character
        return True
    return False

def student_name(request):
    if request.user.is_authenticated:
        # Retrieve the Student instance for the logged-in user
        student = Student.objects.get(user=request.user)
        # Pass the student's first name or full name to the template
        return render(request, 'S_admin.html', {'student': student, 'student_name': student.user.first_name})
    else:
        return redirect('login')
    
def task(request):
    return render(request,'task.html')

@login_required
def assign_task(request):
    if request.method == 'POST':
        task_name = request.POST.get('task_name')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        if task_name and start_date and end_date:
            Task.objects.create(
                task_name=task_name,
                start_date=datetime.strptime(start_date, '%Y-%m-%d'),
                end_date=datetime.strptime(end_date, '%Y-%m-%d'),
                teacher=request.user
            )
            return redirect('T_admin')  # Redirect to a view showing all tasks for the teacher

    return render(request, 'assign_task.html')

def view_task(request):
    tasks = Task.objects.filter(teacher=request.user)  # Filter tasks by the logged-in teacher
    return render(request, 'view_task.html', {'tasks': tasks})

@login_required
def student_view_task(request):
    # Get the student instance for the logged-in user
    student = Student.objects.get(user=request.user)
    
    # Get the teacher assigned to this student
    teacher = student.teacher  # This is the 'CustomUser' instance of the teacher
    
    # Fetch tasks assigned by this teacher
    tasks = Task.objects.filter(teacher=teacher)

    # Check if the student has already submitted each task
    submitted_task_ids = TaskSubmission.objects.filter(student=request.user).values_list('task_id', flat=True)
    
    # Render the task list for the student
    return render(request, 'student_view_task.html', {
        'tasks': tasks,
        'submitted_task_ids': submitted_task_ids  # Pass the list of submitted task IDs to the template
    })

@login_required
def submit_task_page(request, task_id):
    # Fetch the task based on the provided ID
    task = get_object_or_404(Task, id=task_id)
    return render(request, 'submit_task_page.html', {'task': task})

@login_required
def submit_task(request, task_id):
    # Fetch the task object
    task = get_object_or_404(Task, id=task_id)
    
    if request.method == 'POST':
        # Retrieve form data directly from the POST and FILES dictionaries
        description = request.POST.get('description')
        task_file = request.FILES.get('task_file')
        
        # Create a new TaskSubmission entry linked to the task and the current user (student)
        TaskSubmission.objects.create(
            task=task,
            student=request.user,  # Current logged-in user is the student
            file=task_file,
            description=description
        )
        
        # Redirect to a success page or task list page
        return redirect('student_view_task')
    else:
        # Redirect to an error page or back to the task submission page if the request is not POST
        return redirect('S_admin')
    
@login_required
def view_submitted_tasks(request):
    # Fetch all tasks assigned to the current teacher (logged-in user)
    tasks = Task.objects.filter(teacher=request.user)
    
    # Prepare a list of submissions for each task
    task_data = []
    
    for task in tasks:
        submissions = TaskSubmission.objects.filter(task=task)
        task_info = {
            'task_name': task.task_name,
            'submissions': submissions
        }
        task_data.append(task_info)
    
    return render(request, 'view_submitted_tasks.html', {'task_data': task_data})

@login_required
def my_attendance(request):
    teacher = request.user  # Get the logged-in teacher (CustomUser instance)
    attendance_records = Teacherattendence.objects.filter(teacher_name=teacher).order_by('-Date')
    return render(request, 'my_attendance.html', {'attendance_records': attendance_records})

def view_sattendance(request):
    records = None
    student_name = request.GET.get('student_name')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    # Check if all required fields are provided
    if student_name and start_date and end_date:
        # Filter student attendance records
        student = CustomUser.objects.get(id=student_name)  # Get the student object based on the selected student id
        records = Studentattendence.objects.filter(
            student_name=student,
            Date__range=[start_date, end_date]
        )
    
    # Get list of students for the dropdown
    students = CustomUser.objects.filter(user_type='3')  # Get all students (assuming usertype=2 for students)

    return render(request, 'view_sattendance.html', {
        'students': students,
        'records': records,
        'selected_student': student_name,
        'start_date': start_date,
        'end_date': end_date
    })
    


# Create your views here.
