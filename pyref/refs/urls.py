from django.urls import include, path, re_path
from . import views

app_name = 'refs'
urlpatterns = [
    path('', views.ref_list, name='ref_list'),
    re_path(r'^resolve/(?:(?P<pk>\d+))?$', views.resolve, name='resolve'),
    re_path(r'^delete/(?P<pk>\d+)$', views.delete, name='delete'),
    re_path(r'^edit/(?:(?P<pk>\d+))?$', views.edit, name='edit'),
]
