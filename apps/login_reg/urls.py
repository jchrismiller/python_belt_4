from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index),
	url(r'^login$', views.login),
	url(r'^logout$', views.index),
	url(r'^registration$', views.registration),
	url(r'^appointments$', views.appointments),
	url(r'^add$', views.add),
	url(r'^edit/(P?\d+)$', views.edit),
	url(r'^update/(P?\d+)$', views.update),
	url(r'^delete/(P?\d+)$', views.delete)
]