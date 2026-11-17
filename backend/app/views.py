from time import timezone

from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Employees, Departments, Attendance
from django.contrib.auth.hashers import check_password
from django.utils import timezone
from django.contrib.auth import logout as auth_logout


def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        password = request.POST.get('password')

        Employees.objects.create(
            emp_name = username,
            emp_phone = phone,
            emp_email = email,
            password = password,
        )

        if Employees.approval_status == 'Pending':
            return render(request, 'pending.html')
        elif Employees.approval_status == 'Rejected':
            return render(request, 'rejected.html')
        elif Employees.approval_status == 'Approved':    
            return redirect('login')

    return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            employee = Employees.objects.get(emp_email=email)

            if not check_password(password, employee.password):
                raise Employees.DoesNotExist
            
            if employee.approval_status == 'Pending':
                return render(request, 'pending.html')
            elif employee.approval_status == 'Rejected':
                return render(request, 'rejected.html')
            elif employee.approval_status == 'Approved':

                    Attendance.objects.get_or_create(
                        emp_id=employee,
                        date=timezone.localdate(),
                        defaults={
                            'check_in': timezone.localtime().time(),
                            'status': 'Present'}
                    )

                    if employee.role == 'Employee':
                        return redirect('employee_dashboard')

                    elif employee.role == 'Manager':
                        return redirect('manager_dashboard')

                    elif employee.role == 'Admin':
                        return redirect('admin_dashboard')


        except Employees.DoesNotExist:
            error_message = "Invalid email or password."
            return render(request, 'login.html', {'error_message': error_message})

    return render(request, 'login.html')

@login_required
def employee_dashboard(request):
    username = request.user.emp_name
    return render(request, 'employee_dashboard.html', {'username': username})

@login_required
def manager_dashboard(request):
    username = request.user.emp_name
    return render(request, 'manager_dashboard.html', {'username': username})

@login_required
def admin_dashboard(request):
    username = request.user.emp_name
    return render(request, 'admin_dashboard.html', {'username': username})

@login_required
def attendance(request):
    if request.method == 'POST':
        emp_id = request.POST.get('emp_id')
        date = request.POST.get('date')
        status = request.POST.get('status')

        Attendance.objects.create(
            emp_id=emp_id,
            date=date,
            status=status
        )

    return render(request, 'attendance.html')


@login_required
def logout(request):

    employee = Employees.objects.get(emp_email=request.user.email)

    attendance = Attendance.objects.get(
        emp_id=employee,
        date=timezone.localdate()
    )

    if attendance.check_out is None:
        attendance.check_out = timezone.localtime().time()
        attendance.save()

    auth_logout(request)

    return redirect('login')

@login_required
def employee_list(request):
    employees = Employees.objects.filter(role='Employee')
    return render(request, 'employee_list.html', {'employees': employees})

@login_required
def manager_list(request):
    managers = Employees.objects.filter(role='Manager')
    return render(request, 'manager_list.html', {'managers': managers})


@login_required
def department_list(request):
    departments = Departments.objects.all()
    return render(request, 'department_list.html', {'departments': departments})


def employee_approvals(request):
    employees = Employees.objects.filter(approval_status='Pending')

    return render(
        request,
        'employee_approvals.html',
        {'employees': employees}
    )


def approve_employee(request, emp_id):
    if request.method == 'POST':
        employee = get_object_or_404(Employees, emp_id=emp_id)
        employee.approval_status = 'Approved'
        employee.save()

    return redirect('employee_approvals')

def role_employee(request, emp_id):
    if request.method == 'POST':
        employee = get_object_or_404(Employees, emp_id=emp_id)
        employee.role = 'Employee'
        employee.save()

def role_manager(request, emp_id):
    if request.method == 'POST':
        employee = get_object_or_404(Employees, emp_id=emp_id)
        employee.role = 'Manager'
        employee.save()

def reject_employee(request, emp_id):
    if request.method == 'POST':
        employee = get_object_or_404(Employees, emp_id=emp_id)
        employee.approval_status = 'Rejected'
        employee.save()

    return redirect('employee_approvals')
    