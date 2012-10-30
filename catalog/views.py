from django.shortcuts import render, get_object_or_404
from catalog.models import Book, BookOwner
from catalog.forms import BookOwnerForm, MessageOwnerForm
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse, reverse_lazy
from django.db.models import Count
from django.contrib.sites.models import get_current_site
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required



def book_details(request, isbn=None, slug=None, template_name='catalog/book_detail.html'):
    if isbn:
        isbn = isbn.replace("-", "").replace(" ", "").upper();
        if len(isbn) == 10:
            book = get_object_or_404(Book, isbn10=isbn)
        elif len(isbn) == 13:
            book = get_object_or_404(Book, isbn13=isbn)
    elif slug:
        book = get_object_or_404(Book, slug=slug)
    book_owner_list = BookOwner.objects.filter(book=book)
    return render(request, template_name, locals())

@login_required
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

@login_required
def bookshelf(request, template_name='catalog/bookshelf.html'):
    book_owners = BookOwner.objects.filter(
            owner__username=request.user.username)
    return render(request, template_name, locals())

def book_list(request, template_name='catalog/book_list.html'):
    books = Book.objects.annotate(Count('owners')).filter(owners__count__gt=0)
    for book in books:
        book.availability = book.bookowner_set.filter(availability=True).exists()
    form = BookOwnerForm()
    return render(request, template_name, locals())

@login_required
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

class BookUpdateView(UpdateView):
    model = BookOwner
    form_class = BookOwnerForm
    template_name = 'catalog/book_update.html'
    success_url = reverse_lazy('catalog:bookshelf')
    def get_initial(self):
        data = {'isbn':self.object.book.isbn10,
                'title':self.object.book.title,
                'availability':self.object.availability,
                'condition':self.object.condition}
        return data

    def get_queryset(self):
        """Limit User to update their own data"""
        qs = super(BookUpdateView, self).get_queryset()
        return qs.filter(owner=self.request.user)

class BookDeleteView(DeleteView):
    model = BookOwner
    success_url = reverse_lazy('catalog:bookshelf')

    def get_queryset(self):
        """Limit User to delete their own data"""
        qs = super(BookDeleteView, self).get_queryset()
        return qs.filter(owner=self.request.user)
