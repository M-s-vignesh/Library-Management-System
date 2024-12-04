from django.db import models
from django.urls import reverse
from django.core.validators import MaxValueValidator,MinValueValidator
from django.contrib.auth.models import AbstractBaseUser,AbstractUser,BaseUserManager,PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.template.defaultfilters import slugify


class UserManager(BaseUserManager):
    use_in_migrations = True
    def _create_user(self, email,Emp_ID, password=None, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        if not Emp_ID:
            raise ValueError("Id must be set")
        email = self.normalize_email(email)
        user = self.model(Emp_ID=Emp_ID,email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email,Emp_ID, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email,Emp_ID, password, **extra_fields)
        

    def create_superuser(self, email,Emp_ID, password=None, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email,Emp_ID,password, **extra_fields)

class User(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField( unique=True)
    first_name = models.CharField( max_length=30, blank=True)
    last_name = models.CharField( max_length=30, blank=True)
    Emp_ID = models.CharField( max_length=30, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    slug = models.SlugField(unique=True,null=False)

    USERNAME_FIELD = 'Emp_ID'
    REQUIRED_FIELDS = ['email']
    objects = UserManager()

    def get_absolute_url(self):
        return reverse("librarian", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.Emp_ID)
        return super().save(*args, **kwargs)

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)

   

# Create your models here.
class Librarian_Profile(models.Model):
    address = models.TextField(blank=True)
    mobile_no = models.IntegerField(max_length=10,unique=True,null=False,validators=[MinValueValidator(1000000000),MaxValueValidator(9999999999)])
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    def get_absolute_url(self):
        return reverse("librarian", kwargs={"slug": self.slug})
    def __str__(self):
        return self.user.Emp_ID
        
    # @receiver(post_save, sender=User)
    # def create_user_profile(sender, instance, created, **kwargs):
    #     if created:
    #         Librarian_Profile.objects.create(user=instance)

    # @receiver(post_save, sender=User)
    # def save_user_profile(sender, instance, **kwargs):
    #     instance.librarian_profile.save()

