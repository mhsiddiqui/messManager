from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^', include('messManager.urls', namespace="messManager")),
    url(r'^admin/', include(admin.site.urls)),
]