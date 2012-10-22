from django import forms
from registration.forms import RegistrationFormUniqueEmail
from accounts.models import UserProfile

class UserRegistrationForm(RegistrationFormUniqueEmail):
    first_name = forms.CharField()
    last_name = forms.CharField(required=False)
    address = forms.CharField(
            required=False,
            widget=forms.Textarea,
            help_text="The book collection address or meetup point")
    contact = forms.CharField(
            required=False,
            help_text="Receive a call from the borrower directly")

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.fields.keyOrder = [
                'first_name', 'last_name',
                'email', 'username',
                'password1','password2',
                'contact','address']

class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(label='First Name', max_length=30)
    last_name = forms.CharField(label='Last Name', max_length=30, 
            required=False)
    address = forms.CharField(
            required=False,
            widget=forms.Textarea,
            help_text="The book collection address or meetup point")
    contact = forms.CharField(
            required=False,
            help_text="Receive a call from the borrower directly")

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].initial = self.instance.user.first_name
        self.fields['last_name'].initial = self.instance.user.last_name

        self.fields.keyOrder = [
                'first_name', 'last_name',
                'contact','address']

    def save(self, *args, **kw):
        super(UserProfileForm, self).save(*args, **kw)
        self.instance.user.first_name = self.cleaned_data.get('first_name')
        self.instance.user.last_name = self.cleaned_data.get('last_name')
        self.instance.user.save()

    class Meta:
        model = UserProfile

