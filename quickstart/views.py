from django.core.serializers import serialize
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from .models import Doctor, Pharmacy
from .serializers import DoctorSerializer, DoctorLoginSerializer, PharmacySerializer, PharmacyLoginSerializer
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token


class DoctorCreate(APIView):
    def get(self, request):
        doctor_data = Doctor.objects.select_related('user', 'branch').all()
        serializer = DoctorSerializer(doctor_data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = DoctorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DoctorLoginView(APIView):
    def post(self, request):
        serializer = DoctorLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)

            token, created = Token.objects.get_or_create(user=user)
            return Response({"message":"Login successful",
                         "token":token.key}, status=status.HTTP_200_OK)
        return Response({"message":"invalid credentials",
                         "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


# --------------------------PHARMACY ---------------------------------
class PharmacyCreate(APIView):
    def get(self, request):
        pharmacy_data =Pharmacy.objects.select_related('user', 'branch').all()
        serializer = PharmacySerializer(pharmacy_data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def post(self, request):
        serializer = PharmacySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PharmacyLoginView(APIView):
    def post(self, request):
        serializer = PharmacyLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)
            token, created =Token.objects.get_or_create(user=user)
            return Response({"message":"Login Successful", "token":token.key}, status=status.HTTP_200_OK)
        return Response({"message":"Invalid credentials", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)