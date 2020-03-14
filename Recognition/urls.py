from django.conf.urls import url
from . import views

app_name = 'Recognition'

urlpatterns = [
    # home url
    url(r'^$', views.Home.as_view(), name="home"),

    # department url
    url(r'^student/$', views.AddStudent.as_view(), name="student-add"),

    # recognize url
    url(r'^recognize/$', views.RecognizeStudent.as_view(), name="recognize-student"),

    # confirm face
    url(r'^recognize/confirm/(?P<pk>[0-9]+)/$', views.Confirm.as_view(), name="confirm-student"),



    # department url
    url(r'^departments/$', views.Department.as_view(), name="department"),

    # department url
    url(r'^unit_booking/$', views.UnitBooking.as_view(), name="unit-booking"),


    # units url
    url(r'^units/$', views.UnitsView.as_view(), name="units"),

    # Add Unit  url
    url(r'^unit/add$', views.UnitAdd.as_view(), name="unit-add"),

    # lecturers url
    url(r'^lecturers/$', views.LecturersView.as_view(), name="lecturers"),

    # Add Lecturer  url
    url(r'^lecturer/add$', views.LecturerAdd.as_view(), name="lecturer-add"),

    # user registration url
    url(r'^register/$', views.UserFormView.as_view(), name="register"),
    # user login url
    url(r'^login/$', views.LoginUser.as_view(), name="login"),
    # user logout url
    url(r'^logout/$', views.logoutuser, name='logout'),

]
