
from django.db import models
# Create your models here.
import uuid
from cloudinary.models import CloudinaryField

class Student(models.Model):
    studentId=models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=3)
    dob = models.DateField()
    gender = models.CharField(max_length=10, choices=(("Male", "Male"), ("Female", "Female")))
    profile_pic = CloudinaryField("image", blank=True, null=True)
    contact_number = models.CharField(max_length=10)
    address = models.TextField()
    bloodgroup=models.CharField(max_length=100)
    email=models.CharField(max_length=100,unique=True)


class Faculty(models.Model):
    facultyId=models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    email=models.CharField(max_length=100,unique=True)
    name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=10)
    def __str__(self):
        return f"{self.facultyId} {self.email} {self.name} {self.contact_number}"
    

class Subject(models.Model):
    subjectId=models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100)
    faculty = models.ForeignKey(Faculty, related_name='subjects', on_delete=models.CASCADE)
    students = models.ManyToManyField(Student, related_name='subjects')
    



# Profile pic
# First Name
# Last Name
# Date of Birth
# Gender
# Blood Group
# Contact Number
# Address
