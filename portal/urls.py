from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name = 'portal-home'),
    path('test/',views.test, name='portal-test'),
    path('about/', views.about, name = 'portal-about'),
    path('map/<int:map_id>/', views.map, name = 'portal-map'),
]
