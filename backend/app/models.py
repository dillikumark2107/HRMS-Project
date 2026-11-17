
from django.db import models
from django.utils import timezone


class Departments(models.Model):
    dept_id = models.IntegerField(primary_key=True)
    dept_name = models.CharField(max_length=50)
    tot_emp = models.IntegerField(default=0)

    APPROVAL_CHOICES = [
    ('Pending', 'Pending'),
    ('Approved', 'Approved'),
    ('Rejected', 'Rejected'),
    ]

    approval_status = models.CharField(
    max_length=10,
    choices=APPROVAL_CHOICES,
    default='Pending'
    )

    def __str__(self):
        return self.dept_name


class Employees(models.Model):

    ROLE_CHOICES = [
        ('Employee', 'Employee'),
        ('Manager', 'Manager'),
        ('Admin', 'Admin'),
    ]

    emp_id = models.IntegerField(primary_key=True)
    emp_name = models.CharField(max_length=100)
    emp_phone = models.CharField(max_length=15)
    emp_email = models.EmailField()
    password = models.CharField(
            max_length=128,
            null=True,
            blank=True
        )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='Employee',
        blank=True
    )

    dept_id = models.ForeignKey(
        Departments,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    mgr_id = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='team_members'
    )

    hire_date = models.DateField(default=timezone.localdate)

    salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00
    )

    def __str__(self):
        return self.emp_name


class Attendance(models.Model):

    STATUS_CHOICES = [
        ('Present', 'Present'),
        ('Absent', 'Absent'),
    ]

    emp_id = models.ForeignKey(
        Employees,
        on_delete=models.CASCADE,
        related_name='attendance_records'
    )

    cur_date = models.DateField(default=timezone.localdate)

    check_in = models.TimeField(null=True, blank=True)
    check_out = models.TimeField(null=True, blank=True)

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='Absent'
    )

    def __str__(self):
        return f"{self.emp_id.emp_name} - {self.cur_date} - {self.status}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['emp_id', 'cur_date'],
                name='unique_employee_attendance_per_day'
            )
        ]
