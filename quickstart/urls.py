from django.urls import path
from .views import DoctorCreate, DoctorLoginView, PharmacyCreate, PharmacyLoginView, ReceptionCreate, ReceptionLoginView, BranchCreate

urlpatterns = [

    path('', DoctorCreate.as_view(), name='DoctorCreate'),
    path('login', DoctorLoginView.as_view(), name='doctorloginview'),

    path('branch/', BranchCreate.as_view(), name='branchCreate'),


    path('pharmacy/', PharmacyCreate.as_view(), name='pharmacyCreate'),
    path('pharmacylogin', PharmacyLoginView.as_view(), name='pharmacyloginview'),

    path('reception/', ReceptionCreate.as_view(), name='receptionCreate'),
    path('receptionlogin', ReceptionLoginView.as_view(), name='receptionloginview'),

]
