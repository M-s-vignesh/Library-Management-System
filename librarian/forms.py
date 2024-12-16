from django import forms
from books.models import Books,book_code,loaned_books
from Users.models import Student_details
from django.db.models import F,Q,Subquery
from dal import autocomplete


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
