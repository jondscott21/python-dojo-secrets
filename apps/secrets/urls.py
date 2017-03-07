from django.conf.urls import url
from . import views
import re
urlpatterns = [
  url(r'^$', views.index),
  url(r'^regprocess$', views.regprocess),
  url(r'^loginprocess$', views.loginprocess),
  url(r'^secretprocess$', views.secretprocess),
  url(r'^secrets$', views.secrets),
  url(r'^delete$', views.delete),
  url(r'^likes$', views.likes),
  url(r'^logout$', views.logout),
  url(r'^popular$', views.popular),
  url(r'^.*$', views.reroute)
]