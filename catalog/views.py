from django.shortcuts import render, get_object_or_404
from catalog.models import Book, BookOwner
from catalog.forms import BookOwnerForm, MessageOwnerForm
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse
from django.db.models import Count
from django.contrib.sites.models import get_current_site
from django.core.mail import EmailMessage



def book_details(request, isbn=None, slug=None, template_name='catalog/book_detail.html'):
    if isbn:
        isbn = isbn.replace("-", "").replace(" ", "").upper();
        book = get_object_or_404(Book, isbn=isbn)
    elif slug:
        book = get_object_or_404(Book, slug=slug)
    book_owner_list = BookOwner.objects.filter(book=book)
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
    for book in books:
        book.availability = book.bookowner_set.filter(availability=True).exists()
    form = BookOwnerForm()
    return render(request, template_name, locals())

def notify_owner(request, book_owner_id=None,
        template_name='catalog/notify_owner.html'):
    book_owner = BookOwner.objects.get(id=book_owner_id)
    owner = book_owner.owner
    book = book_owner.book
    if request.method == 'POST':
        form = MessageOwnerForm(request.POST)
        if form.is_valid():
            email_message = render_to_string('catalog/borrow_message.txt', {
                'owner':owner,
                'user':request.user,
                'book': book,
                'message':form.cleaned_data['message'],
                'site':get_current_site(request)
                })
            email = EmailMessage('Book Inquiry', email_message,
                    None, (owner.email,),
                    headers = {'Reply-To': request.user.email})
            email.send()
            book_owner.availability = False
            book_owner.save()
            return redirect(book)
    else:
        form = MessageOwnerForm()
    return render(request, template_name, locals())

