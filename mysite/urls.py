from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^', include('messManager.urls', namespace="messManager")),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {"next_page":"/"}, name="logout"),
    url(r'^admin/', include(admin.site.urls)),
]