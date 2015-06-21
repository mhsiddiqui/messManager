from datetime import datetime
from django.contrib.auth.models import User, Group
from django.forms import formset_factory
from django.forms.models import modelform_factory
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import get_object_or_404, render,render_to_response
from django.template import RequestContext, loader
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import RedirectView, View
from django.views import generic
from django.contrib import auth
from django.core.context_processors import csrf
from messManager.forms import Login, UserCreationForm, MessManagerSignUpForm, MessJoiningForm
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from messManager.models import MemberMess, Mess


def send_email(self):
    message_body = 'Hi this is email send through django application made by M Hassan Siddiqui. There is also attached an image.<img src="http://i59.tinypic.com/zv3769.png"/>'
    send_mail('Pangay', '<b>Bold Text</b>.', 'mhassan@messManager.com',
    ['mhassan.qc@gmail.com'], fail_silently=False, html_message=message_body)
    return HttpResponse('True')

@csrf_exempt
def mainPage(request):
    LoginFormset = Login
    if request.method == 'POST':
        signin_formset = LoginFormset(request.POST, request.FILES)
        if signin_formset.is_valid():
            user = authenticate(username=request.POST['username_login'], password=request.POST['password_login'])
            if user.is_active:
                login(request, user)
                request.user = user
                now = datetime.now()
                request.session['last_activity'] = now
                return HttpResponseRedirect('/admin_panel/')
            else:
                print("The password is valid, but the account has been disabled!")
    else:
        signin_formset = LoginFormset()
    return render_to_response('messManager/index.html', {
                                                         'signin_formset': signin_formset},
                              context_instance=RequestContext(request))

@csrf_exempt
def signin(request):
    LoginFormset = Login
    success_msg = ''
    error_msg = ''
    if request.method == 'POST':
        signin_formset = LoginFormset(request.POST, request.FILES)
        if signin_formset.is_valid():
            user = authenticate(username=request.POST['username_login'], password=request.POST['password_login'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    request.user = user
                    now = datetime.now()
                    request.session['last_activity'] = now
                    success_msg = 'Login Successfull'
                    return HttpResponseRedirect('/admin_panel/')
                else:
                    error_msg = 'invalid Login'
    else:
        signin_formset = LoginFormset()
    return render_to_response('messManager/signin.html', {
                                                         'signin_formset': signin_formset, 'success': success_msg,
                                                         'error': error_msg},
                              context_instance=RequestContext(request))


class SignUp(RedirectView):

    manager_signup_form = MessManagerSignUpForm
    member_signup_form = UserCreationForm
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(SignUp, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        manager_formset = self.manager_signup_form()
        member_formset = self.member_signup_form()
        return render_to_response('messManager/signup.html', {
                                                         'manager_formset': manager_formset,
                                                         'member_formset': member_formset},
                              context_instance=RequestContext(request))

    def post(self, request, *args, **kwargs):
        manager_formset = self.manager_signup_form(request.POST, request.FILES)
        member_formset = self.member_signup_form(request.POST, request.FILES)
        member_class = ''
        manager_class = ''
        if len(manager_formset.changed_data)>0:
            if manager_formset.is_valid():
                manager_formset.save()
                return HttpResponseRedirect('/signin')
            else:
                manager_class = 'active'
            member_formset = self.member_signup_form()
        if len(member_formset.changed_data)>0:
            if member_formset.is_valid():
                member_formset.save()
                return HttpResponseRedirect('/signin')
            else:
                member_class = 'active'
            manager_formset = self.manager_signup_form()
        return render_to_response('messManager/signup.html', {
                                                         'manager_formset': manager_formset,
                                                         'member_formset': member_formset,
                                                         'member_class': member_class,
                                                         'manager_class': manager_class,},
                                  context_instance=RequestContext(request))


class AdminPanel(View):

    def dispatch(self, request, *args, **kwargs):
        return super(AdminPanel, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        mess = Mess.objects.get(mess_admin=request.user)
        mess_member = MemberMess.objects.filter(mess=mess)
        return render_to_response('messManager/panel/panel_home.html',
                                    {'member': mess_member},
                                  context_instance=RequestContext(request))


class JoinMess(View):

    mess_joining_form = MessJoiningForm
    template = 'messManager/panel/join_mess.html'
    mess = None

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        try:
            self.mess = MemberMess.objects.get(user=request.user).mess.mess_name
        except MemberMess.DoesNotExist:
            pass
        return super(JoinMess, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        formset = self.mess_joining_form()
        return render_to_response(self.template, {'formset': formset, 'mess': self.mess},
                                  context_instance=RequestContext(request))

    def post(self, request, *args, **kwargs):
        formset = self.mess_joining_form(request.POST, request.FILES)
        if formset.is_valid():
            formset.save(request.user)
        return render_to_response(self.template, {'formset': formset, 'mess': self.mess},
                                  context_instance=RequestContext(request))