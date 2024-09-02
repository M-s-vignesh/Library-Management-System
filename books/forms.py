from django import forms
from .models import Books,book_code
from django.forms.widgets import DateInput
from django.db.models import F,Q


class AddBook(forms.ModelForm):
    class Meta:
        model = Books
        fields = ['title','author','published_date','no_of_copies','current_copies']
        widgets = {
            'published_date': DateInput(attrs={'type': 'date'}),
        }

class AddBookCode(forms.ModelForm):
    class Meta:
        model = book_code
        fields = ['code_no','book']
    def __init__(self, *args, **kwargs):
        super(AddBookCode, self).__init__(*args, **kwargs)
        if self.instance:
            self.fields['book'].queryset = Books.objects.filter(coded_books__lt = F('no_of_copies'))

   
   