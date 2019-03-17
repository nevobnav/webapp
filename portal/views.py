from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.sessions.models import Session
from django.http import HttpResponse
from .models import Plot,Scan,Customer

def get_all_plots(request_session):
    if request_session.user.is_authenticated:
        user = request_session.user
        plots = Plot.objects.filter(customer_id=user.customer.pk).order_by('-startdate')
    else:
        plots = ''
    return plots


def home(request):
    return render(request, 'portal/home.html', context={})


@login_required(login_url='/login/')
def map(request, map_id):
    user = request.user
    plots = get_all_plots(request)
    this_plot =  Plot.objects.get(id=map_id)
    scans = Scan.objects.filter(plot=this_plot).order_by('date')
    area = this_plot.shape.transform(28992,clone=True).area

    if user.customer.pk == this_plot.customer_id:
        context = {
        'map_id' : map_id,
        'this_plot' : this_plot,
        'scans' : scans
        }
        return render(request, 'portal/map.html', context=context)
    else:
        return redirect('portal-home')

@login_required(login_url='/login/')
def user_profile(request):
    user = request.user
    plots = get_all_plots(request)
    acreage = 0
    for plot in plots:
        acreage += plot.area

    context = {
    'acreage': acreage,
    }
    return render(request,'portal/user_profile.html', context=context)


def about(request):
    return render(request, 'portal/about.html')

def test(request):
    return render(request, 'portal/test.html')
