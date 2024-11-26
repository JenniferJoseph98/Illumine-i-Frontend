from django.contrib import admin
from .models import Faculty

# Register your models here.
class FacultyAdmin(admin.ModelAdmin):
    list_display = ("facultyId","email", "name", "contact_number",)

  
admin.site.register(Faculty, FacultyAdmin)