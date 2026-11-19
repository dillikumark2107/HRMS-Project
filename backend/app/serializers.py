from rest_framework import serializers
from .models import Employees, Departments, Attendance
from django.contrib.auth.hashers import make_password

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departments
        fields = ['dept_id', 'dept_name', 'tot_emp']


class EmployeeSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(
        source='dept_id.dept_name',
        read_only=True
    )

    class Meta:
        model = Employees
        fields = [
            'emp_id',
            'emp_name',
            'emp_phone',
            'emp_email',
            'dept_id',
            'department_name',
            'role',
            'approval_status'
        ]


class AttendanceSerializer(serializers.ModelSerializer):
    emp_name = serializers.CharField(
        source='emp_id.emp_name',
        read_only=True
    )

    class Meta:
        model = Attendance
        fields = [
            'id',
            'emp_id',
            'emp_name',
            'cur_date',
            'check_in',
            'check_out',
            'status'
        ]

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    phone = serializers.CharField(max_length=15)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    dept_id = serializers.PrimaryKeyRelatedField(
        queryset=Departments.objects.all()
    )

    def validate_email(self, value):
        if Employees.objects.filter(emp_email=value).exists():
            raise serializers.ValidationError("Email already registered")
        return value

    def create(self, validated_data):
        return Employees.objects.create(
            emp_name=validated_data['username'],
            emp_phone=validated_data['phone'],
            emp_email=validated_data['email'],
            password=make_password(validated_data['password']),
            dept_id=validated_data['dept_id'],
            approval_status='Pending'
        )