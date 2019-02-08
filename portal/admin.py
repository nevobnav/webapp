from django.contrib import admin
from .models import Plot, Scan
from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin



admin.site.register(Plot,LeafletGeoAdmin)
admin.site.register(Scan)
