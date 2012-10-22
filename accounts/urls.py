from django.conf.urls.defaults import *
from accounts.forms import UserRegistrationForm
from registration.views import register

urlpatterns = patterns('accounts.views',
        url(r'^register/$', register,
            {'backend':'registration.backends.default.DefaultBackend',
                'form_class':UserRegistrationForm}),
        url(r'', include('registration.backends.default.urls')),
)
