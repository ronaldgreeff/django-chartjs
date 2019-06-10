from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework.routers import DefaultRouter

from charts import views

router = DefaultRouter()
router.get_api_root_view().cls.__doc__ = 'Main title'
# router.register(r'', views.DataSetViewSet, basename='datasets')
router.register(r'', views.ChartViewSet, basename='datasets')

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'data/', include(router.urls)),
    re_path(r'^$', views.AdminGraphView.as_view(), name='graph'),
]