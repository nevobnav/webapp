from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.sessions.models import Session
from django.http import HttpResponse
from django.utils.html import strip_tags
from django.utils.text import normalize_newlines

from .models import Plot,Scan,Customer, Parent_Plot, MapNote
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
    # this_plot =  Plot.objects.get(id=map_id)
    this_parent_plot = Parent_Plot.objects.get(id=map_id)
    this_plot = this_parent_plot.get_plot()
    scans = Scan.objects.filter(plot=this_plot).order_by('date')
    scan_ids = []
    new_scans = []
    for scan in scans:
        scan_ids.append(scan.pk)
        if scan.seen_by_user is False:
            new_scans.append(scan)

    for new_scan in new_scans:
        if user.customer.pk == this_parent_plot.customer_id:
            new_scan.seen_by_user = True
            new_scan.save()

    print(scan_ids)

    mapnotes = MapNote.objects.filter(scan_id__in=scan_ids)
    print(mapnotes)

    # #Generating langlong list of polygon shape
    coords = this_plot.shape.coords[0] #Get coordinate tuple
    rev_coords = [(y, x) for x, y in coords] #Reverse lat/long
    plot_polygon_latlong = str(list(rev_coords)).replace('(','[').replace(')',']') #Create JavaScript latlong line

    #Adding form to add map notes
    if request.method == 'POST':
        form = MapNoteForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = MapNoteForm()


    if user.customer.pk == this_parent_plot.customer_id or user.is_staff:
        context = {
        'map_id' : map_id,
        'this_parent_plot': this_parent_plot,
        'this_plot' : this_plot,
        'latlong': plot_polygon_latlong,
        'scans' : scans,
        'mapnotes': mapnotes,
        'form' : form,

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
