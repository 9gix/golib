from django.conf.urls.defaults import *
from accounts.forms import UserRegistrationForm, UserProfileForm
from registration.views import register

urlpatterns = patterns('',
        url(r'^register/$', register,
            {'backend':'registration.backends.default.DefaultBackend',
                'form_class':UserRegistrationForm}),
        url(r'', include('registration.backends.default.urls')),
        url(r'^edit/', 'profiles.views.edit_profile',{'form_class':UserProfileForm}),
        url(r'', include('profiles.urls')),
)
