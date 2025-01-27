from django.urls import path
from .views import DoctorCreate, DoctorLoginView

urlpatterns = [

    path('', DoctorCreate.as_view(), name='DoctorCreate'),
    path('login', DoctorLoginView.as_view(), name='doctorloginview')

]
