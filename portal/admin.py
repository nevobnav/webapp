from django.contrib import admin
from .models import Plot, Scan, Customer
from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin

class CustomLeafletGeoAdmin(LeafletGeoAdmin):
    settings_overrides = {
       'DEFAULT_CENTER': (51.9951071, 5.26033378),
       'DEFAULT_ZOOM': 8,
       'ATTRIBUTION_PREFIX': 'VanBoven',
       'TILES': [
            # base layers by preference
            # ('OSM', 'https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', 'Google Satellite'),
            ('GM', 'https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', 'Google Satellite'),
            ('OSM', 'http://tile.openstreetmap.org/{z}/{x}/{y}.png', 'OpenStreetMap'),
            ('AG', 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}', 'ArgGIS'),
            # ('AAN', 'https://geodata.nationaalgeoregister.nl/tiles/service/tms/1.0.0/aan/EPSG:28992/{z}/{y}/{x}.png', 'AAN')
        ]
    }

admin.site.register(Plot,CustomLeafletGeoAdmin)
admin.site.register(Scan)
admin.site.register(Customer)


#Overview of map tiles: https://www.spatialbias.com/2018/02/qgis-3.0-xyz-tile-layers/
