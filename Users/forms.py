from django import forms
from . models import Student_details
from django.contrib.auth import get_user_model

User = get_user_model()

class Login(forms.Form):
    student_id = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Student Id'}))
    password = forms.CharField(widget =forms.PasswordInput(attrs={'placeholder': 'Password'}))

class student_main_form(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','Emp_ID','email','password']
        labels = {
           'first_name' : 'First Name',
           'last_name' : 'Last Name',
           'Emp_ID' : 'Student ID',
           'email' : 'Email',
           'password' : 'Password',

        }

class student_form(forms.ModelForm):
    confirm_password = forms.CharField(label='Confirm Password',widget =forms.PasswordInput)
    class Meta:
        widgets = {
            'password': forms.PasswordInput() ,
        }
        model = Student_details
        fields = ['department','year']
        labels = {
           'department' : 'Department',
           'year' : 'Year'
        }
    field_order = ['confirm_password','department','year']
            
        