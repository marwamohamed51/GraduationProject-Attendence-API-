from rest_framework import serializers
from .models import Student, Attended

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

class AttendedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attended
        fields = '__all__'