from django.urls import path
from .views import DoctorCreate, DoctorLoginView, PharmacyCreate, PharmacyLoginView

urlpatterns = [

    path('', DoctorCreate.as_view(), name='DoctorCreate'),
    path('login', DoctorLoginView.as_view(), name='doctorloginview'),

    path('pharmacy', PharmacyCreate.as_view(), name='pharmacyCreate'),
    path('pharmacylogin', PharmacyLoginView.as_view(), name='pharmacyloginview'),

]
