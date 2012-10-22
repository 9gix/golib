from django import forms
from registration.forms import RegistrationFormUniqueEmail

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
