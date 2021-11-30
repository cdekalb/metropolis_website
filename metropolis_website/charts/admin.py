from django.contrib import admin
from .models import MetropolisPlot

# Register your models here.

# admin.site.register(MetropolisPlot)

class MetropolisPlotAdmin(admin.ModelAdmin):
    list_display = ('dist', 'lowerBound', 'upperBound')
    fields = ['dist', ('lowerBound', 'upperBound')]

admin.site.register(MetropolisPlot, MetropolisPlotAdmin)
