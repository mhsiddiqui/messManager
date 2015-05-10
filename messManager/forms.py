from django.contrib.auth.models import User
from django import forms

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserCreationForm(forms.Form):
    first_name = forms.CharField(label='First Name')
    last_name = forms.CharField(label='Last Name')
    user_name = forms.CharField(label='Username')
    password = forms.CharField(widget=forms.PasswordInput(), label='Password')
    email = forms.EmailField(label='Email id')

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'class' : 'form-control', 'placeholder': 'First Name'})
        self.fields['last_name'].widget.attrs.update({'class' : 'form-control', 'placeholder': 'Last Name'})
        self.fields['user_name'].widget.attrs.update({'class' : 'form-control', 'placeholder': 'Username'})
        self.fields['password'].widget.attrs.update({'class' : 'form-control', 'placeholder': 'Password'})
        self.fields['email'].widget.attrs.update({'class' : 'form-control', 'placeholder': 'Email ID'})

    def save(self):

        username = self.cleaned_data['user_name']
        fname = self.cleaned_data['first_name']
        lname = self.cleaned_data['last_name']
        email = self.cleaned_data['email']
        passwrd = self.cleaned_data['password']
        user = User(username=username, first_name=fname, last_name=lname, email=email, password=passwrd)
        user.save()

class Login(forms.Form):

    username_login = forms.CharField(label='Username')
    password_login = forms.CharField(widget=forms.PasswordInput(), label='Password')


    def __init__(self, *args, **kwargs):
        super(Login, self).__init__(*args, **kwargs)
        self.fields['username_login'].widget.attrs.update({'class' : 'validate'})
        self.fields['password_login'].widget.attrs.update({'class' : 'validate'})
