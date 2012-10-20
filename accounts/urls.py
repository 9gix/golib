from django.conf.urls.defaults import *

urlpatterns = patterns('accounts.views',
    url(r'', include('registration.backends.default.urls')),
)
