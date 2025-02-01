from django.urls import path,include
from .import views

urlpatterns = [
    path('',views.home,name="home"),
    path('log',views.log,name="log"),
    path('teacher',views.teacher,name="teacher"),
    path('student',views.student,name="student"),
    path('login1',views.login1,name="login1"),
    path('admin',views.admin,name="admin"),
    path('add_course',views.add_course,name="add_course"),
    path('add_coursedb',views.add_coursedb,name="add_coursedb"),
    path('add_teacher',views.add_teacher,name="add_teacher"),
    path('add_student',views.add_student,name="add_student"),
    path('approvedisapprove', views.approvedisapprove, name="approvedisapprove"),

    path('approve/<int:k>', views.approve, name="approve"),
    path('disapprove/<int:k>', views.disapprove, name="disapprove"),
    path('managecourse',views.managecourse,name="managecourse"),
    path('tcr_table',views.tcr_table,name="tcr_table"),
    path('dlt/<int:lk>',views.dlt,name="dlt"),
    path('std_table',views.std_table,name="std_table"),
    path('sdlt/<int:sk>',views.sdlt,name="sdlt"),
    path('t_attend',views.t_attend,name="t_attend"),
    path('t_attenddb',views.t_attenddb,name="t_attenddb"),
    path('vta',views.vta,name="vta"),
    path('vtadb',views.vtadb,name="vtadb"),
    path('sta',views.sta,name="sta"),
    path('logout',views.logout,name="logout"),
    path('assign',views.assign,name="assign"),
    path('assign_teacher/<int:student_id>/<int:teacher_id>/',views.assign_teacher,name="assign_teacher"),
    path('admin_view',views.admin_view,name="admin_view"),
    path('T_admin',views.T_admin,name="T_admin"),
    path('mark_attendance/', views.mark_attendance, name="mark_attendance"),
    path('save_attendance/', views.save_attendance, name="save_attendance"),
    path('view_attendance/', views.view_attendance, name="view_attendance"),
    path('view_syllabus/',views.view_syllabus, name='view_syllabus'),
    path('view_students/',views.view_students, name='view_students'),
    path('name_view',views.name_view, name='name_view'),
    path('reset_password/',views.reset_password, name='reset_password'),
    path('S_admin',views.S_admin,name="S_admin"),
    path('student/attendance/', views.student_view_own_attendance, name='student_view_own_attendance'),
    path('syllabus/', views.syllabus, name='syllabus'),
    path('student/profile/', views.student_profile, name='student_profile'),
    path('reset_password2/',views.reset_password2, name='reset_password2'),
    path('student_name', views.student_name, name='student_name'),
    path('task',views.task,name="task"),
    path('assign_task/', views.assign_task, name='assign_task'),
    path('view_task/', views.view_task, name='view_task'),
    path('student_view_task/', views.student_view_task, name='student_view_task'),
    path('submit_task_page/<int:task_id>/', views.submit_task_page, name='submit_task_page'),
    path('submit_task/<int:task_id>/', views.submit_task, name='submit_task'),
    path('teacher/submitted_tasks/', views.view_submitted_tasks, name='view_submitted_tasks'),
    path('my-attendance/', views.my_attendance, name='my_attendance'),
    path('view_sattendance/', views.view_sattendance, name='view_sattendance'),
   
    
    



]