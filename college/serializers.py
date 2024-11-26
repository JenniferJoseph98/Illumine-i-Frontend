from rest_framework import serializers
from .models import Student,Faculty,Subject

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'


class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = '__all__'
        
class SubjectSerializer(serializers.ModelSerializer):
    faculty = FacultySerializer()
    students = StudentSerializer(many=True)
    class Meta:
        model = Subject
        fields = '__all__'


class LimitedStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'gender', 'email', 'contact_number', 'studentId']

class CustomSubjectSerializer(serializers.ModelSerializer):
    faculty = FacultySerializer()
    students = LimitedStudentSerializer(many=True)  # Use limited fields for students

    class Meta:
        model = Subject
        fields = ['id', 'subjectId', 'name', 'faculty', 'students']
