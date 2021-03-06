import os
from jsonfield import JSONField
from django.db import models
from django.contrib.auth.models import (
    AbstractUser
)

import cv2
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class Departments(models.Model):
    department_name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.department_name

    def get_queryset(self):
        return Departments.objects.all()

class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_lecturer = models.BooleanField(default=False)
    phone_no = models.CharField(max_length=10,null=True,default=None)
    id_no = models.CharField(max_length=8,null=True,default=None)
    department = models.ForeignKey(Departments, on_delete=models.CASCADE,null=True,default=None)

    def __str__(self):
        return self.username

@receiver(post_save,sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender,instance=None,created=False,**kwargs):
    if created:
        Token.objects.create(user=instance)



class Students(models.Model):
    student_name = models.OneToOneField(User, limit_choices_to={'is_student': True}, on_delete=models.CASCADE)
    reg_no = models.CharField(max_length=15)
    image = models.FileField(default=None)
    image_features = JSONField(default=None,null=True)


    # def save(self, force_insert=False, force_update=False, using=None,
    #          update_fields=None):
    #
    #     print(self.image)
    #
    #     print(self.image.url)
    #     url = self.image.url
    #     print(os.path.join(settings.BASE_DIR,"media/rihanna.jpg"))
    #     image = cv2.imread(self.image.path)
    #     print(type(image))
    #
    #     return self.image

    def __str__(self):
        return self.student_name.username


class Lecturer(models.Model):
    lecturer_name = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'is_lecturer': True},
                                         related_name="lecturers")
    staff_no = models.CharField(max_length=10)
    def __str__(self):
        return self.lecturer_name.first_name


class Units(models.Model):
    unit_title = models.CharField(max_length=50)
    unit_code = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.unit_code

class ExamSession(models.Model):
    unit = models.ForeignKey(Units,on_delete=models.SET_NULL,null=True)
    lecturer = models.ForeignKey(Lecturer,on_delete=models.SET_NULL,null=True)
    department = models.ForeignKey(Departments,on_delete=models.SET_NULL,null=True)

    def __str__(self):
        return self.unit.unit_code


class Bookings(models.Model):
    student = models.ForeignKey(Students, on_delete=models.CASCADE, related_name="student_bookings")
    unit_booked = models.ForeignKey(Units, on_delete=models.CASCADE)
    is_attended = models.BooleanField(default=False)
    exam_session = models.ForeignKey(ExamSession,on_delete=models.SET_NULL,null=True)

    def __str__(self):
        return str(self.unit_booked)

class Recognizer(models.Model):
    pic = models.FileField()

    def __str__(self):
        return str(self.pk)