from django.conf.urls import url
from .views import *
from rest_framework.authtoken import views
app_name='Recognition'
urlpatterns=[

    # user login url
    url(r'login/',views.obtain_auth_token,name='api-login'),

    # specific user search with username
    url(r'^users/(?P<username>.+)$',UserApiView.as_view(),name="users-api"),
    # specific user url with id
    url(r'^user/(?P<pk>[0-9]+)$',UserRudApiView.as_view(),name="user-api"),


    # student face recognizer view url
    url(r'^students/(?P<imagestring>.+)$', StudentRecognizerView.as_view(), name="student-recognizer"),

    # all students
    url(r'^students/$',StudentApiView.as_view(),name="students-api"),
    # specific student with id url
    url(r'^student/(?P<pk>[0-9]+)$', StudentRudView.as_view(), name="student-api"),

    # all lecturers
    url(r'^lecturers/$',LecturerApiView.as_view(),name="lecturers-api"),
    # specific lecturer details with id
    url(r'^lecturer/(?P<pk>[0-9]+)$', LecturerRudView.as_view(), name="lecturer-api"),

    # All units details display
    url(r'^units/$', UnitApiView.as_view(), name="units-api"),
    # specific unit detail with id
    url(r'^unit/(?P<pk>[0-9]+)$', UnitRudView.as_view(), name="unit-api"),

    # Bookings display
    url(r'^bookings/$', BookingApiView.as_view(), name="bookings-api"),
    url(r'^booking/(?P<pk>[0-9]+)$', BookingRudView.as_view(), name="booking-api"),

    # check if student had already booked for the session before
    url(r'^student/booking/$',BookingExistance.as_view(),name="booking-existance"),
    # update the booked session as attended by the student
    url(r'^student/booking/(?P<pk>[0-9]+)$', BookingExistance.as_view(), name="booking-update_attended"),

    # all Departments details
    url(r'^departments/$', DepartmentApiView.as_view(), name="departments-api"),
    # specific department details using pk
    url(r'^department/(?P<pk>[0-9]+)$', DepartmentRudView.as_view(), name="department-api"),

    # display all the examination sessions for the lecturer
    url(r'^exam-session/(?P<pk>[0-9]+)',ExamSessionView.as_view(),name="lecturer-exam-sessions"),

    # students who attended the Examination session
    url(r'^attended/(?P<pk>[0-9]+)$',CurrentUnitReport.as_view(), name="currentUnit-report")


]