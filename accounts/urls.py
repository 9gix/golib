from django.conf.urls.defaults import *
from accounts.forms import UserRegistrationForm, UserProfileForm

urlpatterns = patterns('',
        url(r'^register/$', 'registration.views.register',
            {'backend':'registration.backends.default.DefaultBackend',
            'form_class':UserRegistrationForm}),
        url(r'^edit/', 'profiles.views.edit_profile',
            {'form_class':UserProfileForm}),
        url(r'', include('registration.backends.default.urls')),
        url(r'', include('profiles.urls')),
)
