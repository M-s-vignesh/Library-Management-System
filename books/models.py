from django.db import models
from Users.models import Student_details
from django.db.models import F,Q
# Create your models here.


class Books(models.Model):
    title = models.CharField(max_length=255,null=False,unique=True)
    author = models.CharField(max_length=255,null=False)
    published_date = models.DateField()
    no_of_copies = models.IntegerField(default=5)
    current_copies = models.IntegerField(default=5)
    coded_books = models.IntegerField(default = 0)
    studentname = models.ManyToManyField(Student_details,related_name='students')

    def __str__(self):
         return self.title
  
  
class book_code(models.Model):
    code_no = models.IntegerField(unique=True)
    book = models.ForeignKey(Books,on_delete=models.CASCADE)
    loaned = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.code_no)


    

    