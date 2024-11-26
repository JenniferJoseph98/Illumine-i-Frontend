from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import Student,Faculty,Subject
from rest_framework.exceptions import NotFound
from .serializers import StudentSerializer,FacultySerializer,SubjectSerializer,CustomSubjectSerializer,LimitedStudentSerializer
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import os
from django.db import transaction




class DeleteAllStudentsAndSubjects(APIView):
    def delete(self, request):
        try:
            # Delete all records in Subject and Student
            Subject.objects.all().delete()
            Student.objects.all().delete()

            return Response(
                {"message": "All Student and Subject records deleted successfully."},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
# Create your views here.

def index(request):
    return HttpResponse('Hello World, Have a Good day')

# Add student (POST)
# class AddStudentView(APIView):
#     def post(self, request):
#         serializer = StudentSerializer(data=request.data) # QUery to add new student
#         if serializer.is_valid():
#             serializer.save()
#             return Response({"status": "success", "data": serializer.data}, status=status.HTTP_201_CREATED)
#         else:
#             return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class AddStudentView(APIView):
    def post(self, request,facultyId):
        try:
            # Check if facultyId is provided
            if not facultyId:
                return Response(
                    {"status": "error", "message": "facultyId is required."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Verify if the faculty exists
            faculty = Faculty.objects.get(facultyId=facultyId)  # Raises DoesNotExist if not found
            
            # Proceed to validate and save the student data
            serializer = StudentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()  # Save the student record
                return Response(
                    {"status": "success", "data": serializer.data},
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response(
                    {"status": "error", "data": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        except Faculty.DoesNotExist:
            # Handle case when the facultyId is invalid
            return Response(
                {"status": "error", "message": "Invalid facultyId. Faculty not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            # Handle unexpected errors
            return Response(
                {"status": "error", "message": f"An unexpected error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )



#Add Faculty (POST)
class AddFacultyView(APIView):
    def post(self, request):
        serializer = FacultySerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
# Faculty Login
class FacultyLoginAPIView(APIView):
    def post(self, request):
        # Extract data from the request
        email = request.data.get('email')
        password = request.data.get('password')
        code = request.data.get('code')

        # Check for Employee Code
        if code != "1234":
            return Response({"error": "Invalid Employee Code"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            # Check faculty credentials
            faculty = Faculty.objects.get(email=email)
            expected_password = f"{email[:4]}{faculty.contact_number[-4:]}"  # first 4 of email and last 4 of contact
            print(expected_password)
            if password == expected_password:
                return Response({"message": "Login Successful", "faculty_id": faculty.facultyId}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid Password"}, status=status.HTTP_401_UNAUTHORIZED)
        except Faculty.DoesNotExist:
            return Response({"error": "Faculty Not Found"}, status=status.HTTP_404_NOT_FOUND)


#Student Login

class StudentLoginAPIView(APIView):
    def post(self, request):
        # Extract data from the request
        email = request.data.get('email')
        password = request.data.get('password')
     

        try:
            # Check student credentials
            student = Student.objects.get(email=email)
            expected_password = f"{email[:4]}{student.contact_number[-4:]}"  # First 4 letters of name, last 4 of contact
            if password == expected_password:
                return Response({"message": "Login Successful", "student_id": student.studentId}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid Password"}, status=status.HTTP_401_UNAUTHORIZED)
        except Student.DoesNotExist:
            return Response({"error": "Student Not Found"}, status=status.HTTP_404_NOT_FOUND)

  
  
  
        

# View all students (GET)
class ViewStudentView(APIView):
    def get(self, request):
        students = Student.objects.all()  # Query all students
        serializer = StudentSerializer(students, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)



# View all Faculty (GET)
class ViewFacultyView(APIView):
    def get(self, request):
        faculty = Faculty.objects.all()  # Query all students
        serializer = FacultySerializer(faculty, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
    

#View Student details by id
class ViewStudentById(APIView):
    def get(self, request, student_id=None):
        try:
            student = Student.objects.get(studentId=student_id)
        except Student.DoesNotExist:
            raise NotFound(detail="Student not found.")
        serializer = StudentSerializer(student)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

#View Faculty details by id
class ViewFacultyById(APIView):
    def get(self, request, facultyId=None):
        try:
            faculty = Faculty.objects.get(facultyId=facultyId)
        except Faculty.DoesNotExist:
            raise NotFound(detail="Faculty not found.")
        serializer = FacultySerializer(faculty)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
      
  
#Update student  
class UpdateStudentView(APIView):
    def put(self, request):
        try:
            # Extract the IDs from the request data
            faculty_id = request.data.get("facultyId")
            student_id = request.data.get("studentId")
            if not faculty_id and not student_id:
                return Response(
                    {"status": "error", "message": "facultyId or studentId is required to update a student record."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if faculty_id:
                # Verify the faculty exists
                try:
                    Faculty.objects.get(facultyId=faculty_id)
                    # Faculty can update any student
                    student = Student.objects.get(studentId=student_id)
                except Faculty.DoesNotExist:
                    return Response(
                        {"status": "error", "message": "Invalid facultyId. Faculty not found."},
                        status=status.HTTP_404_NOT_FOUND
                    )
                except Student.DoesNotExist:
                    return Response(
                        {"status": "error", "message": "Invalid updateStudentId. Student not found."},
                        status=status.HTTP_404_NOT_FOUND
                    )
            elif student_id:
                # Verify the student exists
                try:
                    student = Student.objects.get(studentId=student_id)
                    print(student.studentId , student_id)
                    
                    # A student can only update their own data
                    if str(student.studentId) != str(student_id):
                        return Response(
                            {"status": "error", "message": "Students can only update their own data."},
                            status=status.HTTP_403_FORBIDDEN
                        )
                except Student.DoesNotExist:
                    return Response(
                        {"status": "error", "message": "Invalid studentId. Student not found."},
                        status=status.HTTP_404_NOT_FOUND
                    )

            # Update the student's data
            serializer = StudentSerializer(student, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"status": "success", "message": "Student record updated successfully.", "data": serializer.data},
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {"status": "error", "message": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )

        except Exception as e:
            # Handle unexpected errors
            return Response(
                {"status": "error", "message": f"An unexpected error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
#Add profile picture
class UpdateStudentProfilePictureView(APIView):
    def put(self, request):
        try:
            # Extract studentId and profile picture from the request
            student_id = request.data.get("studentId")
            profile_picture = request.FILES.get("profile_pic")

            if not student_id:
                return Response(
                    {"status": "error", "message": "studentId is required."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            if not profile_picture:
                return Response(
                    {"status": "error", "message": "profile_pic is required."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Check if the file size is within the 1MB limit
            max_size = 1 * 1024 * 1024  # 1MB in bytes
            if profile_picture.size > max_size:
                return Response(
                    {"status": "error", "message": "Profile picture must be 1MB or smaller."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Check if the student exists
            try:
                student = Student.objects.get(studentId=student_id)
            except Student.DoesNotExist:
                return Response(
                    {"status": "error", "message": "Invalid studentId. Student not found."},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Define the directory to save the profile pictures
            profile_pics_dir = os.path.join(settings.MEDIA_ROOT, "profile_pics")
            if not os.path.exists(profile_pics_dir):
                os.makedirs(profile_pics_dir)  # Create the directory if it doesn't exist

            # Save the file to the directory
            file_path = os.path.join(profile_pics_dir, profile_picture.name)
            with open(file_path, "wb+") as destination:
                for chunk in profile_picture.chunks():
                    destination.write(chunk)

            # Update the student's profile_pic field with the relative path
            relative_path = f"profile_pics/{profile_picture.name}"
            student.profile_pic = relative_path
            student.save()

            return Response(
                {
                    "status": "success",
                    "message": "Profile picture updated successfully.",
                    "data": {
                        "studentId": student.studentId,
                        "profile_pic": relative_path
                    }
                },
                status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                {"status": "error", "message": f"An unexpected error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
# Add Subject

class AddSubjectView(APIView):
    def post(self, request):
        try:
            # Extract facultyId and subject name from the request data
            faculty_id = request.data.get("facultyId")
            subject_name = request.data.get("name")
            
            if not faculty_id:
                return Response(
                    {"status": "error", "message": "facultyId is required."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            if not subject_name:
                return Response(
                    {"status": "error", "message": "Subject name is required."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Check if the faculty exists using facultyId
            try:
                faculty = Faculty.objects.get(facultyId=faculty_id)
            except Faculty.DoesNotExist:
                return Response(
                    {"status": "error", "message": "Invalid facultyId. Faculty not found."},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Check if the faculty already has a subject assigned
            if Subject.objects.filter(faculty=faculty).exists():
                return Response(
                    {"status": "error", "message": "This faculty already has a subject assigned."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Create the Subject and assign the Faculty instance
            subject = Subject.objects.create(name=subject_name, faculty=faculty)

            # Serialize and return the created subject
            serializer = SubjectSerializer(subject)
            return Response(
                {"status": "success", "message": "Subject created successfully.", "data": serializer.data},
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            return Response(
                {"status": "error", "message": f"An unexpected error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


#Faculty who dont have subject

class FacultyWithoutSubjectsView(APIView):
    def get(self, request):
        try:
            # Find all faculties who don't have any subjects assigned
            faculties_without_subjects = Faculty.objects.filter(subjects__isnull=True)

            # If no faculties found
            if not faculties_without_subjects:
                return Response(
                    {"status": "error", "message": "No faculties without subjects found."},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Serialize the faculties
            serializer = FacultySerializer(faculties_without_subjects, many=True)

            return Response(
                {"status": "success", "data": serializer.data},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"status": "error", "message": f"An unexpected error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
 
#View Subject details for one faculty with the help of FacultyId
            
class SubjectByFacultyView(APIView):
    def get(self, request, faculty_id):
        try:
            # Fetch subjects filtered by facultyId
            subjects = Subject.objects.select_related('faculty').prefetch_related('students').filter(faculty__facultyId=faculty_id)
            
            # Serialize the data
            # serializer = SubjectSerializer(subjects, many=True)
            serializer = CustomSubjectSerializer(subjects, many=True)
            
            return Response(
                {"status": "success", "data": serializer.data},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"status": "error", "message": f"An unexpected error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

#View all the subject with faculty

class SubjectAndFacultyView(APIView):
    def get(self, request):
        try:
            # Fetch all subjects with related faculty data
            subjects = Subject.objects.select_related('faculty').prefetch_related('students').all()

            # Serialize the data
            serializer = SubjectSerializer(subjects, many=True)

            return Response(
                {"status": "success", "data": serializer.data},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"status": "error", "message": f"An unexpected error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
            
#Student enrollment

class EnrollStudentView(APIView):
    def post(self, request):
        try:
            # Extract subjectId and studentId from the request data
            subject_id = request.data.get("subjectId")
            student_id = request.data.get("studentId")

            if not subject_id:
                return Response(
                    {"status": "error", "message": "SubjectId is required."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            if not student_id:
                return Response(
                    {"status": "error", "message": "StudentId is required."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Check if the subject exists
            try:
                subject = Subject.objects.get(subjectId=subject_id)
            except Subject.DoesNotExist:
                return Response(
                    {"status": "error", "message": "Invalid SubjectId. Subject not found."},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Check if the student exists
            try:
                student = Student.objects.get(studentId=student_id)
            except Student.DoesNotExist:
                return Response(
                    {"status": "error", "message": "Invalid StudentId. Student not found."},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Check if the student is already enrolled in the subject
            if subject.students.filter(studentId=student_id).exists():
                return Response(
                    {"status": "error", "message": "Student is already enrolled in this subject."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Add the student to the subject
            subject.students.add(student)
            return Response(
                {"status": "success", "message": "Student enrolled successfully in the subject."},
                status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                {"status": "error", "message": f"An unexpected error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )





#Enrolled course


class EnrolledSubjectsView(APIView):
    def get(self, request,student_id):
        try:
            if not student_id:
                return Response(
                    {"status": "error", "message": "StudentId is required."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Check if the student exists
            try:
                student = Student.objects.get(studentId=student_id)
            except Student.DoesNotExist:
                return Response(
                    {"status": "error", "message": "Invalid StudentId. Student not found."},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Get all subjects the student is enrolled in
            subjects = Subject.objects.filter(students=student)
            serializer = SubjectSerializer(subjects, many=True)

            return Response(
                {"status": "success", "data": serializer.data},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"status": "error", "message": f"An unexpected error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
          
#Available course

class AvailableCoursesView(APIView):
    def get(self, request,student_id):
        try:            
            if not student_id:
                return Response(
                    {"status": "error", "message": "StudentId is required."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Check if the student exists
            try:
                student = Student.objects.get(studentId=student_id)
            except Student.DoesNotExist:
                return Response(
                    {"status": "error", "message": "Invalid StudentId. Student not found."},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Get all subjects the student is NOT enrolled in
            subjects = Subject.objects.exclude(students=student)
            serializer = SubjectSerializer(subjects, many=True)

            return Response(
                {"status": "success", "data": serializer.data},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"status": "error", "message": f"An unexpected error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )          
            
            
            
            
class EnrollStudentInFacultySubject(APIView):
    def post(self, request):
        try:
            # Extract facultyId and studentId from the request data
            faculty_id = request.data.get("facultyId")
            student_id = request.data.get("studentId")

            if not faculty_id or not student_id:
                return Response(
                    {"status": "error", "message": "facultyId and studentId are required."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Check if the faculty exists
            try:
                faculty = Faculty.objects.get(facultyId=faculty_id)
            except Faculty.DoesNotExist:
                return Response(
                    {"status": "error", "message": "Invalid facultyId. Faculty not found."},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Check if the student exists
            try:
                student = Student.objects.get(studentId=student_id)
            except Student.DoesNotExist:
                return Response(
                    {"status": "error", "message": "Invalid studentId. Student not found."},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Check if the faculty has a subject assigned
            try:
                subject = Subject.objects.get(faculty=faculty)
            except Subject.DoesNotExist:
                return Response(
                    {"status": "error", "message": "No subject found for this faculty."},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Check if the student is already enrolled in the subject
            if subject.students.filter(studentId=student_id).exists():
                return Response(
                    {"status": "error", "message": "Student is already enrolled in this subject."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Enroll the student in the subject
            subject.students.add(student)
            return Response(
                {"status": "success", "message": "Student successfully enrolled in the subject."},
                status=status.HTTP_200_OK
            )
        
        except Exception as e:
            return Response(
                {"status": "error", "message": f"An unexpected error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# Get Students Not Enrolled in Faculty's Subject
class UnenrolledStudent(APIView):
    def get(self, request, faculty_id):
        try:
            # Check if the faculty exists
            try:
                faculty = Faculty.objects.get(facultyId=faculty_id)
            except Faculty.DoesNotExist:
                return Response(
                    {"status": "error", "message": "Invalid facultyId. Faculty not found."},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Get the subject assigned to the faculty
            try:
                subject = Subject.objects.get(faculty=faculty)
            except Subject.DoesNotExist:
                return Response(
                    {"status": "error", "message": "No subject found for this faculty."},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Get all students who are **not** enrolled in the faculty's subject
            students_not_enrolled = Student.objects.exclude(subjects=subject)

            # Serialize the student data
            student_data = LimitedStudentSerializer(students_not_enrolled, many=True)

            return Response(
                {"status": "success", "data": student_data.data},
                status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                {"status": "error", "message": f"An unexpected error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
