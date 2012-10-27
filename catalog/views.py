from django.shortcuts import render, get_object_or_404
from catalog.models import Book, BookOwner
from catalog.forms import BookOwnerForm
from django.shortcuts import redirect, render
from django.core.urlresolvers import reverse
from django.db.models import Count



def book_details(request, isbn=None, slug=None, template_name='catalog/book_detail.html'):
    if isbn:
        isbn = isbn.replace("-", "").replace(" ", "").upper();
        book = get_object_or_404(Book, isbn=isbn)
    elif slug:
        book = get_object_or_404(Book, slug=slug)
    return render(request, template_name, locals())

def book_add(request):
    if request.method == 'POST':
        book_owner = BookOwner(owner=request.user)
        form = BookOwnerForm(request.POST, instance=book_owner)
        if form.is_valid():
            form.save()
            return redirect(reverse('catalog:book_list'))
    else:
        form = BookOwnerForm()
    return render(request, 'catalog/book_add.html', locals())

def book_list(request, template_name='catalog/book_list.html'):
    books = Book.objects.annotate(Count('owners')).filter(owners__count__gt=0)
    form = BookOwnerForm()
    return render(request, template_name, locals())
