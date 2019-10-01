from django.conf.urls import include, url
from . import views

app_name = 'refs'
urlpatterns = [
    url(r'^$', views.ref_list, name='ref_list'),
    url(r'^resolve/(?:(?P<pk>\d+))?$', views.resolve, name='resolve'),
    url(r'^delete/(?P<pk>\d+)$', views.delete, name='delete'),
    url(r'^edit/(?:(?P<pk>\d+))?$', views.edit, name='edit'),
]
