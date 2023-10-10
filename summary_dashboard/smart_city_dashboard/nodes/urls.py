from django.urls import path
from .views import load_map_view

urlpatterns = [
    path(r'^dashboard/$', load_map_view, name='grafana_view'),
]