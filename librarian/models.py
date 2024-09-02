from django.db import models
from django.urls import reverse
from django.core.validators import MaxValueValidator,MinValueValidator
# Create your models here.
class Librarian(models.Model):
    name = models.CharField(max_length=255,null=False)
    email = models.EmailField(unique=True,null=False)
    employee_id = models.IntegerField(unique=True,null=False)
    address = models.TextField(blank=True)
    mobile_no = models.IntegerField(max_length=10,unique=True,null=False,validators=[MinValueValidator(1000000000),MaxValueValidator(9999999999)])
    password = models.CharField(null=False,max_length=50)
    slug = models.SlugField(unique=True,null=False)

    def get_absolute_url(self):
        return reverse("librarian", kwargs={"slug": self.slug})
