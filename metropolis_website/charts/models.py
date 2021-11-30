from django.db import models
from django.urls import reverse

# # Create your models here.

class MetropolisPlot(models.Model):
    DISTRIBUTIONS = (
        ('norm', 'Normal Distribution'),
        ('unif', 'Uniform Distribution')
    )

    dist = models.CharField(choices=DISTRIBUTIONS, help_text='Enter desired distribution', max_length=4)
    bins = models.IntegerField(help_text='Enter desired number of points in distribution')
    totSamples = models.IntegerField(help_text='Enter the desired number of drawn samples')
    mean = models.DecimalField(decimal_places=3, max_digits=6, help_text='Enter the mean of the distribution', default=0)
    std = models.DecimalField(decimal_places=3, max_digits=6, help_text='Enter the standard devaition of the distribution', default=1)
    lowerBound = models.DecimalField(decimal_places=3, max_digits=6, help_text='Enter a lower bound')
    upperBound = models.DecimalField(decimal_places=3, max_digits=6, help_text='Enter an upper bound')

    def get_absolute_url(self):
        """Returns the url to access a detail record for this choice of parameters."""
        return reverse('charts:metropolisplot-detail', args=[str(self.id)])

    def get_plot_view(self, *args):
        """Returns the url to access the plots for the given record."""
        # Currently redirects to itself #
        return reverse('charts:input_metropolis_parameters', args=[str(self.id)])