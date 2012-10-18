from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^book/', include('catalog.urls', namespace='catalog')),
    url(r'^$', 'booku.views.index'),
)
