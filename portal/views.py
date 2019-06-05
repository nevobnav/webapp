from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.sessions.models import Session
from django.http import HttpResponse
from .models import Plot,Scan,Customer, Parent_Plot
from geoalchemy2.shape import to_shape
import shapely



def home(request):
    return render(request, 'portal/home.html', context={})


@login_required(login_url='/login/')
def map(request, map_id):
    user = request.user
    # this_plot =  Plot.objects.get(id=map_id)
    this_parent_plot = Parent_Plot.objects.get(id=map_id)
    this_plot = this_parent_plot.get_plot()
    scans = Scan.objects.filter(plot=this_plot).order_by('date')

    # #Generating langlong list of polygon shape
    coords = this_plot.shape.coords[0] #Get coordinate tuple
    rev_coords = [(y, x) for x, y in coords] #Reverse lat/long
    plot_polygon_latlong = str(list(rev_coords)).replace('(','[').replace(')',']') #Create JavaScript latlong line


    if user.customer.pk == this_parent_plot.customer_id or user.is_staff:
        context = {
        'map_id' : map_id,
        'this_parent_plot': this_parent_plot,
        'this_plot' : this_plot,
        'latlong': plot_polygon_latlong,
        'scans' : scans,
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
