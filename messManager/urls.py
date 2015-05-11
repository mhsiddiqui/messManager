from django.conf.urls import url

from messManager import views

urlpatterns = [
    url(r'^$', views.mainPage, name='main page'),
    url(r'^polls/$', views.IndexView.as_view(), name='index'),
    url(r'^polls/(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^polls/(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
    url(r'^polls/(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {"next_page":"/"}, name="logout"),
    url(r'^accounts/invalid/$',views.invalid_login),
    url(r'^sendemail/$',views.send_email),
    url(r'^signup/$', views.SignUp.as_view()),
    url(r'^signup/$', views.signin, name='signin')

]