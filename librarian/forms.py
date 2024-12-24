from django import forms
from books.models import Books,book_code,loaned_books
from Users.models import Student_details
from django.db.models import F,Q,Subquery
from dal import autocomplete
from django.core.exceptions import ValidationError


class Login(forms.Form):
    employee_id = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Employee Id'}))
    password = forms.CharField(widget =forms.PasswordInput(attrs={'placeholder': 'Password'}))

class loan(forms.Form):
    book_title = forms.ModelChoiceField(queryset=Books.objects.filter(current_copies__gt = 0),
                                        widget = autocomplete.Select2(
                                        url='book-autocomplete',
                                        attrs={'class' : 'form-control'}
             ))
    bookcode = forms.ModelChoiceField(queryset=book_code.objects.all(),
                                      widget = autocomplete.Select2(
                                         url='book-code-autocomplete',forward=['book_title'],
                                         attrs={'class' : 'form-control'}
             ))
    student_id = forms.ModelChoiceField(queryset=Student_details.objects.values_list('user', flat= True),
                                         widget = autocomplete.Select2(
                                        url='student-id-autocomplete',
                                        attrs={'class' : 'form-control',}
             ))

class Return(forms.Form):
    student_ids = forms.ModelChoiceField(queryset=Student_details.objects.values_list('user__Emp_ID', flat= True),
                                         widget = autocomplete.Select2(
                                        url='studentid-autocomplete',
                                        attrs={'class' : 'form-control',}
            ))
    book_title = forms.ModelChoiceField(queryset=Books.objects.all(),widget = autocomplete.Select2(
                                        url='return-book-autocomplete',forward=['student_ids'],
                                        attrs={'class' : 'form-control'}
            ))

class Delete_Book(forms.Form):
    book_title = forms.ModelChoiceField(queryset=Books.objects.all(),
                                         widget = autocomplete.Select2(
                                        url='book-title-autocomplete',
                                        attrs={'class' : 'form-control',}
            ))
    
class Update_Details(forms.Form):
    first_name = forms.CharField(max_length=255, required=True)
    last_name = forms.CharField(max_length=255, required=True)
    email = forms.EmailField(max_length=255,required=True)
    mobile_no = forms.IntegerField(required=True)
    address = forms.CharField(max_length=500,required=False)

    def clean_mobile_no(self):
        mobile_no = self.cleaned_data['mobile_no']
        mobile_str = str(mobile_no)  # Convert to string for length validation

        if len(mobile_str) != 10:
            raise forms.ValidationError("Mobile number must be exactly 10 digits long.")

        return mobile_no
    
class Reset_Password(forms.Form):
    old_password = forms.CharField(max_length=128, widget=forms.PasswordInput)
    new_password = forms.CharField(max_length=128, widget=forms.PasswordInput)
    confirm_password = forms.CharField(max_length=128, widget=forms.PasswordInput)
 