# from django.contrib import admin
# from .models import Student_details
# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from django.contrib.auth import get_user_model

# # # Register your models here.
# User = get_user_model()

# class student_details_inline(admin.TabularInline):
#     model = Student_details

# class UserAdmin(BaseUserAdmin):
#     list_display = ['Emp_ID']
#     ordering = ["Emp_ID"]
#     prepopulated_fields = {'slug':('Emp_ID',)}
#     add_fieldsets = (
#     (None, {
#         'classes': ('table',),
#         'fields': ('email', 'first_name', 'last_name','Emp_ID' ,'slug','password1', 'password2'),
#     }),
# )   
#     fieldsets = (
#         (None, {
#             "fields": (
#                 ('email', 'first_name', 'last_name','Emp_ID' ,'is_staff','slug')
                
#             ),
#         }),
#     )
#     inlines = (student_details_inline,)
    
# admin.site.register(User,UserAdmin)