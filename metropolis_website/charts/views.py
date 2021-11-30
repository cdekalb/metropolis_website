from django.core.exceptions import ValidationError
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.views.generic import View, FormView
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse

from charts.forms import MetropolisParameters, MetropolisDelete
from .models import MetropolisPlot

from rest_framework.views import APIView
from rest_framework.response import Response

import numpy as np
import scipy.stats
from numpy import ndarray, random
from collections import defaultdict

# Create your views here.

class MetropolisPlotListView(generic.ListView):
    model = MetropolisPlot

class MetropolisPlotDetailView(generic.DetailView):
    model = MetropolisPlot

class DataInput(FormView):
    form = MetropolisParameters
    template = 'charts/input.html'

    def get_success_url(self):
        return ''

    def form_valid(self, form):
        return super().form_valid(form)

    def input_data(self, request):
        if request.method == 'POST':
            form = MetropolisParameters(request.POST)
            if form.is_valid:
                return HttpResponseRedirect('')
        else:
            form = MetropolisParameters()

        return render(request, 'charts/input.html', {'form': form})

class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'charts/index.html')

class ChartData(APIView):

    def get_prob_dist_func(leftBound, rightBound, numPoints, mean, std, distribution='norm'):
        data_points = np.linspace(leftBound, rightBound, numPoints) # Create array of evenly spaced points that include left and right bound
        try:
            if distribution=='norm':
                pdf = [scipy.stats.norm.pdf(point, loc=mean, scale=std)/numPoints for point in data_points] # Create a normal distribution from data_points
            elif distribution=='unif':
                pdf = [scipy.stats.uniform.pdf(point)/numPoints for point in data_points] # Create a uniform distribution from data_points
        except:
            print('Invalid distribution') 

        return pdf, ndarray.tolist(data_points)


    def get_markov_chain(pdf, numPoints, tot_samples):

        start_idx = random.randint(0, numPoints) # Select random starting index of data array
        markov_idx = [start_idx]                   # Initialize list of markov indicies
        count = 0

        for i in range(tot_samples):
            coin = random.randint(0,2)
            if coin:
                if markov_idx[count] == len(pdf) - 1:                     # check if the chain can go any more to the right
                    markov_idx.append(markov_idx[count])                  # append current value to chain
                elif pdf[markov_idx[count] + 1] > pdf[markov_idx[count]]: # check if prob to the right is greater
                    markov_idx.append(markov_idx[count] + 1)              # append index of prob to the right
                else:
                    if random.rand() < (pdf[markov_idx[count] + 1] / pdf[markov_idx[count]]): # probabilistically decide to go to the right
                        markov_idx.append(markov_idx[count] + 1)                              # append index of prob to the right
                    else:
                        markov_idx.append(markov_idx[count])                                  # append current index
            else:
                if markov_idx[count] == 0:                                # check if the chain can go any more to the left
                    markov_idx.append(markov_idx[count])                  # append current value to chain
                elif pdf[markov_idx[count] - 1] > pdf[markov_idx[count]]: # check if prob to the left is greater
                    markov_idx.append(markov_idx[count] - 1)              # append index of prob to the right
                else:
                    if random.rand() < (pdf[markov_idx[count] - 1] / pdf[markov_idx[count]]): # probabilistically decide to go to the left
                        markov_idx.append(markov_idx[count] - 1)                              # append index of prob to the left
                    else:
                        markov_idx.append(markov_idx[count])                                  #  append current index

            count += 1

        return markov_idx


    def get_freq(markov_idx):
        fq = defaultdict(int)
        for i in markov_idx:
            fq[i] += 1

        fq = dict(fq)       # Create dictionary with key value pairs consisting of markov indices and their corresponding frequencies
        
        indices = sorted(fq.keys())
        frequencies = [value for (key, value) in sorted(fq.items())]

        return indices, frequencies


    def get(self, request, format = None):

        pdf_chartdata, pdf_temp_labels = ChartData.get_prob_dist_func(-3, 3, 41, 'norm')
        pdf_labels = [round(label, 3) for label in pdf_temp_labels]
        pdf_chartLabel = 'Probability Distribution'
        pdf_data = {
            'labels':pdf_labels,
            'chartLabel':pdf_chartLabel,
            'chartdata':pdf_chartdata,
        }

        mc_chartdata = ChartData.get_markov_chain(pdf_chartdata, len(pdf_labels))
        mc_chartLabel = 'Markov Chain'
        mc_labels = list(range(len(mc_chartdata)))
        mc_data = {
            'labels':mc_labels,
            'chartLabel':mc_chartLabel,
            'chartdata':mc_chartdata
        }

        bar_labels, bar_chartdata = ChartData.get_freq(mc_chartdata)
        bar_chartLabel = 'Markov Histogram'
        bar_data = {
            'labels':bar_labels,
            'chartLabel':bar_chartLabel,
            'chartdata':bar_chartdata
        }

        data = [pdf_data, mc_data, bar_data]
        return Response(data)

def index(request):
    """View function for home page of site."""
    num_plots = MetropolisPlot.objects.all().count()

    context = {
        'num_plots': num_plots,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

def input_metropolis_parameters(request):

    if request.method == 'POST':
        form = MetropolisParameters(request.POST)
        if form.is_valid():
            form.dist = form.cleaned_data['dist']
            form.bins = form.cleaned_data['bins']
            form.totSamples = form.cleaned_data['totSamples']
            form.mean = form.cleaned_data['mean']
            form.std = form.cleaned_data['std']
            form.lowerBound = form.cleaned_data['lowerBound']
            form.upperBound = form.cleaned_data['upperBound']
            plot = MetropolisPlot(dist=form.dist, bins=form.bins, totSamples=form.totSamples, mean=form.mean, std=form.std,
                                  lowerBound=form.lowerBound, upperBound=form.upperBound)
            plot.save()
        
    else:
        form = MetropolisParameters()

    return render(request, 'charts/metropolisplot_input.html', {'form': form})

def delete_record(request):
    if request.method == 'POST':
        form = MetropolisDelete(request.POST)
        if form.is_valid():
            form.id = form.cleaned_data['id']
            try:
                plot = MetropolisPlot(id=form.id)
            except:
                raise ValidationError('ID does not exist')
            plot.delete()
        
    else:
        form = MetropolisDelete()
    
    return render(request, 'charts/metropolisplot_delete.html', {'form': form})

def plot_api(request, pk):

    obj = MetropolisPlot.objects.get(pk=pk)

    mean = float(obj.mean)
    std = float(obj.std)
    lowerBound = float(obj.lowerBound)
    upperBound = float(obj.upperBound)

    pdf_chartdata, pdf_temp_labels = ChartData.get_prob_dist_func(lowerBound, upperBound, obj.bins, mean, std, obj.dist)
    pdf_labels = [round(label, 3) for label in pdf_temp_labels]
    pdf_chartLabel = 'Probability Distribution'
    pdf_data = {
        'labels':pdf_labels,
        'chartLabel':pdf_chartLabel,
        'chartdata':pdf_chartdata,
    }

    mc_chartdata = ChartData.get_markov_chain(pdf_chartdata, len(pdf_labels), tot_samples=obj.totSamples)
    mc_chartLabel = 'Markov Chain'
    mc_labels = list(range(len(mc_chartdata)))
    mc_data = {
        'labels':mc_labels,
        'chartLabel':mc_chartLabel,
        'chartdata':mc_chartdata
    }

    bar_labels, bar_chartdata = ChartData.get_freq(mc_chartdata)
    bar_chartLabel = 'Markov Histogram'
    bar_data = {
        'labels':bar_labels,
        'chartLabel':bar_chartLabel,
        'chartdata':bar_chartdata
    }

    data = [pdf_data, mc_data, bar_data]

    return JsonResponse(data, safe=False)

def plot_view(request, pk):
    context = {'pk': pk}

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'charts/plot_view.html', context=context)
