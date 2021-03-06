from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name = 'portal-home'),
    path('test/',views.test, name='portal-test'),
    path('about/', views.about, name = 'portal-about'),
    path('map/<int:map_id>/', views.map, name = 'portal-map'),
    path('user/',views.user_profile,name='portal-user-profile'),
    path('ajax/add_note/',views.add_note, name='portal-add-note')
]
