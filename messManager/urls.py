from django.conf.urls import url

from messManager import views

urlpatterns = [
    url(r'^$', views.mainPage, name='main page'),
    url(r'^sendemail/$',views.send_email),
    url(r'^signup/$', views.SignUp.as_view()),
    url(r'^signin/$', views.signin, name='signin'),
    url(r'^admin_panel/$', views.AdminPanel.as_view()),
]