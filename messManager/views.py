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
from messManager.models import Question,Choice
from django.views import generic
from django.contrib import auth
from django.core.context_processors import csrf
from messManager.forms import Login, UserCreationForm
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail


def auth_view(request):
    username = request.POST.get('username','')
    password = request.POST.get('password','')
    user = auth.authenticate(username=username,password=password)
    if user is not None:
        auth.login(request,user)
        return HttpResponseRedirect('/polls')
    else:
        return HttpResponseRedirect('/accounts/invalid/')

def invalid_login(request):
    invalid_login = True
    dic = {'invalid_login':invalid_login}
    return render_to_response('messManager/login.html',dic)

def logout(request):
    return HttpResponse('Logged Out')


class IndexView(generic.ListView):
    template_name = 'messManager/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'messManager/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'messManager/results.html'

def vote(request, question_id):
    p = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'messManager/detail.html', {
            'question': p,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('messManager:results', args=(p.id,)))

def mainPage(self):
    return HttpResponseRedirect('/polls')

def send_email(self):
    message_body = 'Hi this is email send through django application made by M Hassan Siddiqui. There is also attached an image.<img src="http://i59.tinypic.com/zv3769.png"/>'
    send_mail('Pangay', '<b>Bold Text</b>.', 'mhassan.eeng@gmail.com',
    ['basit.qc@gmail.com','mhassan.qc@gmail.com'], fail_silently=False, html_message=message_body)
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

    signup_form = UserCreationForm
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(SignUp, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        formset = self.signup_form()
        return render_to_response('messManager/signup.html', {
                                                         'formset': formset},
                              context_instance=RequestContext(request))

    def post(self, request, *args, **kwargs):
        formset = self.signup_form(request.POST, request.FILES)
        if formset.is_valid():
            formset.save()
            return HttpResponseRedirect('/signin')
            
        return render_to_response('messManager/signup.html', {
                                                         'formset': formset},
                              context_instance=RequestContext(request))


class AdminPanel(View):

    def dispatch(self, request, *args, **kwargs):
        return super(AdminPanel, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render_to_response('messManager/panel/panel_home.html',
                                    {'Corporation_Name': 'Django'},
                                  context_instance=RequestContext(request))