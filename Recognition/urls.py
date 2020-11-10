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
    url(r'^unit_booking/$', views.UnitBooking.as_view(), name="unit-booking"),


    # units url
    url(r'^dashboard/units$', views.UnitsView.as_view(), name="units"),

    # Add Unit  url
    url(r'^unit/add$', views.UnitAdd.as_view(), name="unit-add"),

    # Update unit url
    url(r'^dashboard/update_unit/(?P<pk>[0-9]+)/$', views.UnitUpdateView.as_view(), name="unit-update"),

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

    # admin dashboard url
    url(r'^dashboard/$', views.AdminDashboardView.as_view(), name="dashboard"),

    # add Course url

    url(r'^dashboard/add_course$', views.AddCourseView.as_view(), name="add-course"),

    # all courses url
    url(r'^dashboard/courses$', views.AllCoursesView.as_view(), name="courses"),

    # update course url
    url(r'^dashboard/course/update/(?P<pk>[0-9]+)/$', views.CourseUpdateView.as_view(), name="course-update"),

    # all users url
    url(r'^dashboard/users/$', views.AllUsersView.as_view(), name="all-users"),

    # update user url
    url(r'^dashboard/user/update/(?P<pk>[0-9]+)/$', views.UserUpdateView.as_view(), name="user-update"),

    # exam sessions url
    url(r'^dashboard/exam_sessions/$',views.ExamSessionsView.as_view(),name="exam-sessions"),

    # exam session update url
    url(r'^dashboard/exam_session/update/(?P<pk>[0-9]+)/$',views.ExamSessionUpdateView.as_view(),name="exam-update"),

    # exam session add url
    url(r'^dashboard/exam_session/add/$',views.ExamSessionAdd.as_view(),name="exam-add"),

    # All students url
    url(r'^dashboard/students/$',views.AllStudentsView.as_view(),name='students'),

    # All lecturers url
    url(r'^dashboard/lecturers/$', views.AllLecturersView.as_view(), name='lecturers'),

]
