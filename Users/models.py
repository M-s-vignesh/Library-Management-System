from django.db import models
from django.urls import reverse
from django.utils.text import slugify 


# Create your models here.
class Student_details(models.Model):
    name = models.CharField(max_length=255,null=False)
    email = models.EmailField(unique=True,null=False)
    student_id = models.IntegerField(unique=True,null=False)
    department = models.CharField(max_length=255,null=False)
    password = models.CharField(null=False,max_length=50)
    slug = models.SlugField(null=False,unique = True)
    def __str__(self):
        return str(self.student_id)
    
    def get_absolute_url(self):
        return reverse("student_page", kwargs={"slug": self.slug})
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name+'-'+str(self.student_id)+'-'+self.department)
        super(Student_details, self).save(*args, **kwargs)