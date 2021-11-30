"""charts URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from views import input_metropolis_parameters
from django.contrib import admin
from django.urls import path, include
from charts import views

app_name = 'charts'

urlpatterns = [
    path('', views.index, name='index'),
    path('input/', views.input_metropolis_parameters, name='input-metropolis-parameters'),
    path('delete/', views.delete_record, name='delete-record'),
    path('plots/', views.MetropolisPlotListView.as_view(), name='metropolisplots'),
    path('plots/<int:pk>', views.MetropolisPlotDetailView.as_view(), name='metropolisplot-detail'),
    path('plots/<int:pk>/view', views.plot_view, name='plot-view')
]