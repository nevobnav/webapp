from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.sessions.models import Session
from django.http import HttpResponse
from .models import Plot,Scan

def get_all_plots(request_session):
    if request_session.user.is_authenticated:
        user = request_session.user
        plots = Plot.objects.filter(customer=user).order_by('-startdate')
    else:
        plots = ''
    return plots


def home(request):
    plots = get_all_plots(request)
    context = {"name" : "Kaz", "plots" : plots}
    return render(request, 'portal/home.html', context=context)


@login_required(login_url='/login/')
def map(request, map_id):
    user = request.user
    plots = get_all_plots(request)
    this_plot =  Plot.objects.get(id=map_id)
    scans = Scan.objects.filter(plot=this_plot)
    area = this_plot.shape.transform(28992,clone=True).area

    if user == this_plot.customer:
        context = {
        'map_id' : map_id,
        'plots' : plots,
        'plot' : this_plot,
        'scans' : scans
        }
        return render(request, 'portal/map.html', context=context)
    else:
        return redirect('portal-home')


def about(request):
    return render(request, 'portal/about.html')

def test(request):
    return render(request, 'portal/test.html')
