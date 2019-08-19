from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.sessions.models import Session
from django.http import HttpResponse
from django.utils.html import strip_tags
from django.utils.text import normalize_newlines

from .models import Plot,Scan,Customer, Parent_Plot, MapNote, Datalayer
from .forms import MapNoteForm
from geoalchemy2.shape import to_shape
import shapely
import datetime
import os



def home(request):
    return render(request, 'portal/home.html', context={})

def add_note(request):
    name = request.GET.get('name')
    name_sanitized = strip_tags(name)

    note = request.GET.get('note')
    normalized_note = normalize_newlines(note)
    note_text_sanitized = normalized_note.replace('\n',' ')

    lat = request.GET.get('lat')
    lon = request.GET.get('lon')
    scan_id = request.GET.get('scan_id')
    scan = Scan.objects.get(id=int(scan_id))
    time = datetime.datetime.now()

    MapNote.objects.create(
        name = name_sanitized,
        note = note_text_sanitized,
        lat = lat,
        lon = lon,
        scan_id = scan_id
    )
    return render(request, 'portal/about.html')


@login_required(login_url='/login/')
def map(request, map_id):
    user = request.user

    # Get the right plot
    this_parent_plot = Parent_Plot.objects.get(id=map_id)
    this_plot = this_parent_plot.get_plot()

    #Fetch the corresponding scans
    scans = Scan.objects.filter(plot=this_plot).order_by('date')
    scan_ids = []

    #Determine if any scans are new, if so mark as seen
    new_scans = []
    for scan in scans:
        scan_ids.append(scan.pk)
        if scan.seen_by_user is False:
            new_scans.append(scan)

    for new_scan in new_scans:
        if user.customer.pk == this_parent_plot.customer_id:
            new_scan.seen_by_user = True
            new_scan.save()

    #All required for MapNotes:
    mapnotes = MapNote.objects.filter(scan_id__in=scan_ids)

    #Adding form to add map notes
    if request.method == 'POST':
        form = MapNoteForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = MapNoteForm()


    # Fetch shape boundaries for red line on map
    coords = this_plot.shape.coords[0] #Get coordinate tuple
    rev_coords = [(y, x) for x, y in coords] #Reverse lat/long
    plot_polygon_latlong = str(list(rev_coords)).replace('(','[').replace(')',']') #Create JavaScript latlong line


    #Get all data_layers corresponding to this map
    data_layers = Datalayer.objects.filter(scan_id__in=scan_ids)
    data_layer_list = []
    for dl in data_layers:
        data_values = [x['properties'][dl.property_name] for x in dl.data['features']]
        max_val = max(data_values)
        min_val = min(data_values)
        dl_dict = {'datalayer_id': 'datalayer{}'.format(str(dl.pk)),'scan_id': dl.scan_id, 'property_name': dl.property_name,'layer_name':dl.layer_name,  'data': dl.data,
             'max_val': max_val, 'min_val':min_val, 'legend_title':dl.legend_title, 'legend_unit':dl.legend_unit}
        data_layer_list.append(dl_dict)


    if user.customer.pk == this_parent_plot.customer_id or user.is_staff:
        context = {
        'map_id' : map_id,
        'this_parent_plot': this_parent_plot,
        'this_plot' : this_plot,
        'latlong': plot_polygon_latlong,
        'scans' : scans,
        'mapnotes': mapnotes,
        'form' : form,
        'data_layers': data_layer_list,
        }
        return render(request, 'portal/map.html', context=context)
    else:
        return redirect('portal-home')

@login_required(login_url='/login/')
def user_profile(request):
    user = request.user
    parent_plots = user.customer.get_all_parent_plots()
    acreage = 0
    for parent_plot in parent_plots:
        plot = parent_plot.get_plot()
        acreage += plot.area
    context = {
    'acreage': acreage,
    }
    return render(request,'portal/user_profile.html', context=context)


def about(request):
    return render(request, 'portal/about.html')

def test(request):
    return render(request, 'portal/test.html')
