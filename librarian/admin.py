from django.contrib import admin
from librarian.models import User,Librarian_Profile
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class Librarian_ProfileInline(admin.TabularInline):
    model = Librarian_Profile

class UserAdmin(BaseUserAdmin):
    list_display = ['Emp_ID']
    ordering = ["Emp_ID"]
    prepopulated_fields = {'slug':('Emp_ID',)}
    add_fieldsets = (
    (None, {
        'classes': ('wide',),
        'fields': ('email', 'first_name', 'last_name','Emp_ID' ,'slug','password1', 'password2'),
    }),
)   
    fieldsets = (
        (None, {
            "fields": (
                ('email', 'first_name', 'last_name','Emp_ID' ,'is_staff','slug')
                
            ),
        }),
    )
    inlines = (Librarian_ProfileInline,)
    

admin.site.register(User,UserAdmin)

