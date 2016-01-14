from django.conf.urls import include, url

from . import views

app_name = 'webinterface'
urlpatterns = [
	url(r'^$', views.Index.as_view(), name='index'),
	url(r'^register/$', views.RegisterView.as_view(), name='register'),
	url(r'^login/$', views.LoginView.as_view(), name='login'),
	url(r'^logout/$', views.LogoutView.as_view(), name='logout'),
]