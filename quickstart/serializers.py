from rest_framework import serializers
from .models import Doctor, User, Branch, Pharmacy, Receptionist
import random, string
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email']
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
    branch = serializers.PrimaryKeyRelatedField(queryset=Branch.objects.all(), required=True)  # Ensure this handles ID correctly.

    class Meta:
        model = Pharmacy
        fields = ['id', 'experience_years', 'qualification', 'phone_number', 'address', 'user', 'branch']

    def create(self, validated_data):
        print("Validated Data Before Saving:", validated_data)  # Log validated data
        user_data = validated_data.pop('user', None)

        # Handle password
        password = user_data.pop('password', None)
        if not password:
            password = self._generate_random_password()

        # Handle username (if not provided)
        username = user_data.get('username', None)
        if not username:
            username = f"{user_data['first_name'].lower()}_{user_data['last_name'].lower()}"

        # Create the user instance
        user_instance = get_user_model()(**user_data)
        user_instance.username = username  # Set the generated username
        user_instance.set_password(password)
        user_instance.is_pharmacy = True  # Ensure this field exists in your User model
        user_instance.save()

        # Create the Pharmacy instance
        pharmacy_instance = Pharmacy.objects.create(
            user=user_instance,
            **validated_data  # Django will automatically handle branch assignment
        )

        print("Pharmacy Instance Created:", pharmacy_instance)  # Log created pharmacy instance

        # Send the email with the username and password
        self.send_pharmacy_id_email(user_instance.email, user_instance.username, password)

        return pharmacy_instance

    def send_pharmacy_id_email(self, email, username, password):
        subject = "Your Pharmacy Account Details"
        message = f"Dear Pharmacist,\n\nYour account has been created. Here are your login details:\n\nUsername: {username}\nPassword: {password}\n\nThank you!"
        from_email = settings.DEFAULT_FROM_EMAIL

        send_mail(subject, message, from_email, [email])

    def _generate_random_password(self):
        # Generate a random password (you can adjust the length and characters as needed)
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        return password





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

#----------------------Reception--------------------------------

class ReceptionSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    branch = serializers.PrimaryKeyRelatedField(queryset=Branch.objects.all(), required=True)
    class Meta:
        model = Receptionist
        fields = ['id', 'experience_years', 'qualification', 'phone_number', 'address', 'user', 'branch']

    def create(self, validated_data):
        user_data = validated_data.pop('user', None)

        password = user_data.pop('password', None)
        if not password:
            password=self._generate_random_password()

        username=user_data.get('username', None)
        if not username:
            username = f"{user_data['first_name'].lower()}_{user_data['last_name'].lower()}"

        user_instance = get_user_model()(**user_data)
        user_instance.username = username
        user_instance.set_password(password)
        user_instance.is_reception=True
        user_instance.save()

        reception_instance = Receptionist.objects.create(
            user = user_instance,
            **validated_data
        )
        self.send_reception_id_email(user_instance.email, user_instance.username, password)
        return  reception_instance


    def send_reception_id_email(self, email, username, password):
        subject ="Your Receptionist Account Details"
        message = f"Dear Receptionist,\n\n Your account has been created. Here the login details \n\n Username: {username}\nPassword:{password} \n\n Thank You !"
        from_email = settings.DEFAULT_FROM_EMAIL

        send_mail(subject, message, from_email, [email])

    def _generate_random_password(self):
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        return password


class ReceptionLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        if not user.is_reception:
            raise serializers.ValidationError('you are not authorized as a Pharmacist')
        return  {'user':user}