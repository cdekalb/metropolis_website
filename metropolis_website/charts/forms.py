from django import forms
from django.core.exceptions import ValidationError

class MetropolisParameters(forms.Form):
    DISTRIBUTIONS=[('norm', 'Normal Distribution'),
                   ('unif', 'Uniform Distribution')]

    dist = forms.ChoiceField(choices=DISTRIBUTIONS)
    bins = forms.IntegerField()
    totSamples = forms.IntegerField()
    mean = forms.DecimalField()
    std = forms.DecimalField()
    lowerBound = forms.DecimalField()
    upperBound = forms.DecimalField()

    def clean_metropolis_parameters(self):
        data = self.cleaned_data['dist', 'bins', 'totSamples', 'mean', 'std', 'lowerBound', 'upperBound']

        if data['dist'] not in ['norm', 'unif']:
            raise ValidationError('Invalid Distribution')
        if data['bins'] < 2:
            raise ValidationError('Invalid Number of Points')
        if data['totSamples'] < 1:
            raise ValidationError('Invalid Number of Samples')
        if data['std'] <= 0:
            raise ValidationError('Invalid Standard Deviation')
        if data['lowerBound'] >= data['upperBound']:
            raise ValidationError('Invalid Bounds')
        if data['upperBound'] <= data['lowerBound']:
            raise ValidationError('Invalid Bounds')

        return data

class MetropolisDelete(forms.Form):
    id = forms.IntegerField()

    def clean_metropolis_delete(self):
        data = self.cleaned_data['id']

        return data