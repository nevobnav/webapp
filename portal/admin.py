from django.contrib import admin
from .models import Plot, Scan, Customer
from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin

class CustomLeafletGeoAdmin(LeafletGeoAdmin):
    settings_overrides = {
       'DEFAULT_CENTER': (51.9951071, 5.26033378),
       'DEFAULT_ZOOM': 8,
       'MINIMAP': True,

    }

admin.site.register(Plot,CustomLeafletGeoAdmin)
admin.site.register(Scan)
admin.site.register(Customer)
