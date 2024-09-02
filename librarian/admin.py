from django.contrib import admin
from librarian.models import Librarian
# Register your models here.
class librarian(admin.ModelAdmin):
    list_display = ['employee_id','name']
    prepopulated_fields = {"slug":('name','employee_id',)}
admin.site.register(Librarian,librarian)