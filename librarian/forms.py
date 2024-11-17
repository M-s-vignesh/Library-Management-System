from django import forms
from books.models import Books,book_code,loaned_books
from Users.models import Student_details
from django.db.models import F,Q,Subquery


class Login(forms.Form):
    employee_id = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Employee Id'}))
    password = forms.CharField(widget =forms.PasswordInput(attrs={'placeholder': 'Password'}))

class loan(forms.Form):
    book_title = forms.ModelChoiceField(queryset=Books.objects.filter(current_copies__gt = 0),
                                        widget=forms.Select(attrs={"hx-get":'load_codes/',"hx-target":"#id_bookcode"}))          
    bookcode = forms.ModelChoiceField(queryset=book_code.objects.none())
    student_id = forms.IntegerField()
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.data:
            value = int(self.data.get('book_title'))
            self.fields['bookcode'].queryset = book_code.objects.filter(Q(book_id = value) and Q(loaned = False))

# class Return(forms.Form):
#     student_ids = forms.ModelChoiceField(queryset=Student_details.objects.values_list('student_id', flat= True),
#                                          widget=forms.Select(attrs={"hx-get":'load_books/',"hx-target":"#id_book_title"}))
#     book_title = forms.ModelChoiceField(queryset=Books.objects.none())
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         if self.data:
#             value = int(self.data.get('student_ids'))
#             Value = loaned_books.objects.filter(student_id = value )
#             books_code = book_code.objects.filter(id__in=Subquery(Value.values('student_book_code_id')))
#             val_list = Books.objects.filter(id__in=Subquery(books_code.values('book_id')))
#             self.fields['book_title'].queryset = val_list

from dal import autocomplete

from django import forms


class Return(forms.Form):
    student_ids = forms.ModelChoiceField(queryset=Student_details.objects.values_list('student_id', flat= True),
                                         widget = autocomplete.Select2(
                                        url='studentid-autocomplete',
                                        attrs={'class' : 'form-control',}
            ))
    book_title = forms.ModelChoiceField(queryset=Books.objects.all(),widget = autocomplete.Select2(
                                        url='book-title-autocomplete',forward=['student_ids'],
                                        attrs={'class' : 'form-control'}
            ))
    