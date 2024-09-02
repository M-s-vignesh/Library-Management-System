from django.contrib import admin
from .models import Student_details
# Register your models here.
class student(admin.ModelAdmin):
    list_display = ['name','student_id','department']
    prepopulated_fields = {'slug':('name',)}
admin.site.register(Student_details,student)