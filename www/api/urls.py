from django.conf.urls import url

from . import views

app_name = 'api'
urlpatterns = [
	url(r'^(?P<token>)$', views.index, name='index'),
    url(r'^(?P<token>.+)/$', views.index, name='index'),
]