import math
import urllib

import dlib
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import View, CreateView, ListView
from .forms import *
import numpy as np
import cv2
import face_recognition
import dlib
import math
import matplotlib.pyplot as plt
from skimage import exposure
from imutils.face_utils import FaceAligner
from imutils.face_utils import rect_to_bb
import imutils

# Create your views here.
# =======================================================Functions ====================================

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(
    "/home/bassam/Desktop/projects/Face Recognition Model/shape_predictor_68_face_landmarks.dat")

fa = FaceAligner(predictor, desiredFaceWidth=300)


def detect_face(path):
    img = cv2.imread(path)

    faces = detector(img)
    crop = img
    # for i, d in enumerate(faces):
    #     crop = img[d.top():d.bottom(), d.left():d.right()]
    cropped = cv2.resize(crop, (300, 300))
    gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
    # gray = cropped

    faces = detector(gray)
    points = []

    for face in faces:
        x1 = face.left()
        y1 = face.top()
        x2 = face.right()
        y2 = face.bottom()

        (x, y, w, h) = rect_to_bb(face)
        faceOrig = imutils.resize(cropped[y:y + h, x:x + w], width=300)
        aligned = fa.align(cropped, gray, face)

        # plt.imshow(cropped)
        # plt.show()

        return aligned


def crop_aligned(aligned):
    cropped = aligned
    faces = detector(aligned)
    for i, d in enumerate(faces):
        cropped = cropped[d.top():d.bottom(), d.left():d.right()]

        # plt.imshow(cropped)
        # plt.show()
    return cropped


def draw_points(aligned):
    cropped = cv2.resize(aligned, (300, 300))
    gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)

    faces = detector(gray)
    points = []
    vec = []
    for face in faces:
        x1 = face.left()
        y1 = face.top()
        x2 = face.right()
        y2 = face.bottom()

        # cv2.rectangle(cropped, (x1, y1), (x2, y2), (0, 255, 0), 3)

        # dope staff to make sure only face is projected
        cropped = cropped[y1:y2, x1:x2]

        landmarks = predictor(cropped, face)

        vec = np.empty([68, 2], dtype=int)
        for i in range(0, 68):
            vec[i][0] = landmarks.part(i).x
            vec[i][1] = landmarks.part(i).y
            points.append(landmarks.part(i))
            print(landmarks.part(i))

            cv2.circle(cropped, (vec[i][0], vec[i][1]), 1, (255, 0, 0), -1)
            plt.imshow(cv2.circle(cropped, (vec[i][0], vec[i][1]), 1, (255, 0, 0), -1), cmap="gray")
        plt.show()
        print(tuple(vec))

    return vec


def euclidean_distance(vec1, vec2):
    total = 0
    for i in range(17, 48):
        x = vec1[i]
        y = vec2[i]
        distance = math.sqrt(sum([(a - b) ** 2 for a, b in zip(x, y)]))
        total = total + distance
        print("Euclidean distance from {} and {}:{} ".format(x, y, distance))

    print(total)

    return total


def _grab_image(path=None, stream=None, url=None):
    # if the path is not None, then load the image from disk
    if path is not None:
        image = cv2.imread(path)
    # otherwise, the image does not reside on disk
    else:
        # if the URL is not None, then download the image
        if url is not None:
            resp = urllib.urlopen(url)
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


#
# image1 = "/home/bassam/Desktop/projects/Face Recognition Model/images/mayow5.jpg"
# image2 = "/home/bassam/Desktop/projects/Face Recognition Model/images/mayow4.jpg"
#
# aligned1 = detect_face(image1)
# aligned2 = detect_face(image2)
#
# cropped1 = crop_aligned(aligned1)
# cropped2 = crop_aligned(aligned2)
#
# vec1 = draw_points(cropped1)
# vec2 = draw_points(cropped2)
#
# euclidean_distance(vec1, vec2)
#
# cv2.destroyAllWindows()


# =======================================================endFunctions =================================

class Home(View):
    template_name = 'Recognition/home.html'

    def get(self, request):
        return render(request, self.template_name)


class RecognizeStudent(View):
    template_name = 'Recognition/recognize.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        image1 = request.FILES["image"]
        image = _grab_image(stream=request.FILES["image"])

        # image = request.FILES["image"].read()
        image = cv2.imwrite("/home/bassam/Desktop/projects/Students/faces/{}".format(image1), image)
        path = "/home/bassam/Desktop/projects/Students/faces/{}".format(image1)
        aligned = detect_face(path)
        cropped = crop_aligned(aligned)
        img_features = draw_points(cropped)
        students = Students.objects.all()
        for i in students:
            im1 = i.image_features
            euclidean_distance(img_features, im1)

        print("we have posted")
        return redirect('recognition:recognize-student')


class UnitBooking(View):
    template_name = 'Recognition/bookUnits.html'
    form_class = BookUnit

    def get(self, request):
        query = request.GET.get("plate_no")
        result = Units.objects.all()
        if query:
            units = Units.objects.all()
            result = units.filter(unit_code__icontains=query)
            print(result)
        return render(request, self.template_name, {'result': result})

    def post(self,request):
        user = request.user
        unit_id = request.POST.get("unit_id")
        student = Students.objects.get(student_name=user)
        unit = Units.objects.get(pk = unit_id)
        Bookings.objects.create(student=student,unit_booked_id=unit.id)

        return redirect("recognition:unit-booking")


class AddStudent(View):
    template_name = 'Recognition/student_add.html'
    model = Students
    form_class = StudentAddForm

    def get(self, request):
        return render(request, self.template_name, {'form': self.form_class})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():
            student = form.save()
            print(student.image.path)

            img = student.image.path
            aligned = detect_face(img)
            cropped = crop_aligned(aligned)
            img_features = draw_points(cropped)
            student.image_features = img_features
            student.save()

            return redirect('recognition:department')


class Department(View):
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
            return redirect('recognition:department')


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


class LecturersView(View):
    template_name = 'Recognition/lecturers.html'
    model = Lecturer

    def get(self, request):
        lecturers = Lecturer.objects.all()
        return render(request, self.template_name, {'lecturers': lecturers})


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

        if user is not None and user.is_active:
            login(request, user)
            return redirect('recognition:home')

        return render(request, self.template_name, {'form': form})


def logoutuser(request):
    logout(request)

    return redirect('recognition:login')
