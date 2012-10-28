from django.conf.urls.defaults import *
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from catalog.models import Book
from catalog.forms import BookOwnerForm

urlpatterns = patterns('catalog.views',
    url(r'^view/(?P<isbn>(\d-?){9}(\d|X|x)|(\d-?){13})/$', 'book_details',
        name='book_details'),
    url(r'^view/(?P<slug>[\w-]+)/$', 'book_details',
        name='book_details'),
    url(r'^add/$', 'book_add',
        name='book_add'),
    url(r'^borrow/(?P<book_owner_id>(\d+))/$', 'notify_owner',
        name='notify_owner'),
    url(r'^$','book_list',
        name='book_list'),
)
