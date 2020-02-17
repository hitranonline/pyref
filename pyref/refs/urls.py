#   Copyright 2020 Frances M. Skinner, Christian Hill
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

from django.urls import include, path, re_path
from . import views

app_name = 'refs'
urlpatterns = [
    path('', views.ref_list, name='ref_list'),
    re_path(r'^resolve/(?:(?P<pk>\d+))?$', views.resolve, name='resolve'),
    re_path(r'^delete/(?P<pk>\d+)$', views.delete, name='delete'),
    re_path(r'^edit/(?:(?P<pk>\d+))?$', views.edit, name='edit'),
]
