from django.forms import formset_factory
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import get_object_or_404, render,render_to_response
from django.template import RequestContext, loader
from django.views.decorators.csrf import csrf_exempt
from messManager.models import Question,Choice
from django.views import generic
from django.contrib import auth
from django.core.context_processors import csrf
from messManager.forms import UserCreationForm, Login


def login(request):
    c = {}
    c.update(csrf(request))
    return render_to_response('messManager/login.html', c)

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

@csrf_exempt
def mainPage(request):
    UserCreationFormset= UserCreationForm
    LoginFormset = Login
    if request.method == 'POST':
        signup_formset = UserCreationFormset(request.POST, request.FILES)
        signin_formset = LoginFormset(request.POST, request.FILES)
        if signup_formset.is_valid():
            # do something with the formset.cleaned_data
            pass
        if signin_formset.is_valid():
            pass
    else:
        signup_formset = UserCreationFormset()
        signin_formset = LoginFormset()
    return render_to_response('messManager/index.html', {'signup_formset': signup_formset,
                                                         'signin_formset': signin_formset},
                              context_instance=RequestContext(request))
