import math
import urllib.request
from django.contrib import messages

import dlib
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import View, CreateView, ListView, DetailView, UpdateView
from .forms import *
import numpy as np
import cv2
import dlib


# Create your views here.
# =======================================================Functions ====================================
# Models Loaded
face_detector = dlib.get_frontal_face_detector()
pose_predictor_68_point = dlib.shape_predictor(
    '/home/bassam/Desktop/projects/Student-Facial-Recognition/shape_predictor_68_face_landmarks.dat')
face_encoder = dlib.face_recognition_model_v1(
    '/home/bassam/Desktop/projects/Student-Facial-Recognition/dlib_face_recognition_resnet_model_v1.dat')


def whirldata_face_detectors(img, number_of_times_to_upsample=1):
    return face_detector(img, number_of_times_to_upsample)


def whirldata_face_encodings(face_image, num_jitters=1):
    face_locations = whirldata_face_detectors(face_image)
    pose_predictor = pose_predictor_68_point
    predictors = [pose_predictor(face_image, face_location) for face_location in face_locations]
    return \
        [np.array(face_encoder.compute_face_descriptor(face_image, predictor, num_jitters)) for predictor in
         predictors][0]


def return_euclidean_distance(feature_1, feature_2):
    feature_1 = np.array(feature_1)
    feature_2 = np.array(feature_2)
    dist = np.sqrt(np.sum(np.square(feature_1 - feature_2)))
    return dist


def _grab_image(path=None, stream=None, url=None):
    # if the path is not None, then load the image from disk
    if path is not None:
        image = cv2.imread(path)
    # otherwise, the image does not reside on disk
    else:
        # if the URL is not None, then download the image
        if url is not None:
            resp = urllib.request.urlopen(url)
            data = resp.read()
        # if the stream is not None, then the image has been uploaded
        elif stream is not None:
            data = stream.read()
            # convert the image to a NumPy array and then read it into
            # OpenCV format
            image = np.asarray(bytearray(data), dtype="uint8")
            image = cv2.imdecode(image, cv2.IMREAD_COLOR)

            # return the image
            return image


# =======================================================endFunctions =================================

class Home(View):
    template_name = 'Recognition/home.html'

    def get(self, request):
        return render(request, self.template_name)


# ======================================Recognize Students ===============================================

class RecognizeStudent(View):
    template_name = 'Recognition/recognize.html'
    form_class = RecognizerForm

    def get(self, request):
        return render(request, self.template_name, {'form': self.form_class})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)

        student = form.save()
        print(student.pic.path)

        path = student.pic.path
        print(path)
        unknown_image = cv2.imread(path)
        print(type(unknown_image))
        enc1 = whirldata_face_encodings(unknown_image)
        students = Students.objects.all()
        distances = {}
        for i in students:
            enc2 = i.image_features
            distance = return_euclidean_distance(enc1, enc2)
            print(distance)
            if distance < 0.4700:
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

            return render(request, 'Recognition/confirm_face.html', context)

        else:
            messages.success(request, "No such student")

        print(distances)
        return redirect('recognition:recognize-student')


# ======================================FAce Confirming =============================================
class Confirm(View):

    def post(self, request, pk):
        student_id = pk

        return redirect('recognition:recognize-student')


# =======================================Unit Booking and viewing ======================================

class UnitBooking(View):
    template_name = 'Recognition/bookUnits.html'
    form_class = BookUnit

    def get(self, request):
        query = request.GET.get("unit_name")
        result = Units.objects.all()
        if query:
            units = Units.objects.all()
            result = units.filter(unit_code__icontains=query)
            print(result)
        units_booked = []
        user = request.user
        try:
            student = Students.objects.get(student_name=user)
            print("student is", student)
            units_booked = Bookings.objects.filter(student=student)
        except Students.DoesNotExist:
            return render(request, self.template_name, {'result': result, 'units_booked': units_booked})

        return render(request, self.template_name, {'result': result, 'units_booked': units_booked})

    def post(self, request):
        user = request.user
        print(user)
        unit_id = request.POST.get("unit_id")
        try:
            student = Students.objects.get(student_name=user)
            print(student)
            department_of_student = student.student_name.department
            unit = Units.objects.get(pk=unit_id)
            exam_session = ExamSession.objects.get(unit_id=unit.id, department_id=department_of_student.id)

            booking_existance = Bookings.objects.filter(student=student, exam_session=exam_session)
            print(booking_existance)

            if booking_existance.exists():
                print("there is a problem")

                return redirect("recognition:unit-booking")
            else:
                print("created")
                Bookings.objects.create(student=student, unit_booked_id=unit.id, exam_session=exam_session)

        except ObjectDoesNotExist:

            return redirect("recognition:unit-booking")

        return redirect("recognition:unit-booking")


# ===============================Add students plus the face Features ==================================================

class AddStudent(View):
    template_name = 'Recognition/student_add.html'
    model = Students
    form_class = StudentAddForm

    def get(self, request):
        return render(request, self.template_name, {'form': self.form_class})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        image = _grab_image(stream=request.FILES["image"])
        image1 = request.FILES["image"]

        if form.is_valid():
            student = form.save()
            print(student.image.path)

            image = cv2.imwrite("/home/bassam/Desktop/projects/Students/faces/{}".format(image1), image)
            path = student.image.path
            print(path)
            known_image = cv2.imread(path)
            enc1 = whirldata_face_encodings(known_image)
            img_features = enc1
            student.image_features = img_features
            student.save()

            return redirect('recognition:students')


# =========================================Lecturers Views ==========================
class AllLecturersView(View):
    model = User
    template_name = 'Recognition/all_lecturers.html'

    def get(self, request, *args, **kwargs):
        lecturers = self.model.objects.filter(is_lecturer=1)
        return render(request, self.template_name, {'lecturers': lecturers})


# =========================================Course Views===============================
class AllCoursesView(View):
    model = Departments
    template_name = 'Recognition/all_courses.html'

    def get(self, request, *args, **kwargs):
        courses = self.model.objects.all()
        print(courses)
        return render(request, self.template_name, {'courses': courses})


class AddCourseView(View):
    template_name = 'Recognition/department.html'
    model = Departments
    form_class = DepartmentForm

    def get(self, request):
        form = DepartmentForm
        departments = Departments.objects.all()
        return render(request, self.template_name, {'form': form, 'departments': departments})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            department = form.save()
            department.save()
            return redirect('recognition:courses')


class CourseUpdateView(UpdateView):
    model = Departments
    form_class = DepartmentForm
    template_name = 'Recognition/course_update.html'
    success_url = '/home/dashboard/courses'


# ==============================Units ===========================================================

class UnitsView(View):
    template_name = 'Recognition/units.html'
    model = Units

    def get(self, request):
        units = Units.objects.all()
        return render(request, self.template_name, {'units': units})


class UnitAdd(View):
    template_name = "Recognition/unit_add.html"
    form_class = UnitForm

    def get(self, request):
        form = UnitForm

        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            unit = form.save()

            unit.save()

            return redirect('recognition:units')


class UnitUpdateView(UpdateView):
    model = Units
    form_class = UnitForm
    template_name = 'Recognition/unit_update.html'
    success_url = '/home/dashboard/units'


# ==============================View Lecturers ==================================================

class LecturersView(View):
    template_name = 'Recognition/lecturers.html'
    model = Lecturer

    def get(self, request):
        lecturers = Lecturer.objects.all()
        return render(request, self.template_name, {'lecturers': lecturers})


# ==================================Add Lecturers ===================================================


class LecturerAdd(View):
    template_name = "Recognition/lecturers_add.html"
    form_class = LecturerForm

    def get(self, request):
        form = LecturerForm

        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            unit = form.save()

            unit.save()

            return redirect('recognition:lecturers')


class AdminDashboardView(View):
    template_name = 'Recognition/dashboard.html'

    def get(self, request):
        return render(request, self.template_name)


class AllUsersView(View):
    template_name = 'Recognition/all_users.html'
    model = User

    def get(self, request, *args, **kwargs):
        users = self.model.objects.filter(is_superuser=0)
        return render(request, self.template_name, {'users': users})


class UserUpdateView(UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'Recognition/user_update.html'
    success_url = '/home/dashboard/users'


# =======================================Exams Sessions=============================================================

class ExamSessionsView(View):
    model = ExamSession
    template_name = 'Recognition/exam_sessions.html'

    def get(self, request, *args, **kwargs):
        exams_sessions = self.model.objects.all()
        exam_sessions = []

        for e in exams_sessions:
            exam_sessions.append(
                {'id': e.id,
                 'unit_code': e.unit.unit_code,
                 'unit_name': e.unit.unit_title,
                 'lecturer': e.lecturer.lecturer_name.first_name,
                 'department_name': e.department.department_name},
            )
        return render(request, self.template_name, {'exam_sessions': exam_sessions})


class ExamSessionAdd(View):
    template_name = "Recognition/exam_session_add.html"
    form_class = ExamSessionUpdateForm

    def get(self, request):
        form = ExamSessionUpdateForm

        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            unit = form.save()

            unit.save()

            return redirect('recognition:exam-sessions')


class ExamSessionUpdateView(UpdateView):
    model = ExamSession
    form_class = ExamSessionUpdateForm
    template_name = 'Recognition/exam_session_update.html'
    success_url = '/home/dashboard/exam_sessions'


# ======================================== Students Details =========================================================
class AllStudentsView(View):
    model = Students
    template_name = 'Recognition/all_students.html'

    def get(self, request, *args, **kwargs):
        students_keys = self.model.objects.all()
        students = []

        for s in students_keys:
            students.append({
                'student_id': s.id,
                'user_id': s.student_name.id,
                'student_fname': s.student_name.first_name,
                'student_lname': s.student_name.last_name,
                'reg_no': s.reg_no,
                'image_url': s.image.url,
                'department': s.student_name.department
            })

        return render(request, self.template_name, {'students': students})


# ======================================== User Registration ========================================================

class UserFormView(View):
    form_class = UserForm
    template_name = 'Recognition/registration_form.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid() and form.cleaned_data['password'] == form.cleaned_data['password_confirm']:
            user = form.save()

            password = form.cleaned_data['password']
            user.is_student = True
            user.set_password(password)

            user.save()

            user = authenticate(username=form.cleaned_data['username'], password=password)

            if user is not None:

                if user.is_active:
                    login(request, user)
                    return redirect('recognition:login')

        return render(request, self.template_name, {'form': form})


# ===================================User Login ===========================================================

class LoginUser(View):
    template_name = 'Recognition/login.html'
    form_class = LoginForm

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None and user.is_active and user.is_superuser != True:
            login(request, user)
            return redirect('recognition:home')
        elif user is not None and user.is_superuser and user.is_active:
            login(request, user)
            return redirect('recognition:dashboard')

        return render(request, self.template_name, {'form': form})


# ===================================User Login ======================================

def logoutuser(request):
    logout(request)

    return redirect('recognition:login')
