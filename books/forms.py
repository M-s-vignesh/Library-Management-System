from django import forms
from .models import Books,book_code
from django.forms.widgets import DateInput
from django.db.models import F,Q
from dal import autocomplete



class AddBook(forms.ModelForm):
    class Meta:
        model = Books
        fields = ['title','author','published_date','no_of_copies','current_copies']
        widgets = {
            'published_date': DateInput(attrs={'type': 'date'}),
        }

class AddBookCode(forms.Form):
    code_no = forms.IntegerField()
    book = forms.ModelChoiceField(queryset=Books.objects.all(),widget = autocomplete.Select2(
                                         url='BookComplete',
                                         attrs={'class' : 'form-control'}
                                )
                             )

