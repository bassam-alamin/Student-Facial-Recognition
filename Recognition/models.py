from django.db import models
from django.contrib.auth.models import (
    AbstractUser
)


class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_lecturer = models.BooleanField(default=False)


class Departments(models.Model):
    department_name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.department_name


class Students(models.Model):
    student_name = models.OneToOneField(User, limit_choices_to={'is_student': True}, on_delete=models.CASCADE)
    reg_no = models.CharField(max_length=15)
    department = models.ForeignKey(Departments, on_delete=models.CASCADE)
    id_no = models.CharField(max_length=8)
    phone_no = models.CharField(max_length=10)
    year = models.IntegerField(default=1)
    semester = models.IntegerField(default=1)
    is_paid = models.BooleanField(default=False)
    image = models.FileField(default=None)
    image_features = models.CharField(max_length=255, default=None)

    def __str__(self):
        return self.student_name.first_name


class Lecturer(models.Model):
    lecturer_name = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'is_lecturer': True},
                                         related_name="lecturers")
    department = models.ForeignKey(Departments, on_delete=models.CASCADE)
    phone_no = models.CharField(max_length=10)
    id_no = models.CharField(max_length=8)

    def __str__(self):
        return self.lecturer_name.first_name


class Units(models.Model):
    unit_title = models.CharField(max_length=50)
    unit_code = models.CharField(max_length=30, unique=True)
    unit_lecturer = models.ForeignKey(Lecturer, on_delete=models.CASCADE, related_name='unit_lecturer')
    year = models.IntegerField()
    semester = models.IntegerField()

    def __str__(self):
        return self.unit_code


class Bookings(models.Model):
    student = models.ForeignKey(Students, on_delete=models.CASCADE, related_name="student_bookings")
    unit_booked = models.ForeignKey(Units, on_delete=models.CASCADE)
    is_attended = models.BooleanField()

    def __str__(self):
        return self.unit_booked
