from django import forms
from books.models import Books,book_code
from django.db.models import F,Q

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