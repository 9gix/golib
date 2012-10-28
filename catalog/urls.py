from django.conf.urls.defaults import *
from catalog.models import Book, BookOwner
from catalog.forms import BookOwnerForm
from catalog.views import BookUpdateView


urlpatterns = patterns('catalog.views',
    url(r'^view/(?P<isbn>(\d-?){9}(\d|X|x)|(\d-?){13})/$', 'book_details',
        name='book_details'),
    url(r'^view/(?P<slug>[\w-]+)/$', 'book_details',
        name='book_details'),
    url(r'^update/(?P<pk>\d+)/$', BookUpdateView.as_view(),
        name='book_update'),
    url(r'^add/$', 'book_add',
        name='book_add'),
    url(r'^shelf/$', 'bookshelf',
        name='bookshelf'),
    url(r'^borrow/(?P<book_owner_id>(\d+))/$', 'notify_owner',
        name='notify_owner'),
    url(r'^$','book_list',
        name='book_list'),
)
