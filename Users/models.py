from django.db import models
from django.urls import reverse
from django.utils.text import slugify 
from django.core.validators import MaxValueValidator,MinValueValidator
from django.contrib.auth import get_user_model

User = get_user_model()
# # Create your models here.
class Student_details(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    department = models.CharField(max_length=255,null=False)
    year = models.IntegerField(null=False,validators=[MinValueValidator(1),MaxValueValidator(4)])
    
    def __str__(self):
        return str(self.user.Emp_ID)
    
    def get_url(self):
        return reverse("student_page", kwargs={"slug": self.user.slug})

@classmethod
def model_field_exists(cls, field):
    try:
        cls._meta.get_field(field)
        return True
    except models.FieldDoesNotExist:
        return False

models.Model.field_exists = model_field_exists
