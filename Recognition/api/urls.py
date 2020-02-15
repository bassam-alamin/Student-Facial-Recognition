from django.conf.urls import url
from .views import *

app_name='Recognition'
urlpatterns=[
    url(r'^users$',UserApiView.as_view(),name="users-api"),
    url(r'^user/(?P<pk>[0-9]+)$',UserRudApiView.as_view(),name="user-api"),
    url(r'^students/$',StudentApiView.as_view(),name="students-api"),
    url(r'^student/(?P<pk>[0-9]+)$', StudentRudView.as_view(), name="student-api"),
    url(r'^lecturers/$',LecturerApiView.as_view(),name="lecturers-api"),
    url(r'^lecturer/(?P<pk>[0-9]+)$', LecturerRudView.as_view(), name="lecturer-api"),
    url(r'^units/$', UnitApiView.as_view(), name="units-api"),
    url(r'^unit/(?P<pk>[0-9]+)$', UnitRudView.as_view(), name="unit-api"),
    url(r'^bookings/$', BookingApiView.as_view(), name="bookings-api"),
    url(r'^booking/(?P<pk>[0-9]+)$', BookingRudView.as_view(), name="booking-api"),
    url(r'^departments/$', DepartmentApiView.as_view(), name="departments-api"),
    url(r'^department/(?P<pk>[0-9]+)$', DepartmentRudView.as_view(), name="department-api"),



]