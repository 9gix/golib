from django import forms
from catalog.models import Book, BookOwner, validate_isbn
from django.forms.widgets import HiddenInput
from catalog.book import search_and_save_to_db
from django.core.exceptions import ValidationError


class BookModelForm(forms.ModelForm):
    class Meta:
        model = Book

    def clean_isbn(self):
        return self.cleaned_data['isbn'] or None

class BookOwnerForm(forms.ModelForm):
    isbn = forms.CharField(label="ISBN", max_length=20, required=False)

    class Meta:
        model = BookOwner
        exclude = ('owner', 'book',)
        fields = ['isbn','availability','condition']

    def clean_isbn(self):
        isbn = self.cleaned_data.get('isbn')
        if not isbn:
            raise ValidationError("Please enter your book ISBN")
        isbn = isbn.replace("-", "").replace(" ", "").upper();
        validate_isbn(isbn)
        try:
            book = Book.objects.get(isbn=isbn)
        except Book.DoesNotExist:
            book = search_and_save_to_db(isbn)

        if not book:
            raise ValidationError("We couldn't find your book")

        self.instance.book = book
        return book
