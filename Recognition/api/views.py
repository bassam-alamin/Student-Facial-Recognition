import base64

import numpy as np
from django.http import HttpResponse, Http404, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
import json

from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from rest_framework import generics, status
from rest_framework.views import APIView

from .serializers import *
from rest_framework.permissions import AllowAny
from Recognition.views import *


# part to authenticate ony lecturers and return other details

class UserApiView(APIView):
    lookup_field = "staff_no"
    serializer_class = LecturerSerializer
    permission_classes = [AllowAny, ]

    def get(self, request, *args, **kwargs):
        staff_no = self.kwargs.get("staff_no")
        lecturer = get_object_or_404(Lecturer, staff_no=staff_no)
        context = []
        if lecturer:
            context.append({
                "id": lecturer.id,
                "first_name": lecturer.lecturer_name.first_name,
                "second_name": lecturer.lecturer_name.last_name,
                "username":lecturer.lecturer_name.username,
                "department": lecturer.lecturer_name.department.department_name
            })

        return Response({
                "id": lecturer.id,
                "first_name": lecturer.lecturer_name.first_name,
                "second_name": lecturer.lecturer_name.last_name,
                "username":lecturer.lecturer_name.username,
                "department": lecturer.lecturer_name.department.department_name
            })


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


class StudentRecognizerView(APIView):
    lookup_field = "imagestring"
    serializer_class = StudentSerializer
    permission_classes = [AllowAny, ]

    def get_object(self, pk):
        try:
            return Students.objects.get(pk=pk)
        except Students.DoesNotExist:
            raise Http404

    def get(self, request, *args, **kwargs):
        imb64 = self.kwargs.get(self.lookup_field)
        im_bytes = base64.b64decode(imb64)
        im_arr = np.frombuffer(im_bytes, dtype=np.uint8)  # im_arr is one-dim Numpy array
        unknown_person = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)
        print("===================================================")
        print(type(unknown_person))
        enc1 = whirldata_face_encodings(unknown_person)
        students = Students.objects.all()
        distances = {}
        for i in students:
            enc2 = i.image_features
            distance = return_euclidean_distance(enc1, enc2)
            print(distance)
            if distance < 0.5:
                distances.update({i.id: distance})

        all = {}
        context = {
            'students': all,
        }
        if len(distances) > 0:
            for k, v in enumerate(distances):
                student = Students.objects.get(pk=v)
                all.update({student.student_name.username: student.image.url})
                print(distances)
                snippet = self.get_object(v)
                serializer = StudentSerializer(snippet)
                return Response(serializer.data)


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


# Confirm if the found student has Booked the exam session and update his booking as attended

class BookingExistance(APIView):
    serializer_class = BookingSerializer
    permission_classes = [AllowAny, ]

    def get(self, request, *args, **kwargs):
        query1 = self.request.GET.get('student_id')
        query2 = self.request.GET.get('session_id')

        # booking = Bookings.objects.get(student=query1,unit_booked=query2)
        booking = get_object_or_404(Bookings, student=query1, exam_session=query2)

        serializerbooking = BookingSerializer(booking)

        return Response(serializerbooking.data)

    def patch(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')

        booking_object = Bookings.objects.get(pk=pk)

        booking_object.is_attended = True
        booking_object.save()
        serializer = BookingSerializer(booking_object)
        return Response(serializer.data)


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


# ==================================Exam Session serialzier ============================

class ExamSessionView(APIView):
    serializer_class = ExamsessionSerializer
    permission_classes = [AllowAny, ]

    def get(self, request, *args, **kwargs):
        lecturer_pk = self.kwargs.get("pk")
        e_session = ExamSession.objects.filter(lecturer=lecturer_pk)
        sessions = []

        for s in e_session:
            sessions.append({"id": s.id,
                             "unit": s.unit.unit_code,
                             "department": s.department.department_name
                             })
        return Response(sessions)


# =================================Reports section======================================
class CurrentUnitReport(APIView):
    serializer_class = BookingSerializer
    permission_classes = [AllowAny, ]

    def get(self, request, *args, **kwargs):
        session_id = self.kwargs.get("pk")
        bookings = Bookings.objects.filter(exam_session=session_id, is_attended=1)

        context = []
        for b in bookings:
            print(b.student.student_name.first_name)
            context.append({"first_name": b.student.student_name.first_name,
                            "second_name": b.student.student_name.last_name,
                            "reg_no": b.student.reg_no})

        print(type(bookings))

        return Response(context)
