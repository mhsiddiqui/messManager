from django.contrib.auth.models import User, Group, UserManager
from django import forms
from django.forms import ModelForm
from models import Mess

class MessManagerSignUpForm(forms.Form):
    mess_name = forms.CharField(label='Mess Name')
    institute_name = forms.CharField(label='Institute/Company Name')
    mm_first_name = forms.CharField(label='Administrator/Manager First Name')
    mm_last_name = forms.CharField(label='Administrator/Manager Last Name')
    mm_user_name = forms.CharField(label='Administrator/Manager Username')
    mm_password = forms.CharField(widget=forms.PasswordInput(), label='Password')
    mm_email = forms.EmailField(label='Email id')

    def __init__(self, *args, **kwargs):
        super(MessManagerSignUpForm, self).__init__(*args, **kwargs)
        self.fields['mess_name'].widget.attrs.update({'class' : 'validate'})
        self.fields['mess_name'].help_text = 'Name of Mess e.g. ABC Mess'
        self.fields['institute_name'].widget.attrs.update({'class' : 'validate'})
        self.fields['institute_name'].help_text = 'Name of Company or University/Institute e.g. ABC Company/University'
        self.fields['mm_first_name'].help_text = 'Name of Person who will manage the mess'
        self.fields['mm_last_name'].help_text = 'Name of Person who will manage the mess'
        self.fields['mm_first_name'].widget.attrs.update({'class' : 'validate'})
        self.fields['mm_last_name'].widget.attrs.update({'class' : 'validate'})
        self.fields['mm_password'].widget.attrs.update({'class' : 'validate'})
        self.fields['mm_email'].widget.attrs.update({'class' : 'validate'})

    def save(self):
        first_name = self.cleaned_data['mm_first_name']
        last_name = self.cleaned_data['mm_last_name']
        user_name = self.cleaned_data['mm_user_name']
        email_id= self.cleaned_data['mm_email']
        mess_name = self.cleaned_data['mess_name']
        istitute_name = self.cleaned_data['institute_name']
        password = self.cleaned_data['mm_password']
        user = User(username=user_name, first_name=first_name, last_name=last_name, email=email_id)
        user.set_password(password)
        user.save()
        new_mess = Mess(mess_name=mess_name, institute_name=istitute_name, mess_admin=user)
        new_mess.save()

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
        is_staff = False
        if str(user_type.name) == 'Administrator':
            is_staff = True
        user = User(username=username, first_name=fname, last_name=lname, email=email, is_staff=is_staff)
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
