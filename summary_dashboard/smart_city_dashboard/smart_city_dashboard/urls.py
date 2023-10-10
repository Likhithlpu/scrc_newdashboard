"""smart_city_dashboard URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import os
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import *
from django.views.generic import RedirectView

admin.site.site_header = 'Living Lab Dashboard Admin console'
admin.site.site_title = 'Living Lab Dashboard'
from django.views.generic import RedirectView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('loadmaps/', loadMapAllVerticals),
    path('graph/', getGraphData),
    path('', loadGrafanaView),
    path('home/', loadGrafanaView),
    path('building/', loadBuilding),
    path('3d/', load3D),
    # path('createallnodes/', createAllNodes),
    path('grafana_view/', RedirectView.as_view(url='/')),
    path('point_picker/', loadPointPicker),
    path('verticals/all/latest/', getAllVeriticalDataWithNodes),
    path('verticals/avg/', getVerticalsAverage),
    path('get_3d_config/', get3DConfig),
    path('save_3d_config/', save3DConfig),
    path('wisun_view/',wisunDashboard),
    path('wisun_view/switch/<command>/<id>/<data>',switchOnOff),
    path('wisun_view/get/ack/<id>',getAcknowledgement)
] 

if settings.DEBUG:  # Dev only
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

# if not os.path.exists(os.path.join(settings.BASE_DIR, 'storage')):
#     os.makedirs(os.path.join(settings.BASE_DIR, 'storage'))
