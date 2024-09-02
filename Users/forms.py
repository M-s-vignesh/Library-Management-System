from django import forms
from . models import Student_details

class Login(forms.Form):
    student_id = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Student Id'}))
    password = forms.CharField(widget =forms.PasswordInput(attrs={'placeholder': 'Password'}))

class student_form(forms.ModelForm):
    confirm_password = forms.CharField(label='Confirm Password',widget =forms.PasswordInput)
    class Meta:
        model = Student_details
        fields = ['name','email','department','student_id','password']
        label = {
           'name': 'Name' ,
           'email': 'Email',
           'department' : 'Department',
           'student_id' : 'Student ID',
           'password' : 'Password'
        }
        widgets = {
            'password': forms.PasswordInput() ,
        }
        