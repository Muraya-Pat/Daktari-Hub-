# serializers.py
from rest_framework import serializers
from clients.models import Client
from programs.models import Program, Enrollment

class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = ['id', 'name', 'description', 'start_date', 'end_date']

class EnrollmentSerializer(serializers.ModelSerializer):
    program = ProgramSerializer()
    
    class Meta:
        model = Enrollment
        fields = ['program', 'enrollment_date']

class ClientSerializer(serializers.ModelSerializer):
    enrollments = EnrollmentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Client
        fields = [
            'id', 'first_name', 'last_name', 
            'national_id', 'date_of_birth', 'gender',
            'phone_number', 'email', 'enrollments'
        ]