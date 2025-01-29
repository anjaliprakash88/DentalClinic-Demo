from django.contrib import admin
from .models import Doctor, User, Receptionist, Pharmacy,Branch

admin.site.register(User)
admin.site.register(Doctor)
admin.site.register(Receptionist),
admin.site.register(Pharmacy)
admin.site.register(Branch)
