from rest_framework import serializers
from .models import Doctor, User, Branch, Pharmacy
import random, string
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}  # Hide password in responses

class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = '__all__'


# -----------------------Doctor Serializer ---------------------------------------
class DoctorSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    branch = BranchSerializer()

    class Meta:
        model = Doctor
        fields = '__all__'

    def create(self, validated_data):
        user_data = validated_data.pop('user', None)
        branch_data = validated_data.pop('branch')

        branch_instance, created = Branch.objects.get_or_create(**branch_data)
        password = user_data.pop('password', None)
        user_instance = User(**user_data)
        user_instance.set_password(password)
        user_instance.is_doctor = True  # Set role as doctor
        user_instance.save()


        doctor_id_number = f"A{random.choice(string.ascii_uppercase)}{random.randint(1000, 9999)}"
        print(doctor_id_number)
        # Create Doctor instance with associated user
        doctor_instance = Doctor.objects.create(
            user=user_instance,
            branch=branch_instance,
            **validated_data)
        self.send_doctor_id_email(user_instance.email, doctor_id_number)
        return doctor_instance

    def send_doctor_id_email(self, email, doctor_id_number):
        subject = "Your Doctor ID Number"
        message = f"Dear Doctor, \n\n Your  doctor ID number is: {doctor_id_number}. \n\n Thank You !"
        from_email = settings.DEFAULT_FROM_EMAIL

        send_mail(subject, message, from_email, [email])


class DoctorLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        if not user.is_doctor:
            raise serializers.ValidationError("You are not authorized as a doctor")
        return {'user':user}


# --------------------------Pharmacy Serializer ----------------------------------------

class PharmacySerializer(serializers.ModelSerializer):
    user = UserSerializer()
    branch = BranchSerializer()
    class Meta:
        model = Pharmacy
        fields = '__all__'

    def create(self, validated_data):
        user_data = validated_data.pop('user', None)
        branch_data = validated_data.pop('branch')

        branch_instance, created = Branch.objects.get_or_create(**branch_data)
        password = user_data.pop('password', None)
        user_instance = User(**user_data)
        user_instance.set_password(password)
        user_instance.is_pharmacy=True
        user_instance.save()

        pharmacy_id_number = f"A{random.choice(string.ascii_uppercase)}{random.randint(1000, 9999)}"
        pharmacy_instance = Pharmacy.objects.create(user=user_instance, branch=branch_instance, **validated_data)
        self.send_pharmacy_id_email(user_instance.email, pharmacy_id_number)
        return  pharmacy_instance


    def send_pharmacy_id_email(self, email, pharmacy_id_number):
        subject ="Your Pharmacist ID Number"
        message = f"Dear Pharmacist, \n\n Your Pharmacist ID number is: {pharmacy_id_number}. \n\n Thank You !"
        from_email = settings.DEFAULT_FROM_EMAIL

        send_mail(subject, message, from_email, [email])

class PharmacyLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        if not user.is_pharmacy:
            raise serializers.ValidationError('you are not authorized as a Pharmacist')
        return  {'user':user}