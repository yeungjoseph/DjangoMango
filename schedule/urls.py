from django.urls import re_path
from . import views


app_name = 'schedule'
urlpatterns = [
	re_path(r'^$', views.task_list, name='task_list'),
	re_path(r'^new/$', views.task_add, name='task_add'),
	re_path(r'^(?P<pk>\d+)/edit/$', views.task_edit, name='task_edit'),
	re_path(r'^(?P<pk>\d+)/remove/$', views.task_remove, name='task_remove'),
]