from django.contrib import admin
from .models import Doctor, User

admin.site.register(User)
admin.site.register(Doctor)