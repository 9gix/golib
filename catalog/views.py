from django.shortcuts import render, get_object_or_404
from catalog.models import Book

def book_details(request, book_id, template_name='catalog/book_detail.html'):
    book = get_object_or_404(Book, id=book_id)
    return render(request, template_name, locals())

def book_list(request, template_name='catalog/book_list.html'):
    books = Book.objects.all()
    return render(request, template_name, locals())
