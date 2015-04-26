from django.conf.urls import url

from messManager import views

urlpatterns = [
    url(r'^$', views.mainPage, name='main page'),
    url(r'^polls/$', views.IndexView.as_view(), name='index'),
    url(r'^polls/(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^polls/(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
    url(r'^polls/(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
    url(r'^accounts/login/$',views.login),
    url(r'^accounts/auth$',views.auth_view),
    url(r'^accounts/logout/$',views.logout),
    url(r'^accounts/invalid/$',views.invalid_login)

]