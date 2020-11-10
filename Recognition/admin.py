from .models import *
from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()

admin.site.register(User)
admin.site.register(Departments)
admin.site.register(Students)
admin.site.register(Lecturer)
admin.site.register(Units)
admin.site.register(Bookings)
admin.site.register(Recognizer)
admin.site.register(ExamSession)
