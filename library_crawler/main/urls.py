from django.conf.urls import url
from . import views


urlpatterns = [
	url(r'^$', views.main),
	url(r'^(?P<room>\d{1})/$', views.main),
	url(r'^(?P<date>\d{4,8})/$', views.main),
	url(r'^(?P<room>\d{1})/(?P<date>\d{4,8})/$', views.main),
	url(r'^(?P<date>\d{4,8})/(?P<room>\d{1})/$', views.main),
]
