from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('delete',views.DeleteAllStudentsAndSubjects.as_view(),name='delete'),
    path('faculty/login',views.FacultyLoginAPIView.as_view(),name='facultylogin'),
    path('student/login',views.StudentLoginAPIView.as_view(),name='studentlogin'),
    path('viewsinglestudent/<str:student_id>',views.ViewStudentById.as_view(),name='viewSingleStudent'),
    path('viewstudent', views.ViewStudentView.as_view(), name='student_viewset'),
    path('addstudent/<str:facultyId>', views.AddStudentView.as_view(), name='add_Student'),
    path('viewsubject/<str:faculty_id>', views.SubjectByFacultyView.as_view(), name='viewfacultysubject'),
    path('update', views.UpdateStudentView.as_view(), name='update_Student'),
    path('addfaculty',views.AddFacultyView.as_view(),name='addFaculty'),
    path('addsubject',views.AddSubjectView.as_view(),name='addSubject'),
    path('viewfaculty',views.ViewFacultyView.as_view(),name="addfaculty"),
    path('viewsinglefaculty/<str:facultyId>',views.ViewFacultyById.as_view(),name='viewfacultybyid'),
    path('withoutsubject',views.FacultyWithoutSubjectsView.as_view(),name="withoutsubject"),
    path('subject',views.SubjectAndFacultyView.as_view(),name='viewsubject'),
    path('enroll',views.EnrollStudentView.as_view(),name='enroll'),
    path('enrolledcourse/<str:student_id>',views.EnrolledSubjectsView.as_view(),name='enrolledcourse'),
    path('availablecourse/<str:student_id>',views.AvailableCoursesView.as_view(),name='availablecourse'),
    path('enrollbyfaculty',views.EnrollStudentInFacultySubject.as_view(),name='enrolledbyfaculty'),
    path('unenrolledstudent/<str:faculty_id>',views.UnenrolledStudent.as_view(),name='unenrolledstudent'),
    path('students/update-profile-pic/<str:studentId>', views.UpdateProfilePicView.as_view(), name='update-profile-pic'),

]
