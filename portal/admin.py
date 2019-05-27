from django.contrib import admin
from .models import Plot, Scan, Customer, Logbook
from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin


class ScanAdmin(admin.ModelAdmin):
    model = Scan
    list_display = ['date', 'time', 'plot', 'zoomlevel','flight_altitude' ]
    admin_order_field = 'date'

class LogbookAdmin(admin.ModelAdmin):
    model = Logbook
    list_display = ['time','username','action','ip',]


class CustomLeafletGeoAdmin(LeafletGeoAdmin):
    settings_overrides = {
    #Info from https://pypi.org/project/django-leaflet/0.19.0/
       'DEFAULT_CENTER': (51.9951071, 5.26033378),
       'DEFAULT_ZOOM': 8,
       'ATTRIBUTION_PREFIX': 'VanBoven',
       'TILES': [
            # base layers by preference
            ('GM', 'https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', 'Google Satellite'),
            ('OSM', 'http://tile.openstreetmap.org/{z}/{x}/{y}.png', 'OpenStreetMap'),
            ('AG', 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}', 'ArgGIS'),
            ('LF', 'https://geodata.nationaalgeoregister.nl/luchtfoto/rgb/wmts/Actueel_ortho25/EPSG:3857/{z}/{x}/{y}.jpeg', 'Luchtfoto')
        ],
        'RESET_VIEW': False,
    }
    map_height = '800px'

admin.site.register(Plot,CustomLeafletGeoAdmin)
admin.site.register(Scan, ScanAdmin)
admin.site.register(Customer)
admin.site.register(Logbook,LogbookAdmin)




#Overview of map tiles: https://www.spatialbias.com/2018/02/qgis-3.0-xyz-tile-layers/
