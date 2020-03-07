import os

from django import forms
from django.utils import timezone
import datetime,calendar

from Students import settings
from .models import *
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
User = get_user_model()


class DepartmentForm(forms.ModelForm):

    class Meta:
        model = Departments
        fields = ['department_name']
        widgets = {
            'department_name': forms.TextInput(attrs={'class':'form-control','placeholder':'Department name...'}),
        }

class UnitForm(forms.ModelForm):

    class Meta:
        model = Units
        fields = ['unit_title','unit_code','unit_lecturer','year','semester']
        widgets = {
            'unit_title': forms.TextInput(attrs={'class':'form-control','placeholder':'Unit title ...'}),
            'unit_code': forms.TextInput(attrs={'class': 'form-control ', 'placeholder': 'i.e Comp420 ...'}),
            'unit_lecturer': forms.Select(attrs={'class': 'form-control '}),
            'year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'year'}),
            'semester': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'semester'}),

        }

class LecturerForm(forms.ModelForm):

    class Meta:
        model = Lecturer
        fields = ['lecturer_name',"staff_no"]
        widgets = {
            'lecturer_name': forms.Select(attrs={'class':'form-control','placeholder':'Unit title ...'}),
            'staff_no': forms.TextInput(attrs={'class': 'form-control ','placeholder':'Staff No....'}),

        }


class StudentAddForm(forms.ModelForm):

    class Meta:
        model = Students
        fields = ["student_name","reg_no","image"]

        widgets = {
            "student_name":forms.Select(attrs={'class':'form-control'}),
            "reg_no":forms.TextInput(attrs={'class':'form-control','placeholder':'Assign reg_no ...'}),
            "image": forms.FileInput(attrs={'class': 'form-control'}),
        }

    # def clean_image(self):



        # img = self.cleaned_data['image']
        # cv_image = cv2.imread(img)
        # print(type(cv_image))

        # print(type(img))

        # return img





















class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email','phone_no','id_no','department' ,'password']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control pt-0 mt-0','placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control pt-0 mt-0','placeholder': 'Second Name'}),
            'username': forms.TextInput(attrs={'class': 'form-control pt-0 mt-0','placeholder': 'Index Number'}),
            'email':forms.TextInput(attrs={'class': 'form-control pt-0 mt-0','placeholder': 'email'}),
            'phone_no': forms.TextInput(attrs={'class': 'form-control pt-0 mt-0', 'placeholder': 'Phone no'}),
            'id_no': forms.TextInput(attrs={'class': 'form-control pt-0 mt-0', 'placeholder': 'ID No...'}),
            'department': forms.Select(attrs={'class': 'form-control pt-0 mt-0', 'placeholder': 'email'}),

        }
    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if first_name.isalpha() == False:
            raise forms.ValidationError("Name cant have Numbers")
        else:
            return first_name

    def clean_second_name(self):
        second_name = self.cleaned_data['second_name']

        if second_name.isalpha() == False:
            raise ValidationError('Name cant have numbers')
        else:
            return second_name

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password != password_confirm:
            self.add_error('password_confirm', "Password does not match")
        return cleaned_data

class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }
