from django.contrib.auth.models import User, Group, UserManager
from django import forms
from django.forms import ModelForm

class UserCreationForm(forms.Form):
    first_name = forms.CharField(label='First Name')
    last_name = forms.CharField(label='Last Name')
    user_name = forms.CharField(label='Username')
    password = forms.CharField(widget=forms.PasswordInput(), label='Password')
    email = forms.EmailField(label='Email id')
    user_type = forms.ModelChoiceField(queryset=Group.objects.all())

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'class' : 'validate'})
        self.fields['last_name'].widget.attrs.update({'class' : 'validate'})
        self.fields['user_name'].widget.attrs.update({'class' : 'validate'})
        self.fields['password'].widget.attrs.update({'class' : 'validate'})
        self.fields['email'].widget.attrs.update({'class' : 'validate'})
        self.fields['user_type'].widget.attrs.update({})

    def save(self):

        username = self.cleaned_data['user_name']
        fname = self.cleaned_data['first_name']
        lname = self.cleaned_data['last_name']
        email = self.cleaned_data['email']
        passwrd = self.cleaned_data['password']
        user_type = self.cleaned_data['user_type']
        user = User(username=username, first_name=fname, last_name=lname, email=email)
        user.set_password(passwrd)
        user.save()
        user_type.user_set.add(user)


class Login(forms.Form):

    username_login = forms.CharField(label='Username')
    password_login = forms.CharField(widget=forms.PasswordInput(), label='Password')


    def __init__(self, *args, **kwargs):
        super(Login, self).__init__(*args, **kwargs)
        self.fields['username_login'].widget.attrs.update({'class': 'validate', 'placeholder': 'Username'})
        self.fields['password_login'].widget.attrs.update({'class': 'validate', 'placeholder': 'Password'})
