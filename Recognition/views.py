from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import View, CreateView
from .forms import *


# Create your views here.

class Home(View):
    template_name = 'Recognition/home.html'

    def get(self, request):
        return render(request, self.template_name)


class Department(View):
    template_name = 'Recognition/department.html'
    model = Departments
    form_class = DepartmentForm

    def get(self, request):
        form = DepartmentForm
        departments = Departments.objects.all()
        return render(request, self.template_name, {'form': form,'departments':departments})

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
        return render(request, self.template_name, {'units':units})


class UnitAdd(View):
    template_name = "Recognition/unit_add.html"
    form_class = UnitForm

    def get(self,request):
        form = UnitForm

        return render(request,self.template_name,{'form':form})

    def post(self,request):
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
        return render(request, self.template_name, {'lecturers':lecturers})


class LecturerAdd(View):
    template_name = "Recognition/lecturers_add.html"
    form_class = LecturerForm

    def get(self,request):
        form = LecturerForm

        return render(request,self.template_name,{'form':form})

    def post(self,request):
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
