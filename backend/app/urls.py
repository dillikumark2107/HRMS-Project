# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.home, name='home'),

#     path('register/', views.register, name='register'),
#     path('login/', views.login, name='login'),
#     path('logout/', views.logout, name='logout'),

#     path('employee-dashboard/', views.employee_dashboard, name='employee_dashboard'),
#     path('manager-dashboard/', views.manager_dashboard, name='manager_dashboard'),
#     path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),

#     path('attendance/', views.attendance, name='attendance'),

#     path('employee-list/', views.employee_list, name='employee_list'),
#     path('manager-list/', views.manager_list, name='manager_list'),
#     path('department-list/', views.department_list, name='department_list'),

#     path('employee-approvals/', views.employee_approvals, name='employee_approvals'),
#     path('approve-employee/<int:emp_id>/', views.approve_employee, name='approve_employee'),
#     path('reject-employee/<int:emp_id>/', views.reject_employee, name='reject_employee'),

#     path('role-employee/<int:emp_id>/', views.role_employee, name='role_employee'),
#     path('role-manager/<int:emp_id>/', views.role_manager, name='role_manager'),

#     path('edit-employee/<int:emp_id>/', views.edit_employee, name='edit_employee'),
#     path('edit-manager/<int:emp_id>/', views.edit_manager, name='edit_manager'),

#     path('delete-employee/<int:emp_id>/', views.delete_employee, name='delete_employee'),
# ]


from django.urls import path
from . import views

urlpatterns = [
    path('csrf/', views.csrf_token, name='csrf_token'),

    path('home/', views.home, name='home'),

    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),

    path('employee-dashboard/', views.employee_dashboard, name='employee_dashboard'),
    path('manager-dashboard/', views.manager_dashboard, name='manager_dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),

    path('attendance/', views.attendance, name='attendance'),

    path('employees/', views.employee_list, name='employee_list'),
    path('managers/', views.manager_list, name='manager_list'),
    path('departments/', views.department_list, name='department_list'),

    path('employee-approvals/', views.employee_approvals, name='employee_approvals'),
    path('approve-employee/<int:emp_id>/', views.approve_employee, name='approve_employee'),
    path('reject-employee/<int:emp_id>/', views.reject_employee, name='reject_employee'),

    path('role-employee/<int:emp_id>/', views.role_employee, name='role_employee'),
    path('role-manager/<int:emp_id>/', views.role_manager, name='role_manager'),

    path('edit-employee/<int:emp_id>/', views.edit_employee, name='edit_employee'),
    path('edit-manager/<int:emp_id>/', views.edit_manager, name='edit_manager'),

    path('delete-employee/<int:emp_id>/', views.delete_employee, name='delete_employee'),
]