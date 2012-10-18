from django.conf.urls.defaults import *

urlpatterns = patterns('catalog.views',
    url(r'^(?P<book_id>\d+)$', 'book_details',
        name='book_details'),
    url(r'^$','book_list',
        name='book_list'),
)
