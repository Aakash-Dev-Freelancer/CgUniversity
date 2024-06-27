# in myapp/serializers.py
from rest_framework import serializers
from .models import Student, StudentData, StudentLogin, MarkSheets, AdminLogin, ContactForm

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

class StudentLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentLogin
        fields = '__all__'
    

class StudentDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentData
        fields = '__all__'


class MarkSheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarkSheets
        fields = '__all__'

class AdminLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminLogin
        fields = '__all__'

class ContactFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactForm
        fields = '__all__'
