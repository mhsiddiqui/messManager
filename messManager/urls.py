from django.conf.urls import patterns, include, url

from messManager import views

urlpatterns = [
    url(r'^$', views.mainPage, name='main page'),
    url(r'^sendemail/$',views.send_email),
    url(r'^signup/$', views.SignUp.as_view()),
    url(r'^signin/$', views.signin, name='signin'),
    url(r'^admin_panel/$', views.AdminPanel.as_view()),
    url(r'^join_mess/$', views.JoinMess.as_view(), name='messManager_join_mess')
]