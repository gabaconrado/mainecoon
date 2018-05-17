'''
xScratch form models
'''
from django import forms
from django.contrib.auth.models import User


class SignUpForm(forms.ModelForm):
    '''
    The user sign up form
    '''
    class Meta:
        '''
        Meta information about the class form
        @model User user: The usar model defined in django authentication
        @field str username: The user's username
        @field str password: The user's password
        @field str first_name: The user's first name
        @field str last_name: The user's last name
        @field str email: The user's email
        '''
        model = User
        fields = [
            'username', 'first_name', 'last_name', 'email', 'password'
        ]
        widgets = {
            'password': forms.PasswordInput(),
        }


class SignInForm(forms.Form):
    '''
    The user sign in form
    @field str username: The user's username
    @field str password: The user's password
    '''
    username = forms.CharField(label='username', max_length=50)
    password = forms.CharField(label='password', max_length=20, widget=forms.PasswordInput)
