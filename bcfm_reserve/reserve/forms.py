from django import forms
from django.contrib.auth.models import User
from .models import Profile


class UserForm(forms.ModelForm):
    """
    This class represents an HTML form to login and authenticate users.
    ----Fields----
    - username
    - email
    - password (widget=forms.PasswordInput())
    - first_name
    - last_name
    Author: Beve Strownlee
    """

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class':'form-control'}))

    class Meta:
        model = User
        help_texts = {
            'username':None,
        }
        fields = ( 'first_name', 'last_name', 'username', 'email', 'password',)

class EditUserForm(forms.ModelForm):
    """
    This class represents an HTML form to login and authenticate users.
    ----Fields----
    - email
    - first_name
    - last_name
    Author: Beve Strownlee
    """

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email',)

class ProfileForm(forms.ModelForm):
    """
    This class represents an HTML form to login and authenticate users.
    ----Fields----
    - phone
    Author: Beve Strownlee
    """

    class Meta:
        model = Profile
        fields = ('phone',)

class LoginForm(forms.ModelForm):
    """
    This class represents an HTML form to login and authenticate users.
    ----Fields----
    - username
    - help_texts (username): None
    - password (widget=forms.PasswordInput())
    Author: Will Sims
    """
    
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class':'form-control'}))

    class Meta:
        model = User
        help_texts = {
            'username':None,
        }
        fields = ('username', 'password',)
        