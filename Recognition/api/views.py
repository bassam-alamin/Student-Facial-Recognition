import base64


import numpy as np
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from rest_framework import generics
from .serializers import *
from rest_framework.permissions import AllowAny
from Recognition.views import *


class UserApiView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = "username"
    serializer_class = UserSerializer
    permission_classes = [AllowAny, ]

    def get_queryset(self):
        return User.objects.all()

    def perform_create(self, serializer):
        instance = serializer.save()
        instance.set_password(instance.password)
        instance.save()


class UserRudApiView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = "pk"
    serializer_class = UserSerializer
    permission_classes = [AllowAny, ]

    def get_queryset(self):
        return User.objects.all()


class StudentApiView(generics.ListAPIView):
    lookup_field = "pk"
    serializer_class = StudentSerializer
    permission_classes = [AllowAny, ]

    def get_queryset(self):
        return Students.objects.all()

class StudentRecognizerView(generics.ListAPIView):
    lookup_field = "imagestring"
    serializer_class = StudentSerializer
    permission_classes = [AllowAny, ]

    def get_queryset(self):
        imb64 = self.kwargs.get(self.lookup_field)
        im_bytes = base64.b64decode(imb64)
        im_arr = np.frombuffer(im_bytes, dtype=np.uint8)  # im_arr is one-dim Numpy array
        img = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)
        print("===================================================")
        print(type(img))


        return Students.objects.all()


class StudentRudView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = "pk"
    serializer_class = StudentSerializer
    permission_classes = [AllowAny, ]

    def get_queryset(self):
        return Students.objects.all()


class LecturerApiView(generics.ListAPIView):
    lookup_field = "pk"
    serializer_class = LecturerSerializer
    permission_classes = [AllowAny, ]

    def get_queryset(self):
        return Lecturer.objects.all()


class LecturerRudView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = "pk"
    serializer_class = LecturerSerializer
    permission_classes = [AllowAny, ]

    def get_queryset(self):
        return Lecturer.objects.all()


class UnitApiView(generics.ListAPIView):
    lookup_field = "pk"
    serializer_class = UnitSerializer
    permission_classes = [AllowAny, ]

    def get_queryset(self):
        return Units.objects.all()


class UnitRudView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = "pk"
    serializer_class = UnitSerializer
    permission_classes = [AllowAny, ]

    def get_queryset(self):
        return Units.objects.all()


class BookingApiView(generics.ListAPIView):
    lookup_field = "pk"
    serializer_class = BookingSerializer
    permission_classes = [AllowAny, ]

    def get_queryset(self):
        return Bookings.objects.all()


class BookingRudView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = "pk"
    serializer_class = BookingSerializer
    permission_classes = [AllowAny, ]

    def get_queryset(self):
        return Bookings.objects.all()


class DepartmentApiView(generics.ListCreateAPIView):
    lookup_field = "pk"
    serializer_class = DepartmentSerializer
    permission_classes = [AllowAny, ]

    def get_queryset(self):
        return Departments.objects.all()


class DepartmentRudView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = "pk"
    serializer_class = DepartmentSerializer
    permission_classes = [AllowAny, ]

    def get_queryset(self):
        return Departments.objects.all()


