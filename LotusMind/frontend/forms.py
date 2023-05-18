from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from Lotus.models import Usuario

class RegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'my-custom-class'}), required=True)
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'email-custom-class'}), required=True)
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'my-custom-class'}), required=True)
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'my-custom-class'}),required=True)

    class Meta:
        model = Usuario
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user