from django import forms
from catalog.models import Book, BookOwner, validate_isbn
from django.forms.widgets import HiddenInput
from django.forms.models import fields_for_model
from catalog.book import search_and_save_to_db
from django.core.exceptions import ValidationError


class BookModelForm(forms.ModelForm):
    class Meta:
        model = Book

    def clean_isbn(self):
        return self.cleaned_data['isbn'] or None

class BookOwnerForm(forms.ModelForm):
    isbn = forms.CharField(label="ISBN", max_length=20, required=False)
    title = forms.CharField(label="Title", max_length=150, required=False)

    class Meta:
        model = BookOwner
        exclude = ('owner', 'book',)
        fields = ['isbn','title','availability','condition']

    def clean(self):
        title = self.cleaned_data.get('title')
        isbn = self.cleaned_data.get('isbn')
        if isbn:
            isbn = isbn.replace("-", "").replace(" ", "").upper();
            validate_isbn(isbn)
            try:
                book = Book.objects.get(isbn=isbn)
            except Book.DoesNotExist:
                book = search_and_save_to_db(isbn)

            if not book:
                raise ValidationError("We couldn't find your book")
        elif title:
            book = Book.objects.create(title=title)
        else:
            raise ValidationError("What book do you have?")

        self.instance.book = book
        return self.cleaned_data

