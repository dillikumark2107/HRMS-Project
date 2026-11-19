
# from django.shortcuts import render,redirect, get_object_or_404
# from .models import Employees, Departments, Attendance
# from django.contrib.auth.hashers import check_password
# from django.utils import timezone
# from django.contrib.auth.hashers import make_password
# from django.db.models import F


# def home(request):
#     return render(request, 'home.html')


# def register(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         phone = request.POST.get('phone')
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         dept_id = request.POST.get('dept_id')

#         department = get_object_or_404(
#             Departments,
#             dept_id=dept_id
#         )

#         Employees.objects.create(
#             emp_name=username,
#             emp_phone=phone,
#             emp_email=email,
#             password=make_password(password),
#             dept_id=department,
#             approval_status='Pending'
#         )

#         return redirect('login')

#     departments = Departments.objects.all()

#     return render(request, 'register.html', {
#         'departments': departments
#     })

# def login(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         password = request.POST.get('password')

#         try:
#             employee = Employees.objects.get(emp_email=email)

#             if not check_password(password, employee.password):
#                 raise Employees.DoesNotExist
            
#             if employee.approval_status == 'Pending':
#                 return render(request, 'pending.html')
#             elif employee.approval_status == 'Rejected':
#                 return render(request, 'rejected.html')
#             elif employee.approval_status == 'Approved':
#                     request.session['emp_id'] = employee.emp_id

#                     Attendance.objects.get_or_create(
#                         emp_id=employee,
#                         cur_date=timezone.localdate(),
#                         defaults={
#                             'check_in': timezone.localtime().time(),
#                             'status': 'Present'}
#                     )

#                     if employee.role == 'Employee':
#                         return redirect('employee_dashboard')

#                     elif employee.role == 'Manager':
#                         return redirect('manager_dashboard')

#                     elif employee.role == 'Admin':
#                         return redirect('admin_dashboard')


#         except Employees.DoesNotExist:
#             error_message = "Invalid email or password."
#             return render(request, 'login.html', {'error_message': error_message})

#     return render(request, 'login.html')


# def employee_dashboard(request):
#     emp_id = request.session.get('emp_id')

#     if not emp_id:
#         return redirect('login')

#     employee = get_object_or_404(Employees, emp_id=emp_id)

#     if employee.role != 'Employee':
#             return redirect('login')

#     return render(request, 'employee_dashboard.html', {
#         'employee': employee
#     })


# def manager_dashboard(request):
#     emp_id = request.session.get('emp_id')

#     if not emp_id:
#         return redirect('login')

#     manager = get_object_or_404(Employees, emp_id=emp_id)

#     if manager.role != 'Manager':
#         return redirect('login')

#     return render(request, 'manager_dashboard.html', {'manager': manager})


# def admin_dashboard(request):
#     emp_id = request.session.get('emp_id')

#     if not emp_id:
#         return redirect('login')

#     admin = get_object_or_404(Employees, emp_id=emp_id)

#     if admin.role != 'Admin':
#         return redirect('login')

#     return render(request, 'admin_dashboard.html', {'admin': admin})


# def attendance(request):
#     attendances = Attendance.objects.all()

#     return render(request, 'attendance.html', {'attendances': attendances})



# def logout(request):
#     emp_id = request.session.get('emp_id')

#     if emp_id:
#         employee = get_object_or_404(Employees, emp_id=emp_id)

#         attendance = Attendance.objects.filter(
#             emp_id=employee,
#             cur_date=timezone.localdate()
#         ).first()

#         if attendance and attendance.check_out is None:
#             attendance.check_out = timezone.localtime().time()
#             attendance.save()

#     request.session.flush()

#     return redirect('login')


# def employee_list(request):
#     employees = Employees.objects.filter(role='Employee')
#     return render(request, 'employee_list.html', {'employees': employees})


# def manager_list(request):
#     managers = Employees.objects.filter(role='Manager')
#     return render(request, 'manager_list.html', {'managers': managers})



# def department_list(request):
#     departments = Departments.objects.all()
#     return render(request, 'department_list.html', {'departments': departments})


# def employee_approvals(request):
#     employees = Employees.objects.filter(approval_status='Pending')
#     return render(request, 'employee_approvals.html', {'employees': employees})




# def approve_employee(request, emp_id):
#     if request.method == 'POST':
#         employee = get_object_or_404(Employees, emp_id=emp_id)

#         if employee.approval_status == 'Pending':
#             employee.approval_status = 'Approved'
#             employee.save()

#             if employee.dept_id:
#                 Departments.objects.filter(
#                     dept_id=employee.dept_id.dept_id
#                 ).update(tot_emp=F('tot_emp') + 1)

#     return redirect('employee_approvals')


# def role_employee(request, emp_id):
#     if request.method == 'POST':
#         employee = get_object_or_404(Employees, emp_id=emp_id)
#         employee.role = 'Employee'
#         employee.save()

#     return redirect('employee_approvals')


# def role_manager(request, emp_id):
#     if request.method == 'POST':
#         employee = get_object_or_404(Employees, emp_id=emp_id)
#         employee.role = 'Manager'
#         employee.save()

#     return redirect('employee_approvals')


# def reject_employee(request, emp_id):
#     if request.method == 'POST':
#         employee = get_object_or_404(Employees, emp_id=emp_id)
#         employee.approval_status = 'Rejected'
#         employee.save()

#     return redirect('employee_approvals')


# def edit_employee(request, emp_id):
#     employee = get_object_or_404(Employees, emp_id=emp_id)

#     if request.method == 'POST':
#         employee.emp_name = request.POST.get('emp_name')
#         employee.emp_phone = request.POST.get('emp_phone')
#         employee.emp_email = request.POST.get('emp_email')

#         dept_id = request.POST.get('dept_id')
#         department = get_object_or_404(Departments, dept_id=dept_id)
#         employee.dept_id = department

#         employee.save()

#         return redirect('employee_dashboard')

#     departments = Departments.objects.all()

#     return render(request, 'edit_employee.html', {
#         'employee': employee,
#         'departments': departments
#     })

# def edit_manager(request, emp_id):
#     manager = get_object_or_404(Employees, emp_id=emp_id)

#     if request.method == 'POST':
#         manager.emp_name = request.POST.get('emp_name')
#         manager.emp_phone = request.POST.get('emp_phone')
#         manager.emp_email = request.POST.get('emp_email')

#         dept_id = request.POST.get('dept_id')
#         department = get_object_or_404(Departments, dept_id=dept_id)
#         manager.dept_id = department

#         manager.save()

#         return redirect('manager_dashboard')

#     departments = Departments.objects.all()

#     return render(request, 'edit_manager.html', {
#         'manager': manager,
#         'departments': departments
#     })

# def delete_employee(request, emp_id):
#     if request.method == 'POST':
#         employee = get_object_or_404(Employees, emp_id=emp_id)
#         employee.delete()

#     return redirect('employee_list')



from django.shortcuts import get_object_or_404
from django.db import transaction
from django.db.models import F
from django.utils import timezone
from django.middleware.csrf import get_token

from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes
)
from rest_framework.authentication import BaseAuthentication, SessionAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth.hashers import check_password

from .models import Employees, Departments, Attendance
from .serializers import (
    RegisterSerializer,
    EmployeeSerializer,
    DepartmentSerializer,
    AttendanceSerializer
)


# --------------------------------
# Custom session authentication
# --------------------------------

class EmployeeSessionAuthentication(BaseAuthentication):

    def authenticate(self, request):

        # Enforce CSRF for unsafe requests, including login
        SessionAuthentication().enforce_csrf(request)

        emp_id = request.session.get('emp_id')

        if not emp_id:
            return None

        employee = Employees.objects.filter(emp_id=emp_id).first()

        if not employee:
            return None

        return (employee, None)


# Common API decorator
def hrms_api(methods):

    def decorator(view):

        view = authentication_classes(
            [EmployeeSessionAuthentication]
        )(view)

        view = permission_classes([AllowAny])(view)

        return api_view(methods)(view)

    return decorator


# --------------------------------
# Common helper functions
# --------------------------------

def get_current_employee(request):

    emp_id = request.session.get('emp_id')

    if not emp_id:
        return None

    return Employees.objects.filter(emp_id=emp_id).first()


def check_role(request, allowed_roles):

    employee = get_current_employee(request)

    if not employee:
        return None, Response(
            {'error': 'Please login first'},
            status=status.HTTP_401_UNAUTHORIZED
        )

    if employee.role not in allowed_roles:
        return None, Response(
            {'error': 'Permission denied'},
            status=status.HTTP_403_FORBIDDEN
        )

    return employee, None


# --------------------------------
# CSRF API
# --------------------------------

@hrms_api(['GET'])
def csrf_token(request):

    get_token(request)

    return Response({
        'message': 'CSRF token generated'
    })


# --------------------------------
# Home API
# --------------------------------

@hrms_api(['GET'])
def home(request):

    return Response({
        'message': 'Welcome to HRMS'
    })


# --------------------------------
# Register API
# --------------------------------

@hrms_api(['POST'])
def register(request):

    serializer = RegisterSerializer(data=request.data)

    if serializer.is_valid():
        employee = serializer.save()

        return Response({
            'message': 'Registration successful. Waiting for approval.',
            'emp_id': employee.emp_id
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# --------------------------------
# Login API
# --------------------------------

@hrms_api(['POST'])
def login(request):

    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response(
            {'error': 'Email and password are required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    employee = Employees.objects.filter(emp_email=email).first()

    if not employee or not check_password(
        password, employee.password or ''
    ):
        return Response(
            {'error': 'Invalid email or password'},
            status=status.HTTP_400_BAD_REQUEST
        )

    if employee.approval_status == 'Pending':
        return Response({
            'message': 'Your account is waiting for approval'
        })

    if employee.approval_status == 'Rejected':
        return Response(
            {'message': 'Your registration was rejected'},
            status=status.HTTP_403_FORBIDDEN
        )

    # Start employee session
    request.session.cycle_key()
    request.session['emp_id'] = employee.emp_id

    # Automatic attendance check-in
    Attendance.objects.get_or_create(
        emp_id=employee,
        cur_date=timezone.localdate(),
        defaults={
            'check_in': timezone.localtime().time(),
            'status': 'Present'
        }
    )

    return Response({
        'message': 'Login successful',
        'employee': EmployeeSerializer(employee).data,
        'role': employee.role
    })


# --------------------------------
# Employee Dashboard
# --------------------------------

@hrms_api(['GET'])
def employee_dashboard(request):

    employee, error = check_role(request, ['Employee'])

    if error:
        return error

    serializer = EmployeeSerializer(employee)

    return Response(serializer.data)


# --------------------------------
# Manager Dashboard
# --------------------------------

@hrms_api(['GET'])
def manager_dashboard(request):

    manager, error = check_role(request, ['Manager'])

    if error:
        return error

    serializer = EmployeeSerializer(manager)

    return Response(serializer.data)


# --------------------------------
# Admin Dashboard
# --------------------------------

@hrms_api(['GET'])
def admin_dashboard(request):

    admin, error = check_role(request, ['Admin'])

    if error:
        return error

    serializer = EmployeeSerializer(admin)

    return Response(serializer.data)


# --------------------------------
# Attendance API - Admin
# --------------------------------

@hrms_api(['GET'])
def attendance(request):

    admin, error = check_role(request, ['Admin'])

    if error:
        return error

    attendances = Attendance.objects.select_related('emp_id').all()

    serializer = AttendanceSerializer(attendances, many=True)

    return Response(serializer.data)


# --------------------------------
# Logout API
# --------------------------------

@hrms_api(['POST'])
def logout(request):

    employee = get_current_employee(request)

    if not employee:
        return Response(
            {'error': 'Please login first'},
            status=status.HTTP_401_UNAUTHORIZED
        )

    attendance_record = Attendance.objects.filter(
        emp_id=employee,
        cur_date=timezone.localdate()
    ).first()

    if attendance_record and attendance_record.check_out is None:
        attendance_record.check_out = timezone.localtime().time()
        attendance_record.save()

    request.session.flush()

    return Response({
        'message': 'Logout successful'
    })


# --------------------------------
# Employee List - Admin
# --------------------------------

@hrms_api(['GET'])
def employee_list(request):

    admin, error = check_role(request, ['Admin'])

    if error:
        return error

    employees = Employees.objects.filter(role='Employee')

    serializer = EmployeeSerializer(employees, many=True)

    return Response(serializer.data)


# --------------------------------
# Manager List - Admin
# --------------------------------

@hrms_api(['GET'])
def manager_list(request):

    admin, error = check_role(request, ['Admin'])

    if error:
        return error

    managers = Employees.objects.filter(role='Manager')

    serializer = EmployeeSerializer(managers, many=True)

    return Response(serializer.data)


# --------------------------------
# Department List
# --------------------------------

@hrms_api(['GET'])
def department_list(request):

    employee = get_current_employee(request)

    if not employee:
        return Response(
            {'error': 'Please login first'},
            status=status.HTTP_401_UNAUTHORIZED
        )

    departments = Departments.objects.all()

    serializer = DepartmentSerializer(departments, many=True)

    return Response(serializer.data)


# --------------------------------
# Pending Employee Approvals - Admin
# --------------------------------

@hrms_api(['GET'])
def employee_approvals(request):

    admin, error = check_role(request, ['Admin'])

    if error:
        return error

    employees = Employees.objects.filter(
        approval_status='Pending'
    )

    serializer = EmployeeSerializer(employees, many=True)

    return Response(serializer.data)


# --------------------------------
# Approve Employee - Admin
# --------------------------------

@hrms_api(['POST'])
def approve_employee(request, emp_id):

    admin, error = check_role(request, ['Admin'])

    if error:
        return error

    with transaction.atomic():

        employee = get_object_or_404(
            Employees.objects.select_for_update(),
            emp_id=emp_id
        )

        if employee.approval_status == 'Pending':

            employee.approval_status = 'Approved'
            employee.save()

            if employee.dept_id:
                Departments.objects.filter(
                    dept_id=employee.dept_id.dept_id
                ).update(tot_emp=F('tot_emp') + 1)

    return Response({
        'message': 'Employee approved successfully'
    })


# --------------------------------
# Reject Employee - Admin
# --------------------------------

@hrms_api(['POST'])
def reject_employee(request, emp_id):

    admin, error = check_role(request, ['Admin'])

    if error:
        return error

    employee = get_object_or_404(Employees, emp_id=emp_id)

    if employee.approval_status == 'Pending':
        employee.approval_status = 'Rejected'
        employee.save()

    return Response({
        'message': 'Employee rejected'
    })


# --------------------------------
# Change Role to Employee - Admin
# --------------------------------

@hrms_api(['POST'])
def role_employee(request, emp_id):

    admin, error = check_role(request, ['Admin'])

    if error:
        return error

    employee = get_object_or_404(Employees, emp_id=emp_id)

    employee.role = 'Employee'
    employee.save()

    return Response({
        'message': 'Role changed to Employee'
    })


# --------------------------------
# Change Role to Manager - Admin
# --------------------------------

@hrms_api(['POST'])
def role_manager(request, emp_id):

    admin, error = check_role(request, ['Admin'])

    if error:
        return error

    employee = get_object_or_404(Employees, emp_id=emp_id)

    employee.role = 'Manager'
    employee.save()

    return Response({
        'message': 'Role changed to Manager'
    })


# --------------------------------
# Edit Employee
# --------------------------------

@hrms_api(['PUT', 'PATCH'])
def edit_employee(request, emp_id):

    current_employee = get_current_employee(request)

    if not current_employee:
        return Response(
            {'error': 'Please login first'},
            status=status.HTTP_401_UNAUTHORIZED
        )

    if (
        current_employee.role != 'Admin'
        and current_employee.emp_id != emp_id
    ):
        return Response(
            {'error': 'Permission denied'},
            status=status.HTTP_403_FORBIDDEN
        )

    employee = get_object_or_404(Employees, emp_id=emp_id)

    old_department = employee.dept_id

    employee.emp_name = request.data.get(
        'emp_name', employee.emp_name
    )
    employee.emp_phone = request.data.get(
        'emp_phone', employee.emp_phone
    )
    employee.emp_email = request.data.get(
        'emp_email', employee.emp_email
    )

    if 'dept_id' in request.data:
        new_department = get_object_or_404(
            Departments,
            dept_id=request.data['dept_id']
        )

        if (
            employee.approval_status == 'Approved'
            and old_department != new_department
        ):
            with transaction.atomic():

                if old_department:
                    Departments.objects.filter(
                        dept_id=old_department.dept_id,
                        tot_emp__gt=0
                    ).update(tot_emp=F('tot_emp') - 1)

                Departments.objects.filter(
                    dept_id=new_department.dept_id
                ).update(tot_emp=F('tot_emp') + 1)

                employee.dept_id = new_department
                employee.save()
        else:
            employee.dept_id = new_department
            employee.save()
    else:
        employee.save()

    return Response({
        'message': 'Employee details updated',
        'employee': EmployeeSerializer(employee).data
    })


# --------------------------------
# Edit Manager
# --------------------------------

@hrms_api(['PUT', 'PATCH'])
def edit_manager(request, emp_id):

    current_employee = get_current_employee(request)

    if not current_employee:
        return Response(
            {'error': 'Please login first'},
            status=status.HTTP_401_UNAUTHORIZED
        )

    if (
        current_employee.role != 'Admin'
        and current_employee.emp_id != emp_id
    ):
        return Response(
            {'error': 'Permission denied'},
            status=status.HTTP_403_FORBIDDEN
        )

    manager = get_object_or_404(
        Employees,
        emp_id=emp_id,
        role='Manager'
    )

    old_department = manager.dept_id

    manager.emp_name = request.data.get(
        'emp_name', manager.emp_name
    )
    manager.emp_phone = request.data.get(
        'emp_phone', manager.emp_phone
    )
    manager.emp_email = request.data.get(
        'emp_email', manager.emp_email
    )

    if 'dept_id' in request.data:
        new_department = get_object_or_404(
            Departments,
            dept_id=request.data['dept_id']
        )

        if (
            manager.approval_status == 'Approved'
            and old_department != new_department
        ):
            with transaction.atomic():

                if old_department:
                    Departments.objects.filter(
                        dept_id=old_department.dept_id,
                        tot_emp__gt=0
                    ).update(tot_emp=F('tot_emp') - 1)

                Departments.objects.filter(
                    dept_id=new_department.dept_id
                ).update(tot_emp=F('tot_emp') + 1)

                manager.dept_id = new_department
                manager.save()
        else:
            manager.dept_id = new_department
            manager.save()
    else:
        manager.save()

    return Response({
        'message': 'Manager details updated',
        'manager': EmployeeSerializer(manager).data
    })


# --------------------------------
# Delete Employee or Manager - Admin
# --------------------------------

@hrms_api(['DELETE'])
def delete_employee(request, emp_id):

    admin, error = check_role(request, ['Admin'])

    if error:
        return error

    employee = get_object_or_404(Employees, emp_id=emp_id)

    with transaction.atomic():

        if employee.approval_status == 'Approved' and employee.dept_id:

            Departments.objects.filter(
                dept_id=employee.dept_id.dept_id,
                tot_emp__gt=0
            ).update(tot_emp=F('tot_emp') - 1)

        employee.delete()

    return Response({
        'message': 'Employee deleted successfully'
    })
