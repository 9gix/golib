from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings
from accounts.models import UserProfile


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^book/', include('catalog.urls', namespace='catalog')),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^profile/', include('accounts.urls')),
    url(r'^$', 'golib.views.index'),
)
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

