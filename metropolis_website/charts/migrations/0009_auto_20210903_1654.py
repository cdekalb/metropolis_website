# Generated by Django 2.2.5 on 2021-09-03 20:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('charts', '0008_auto_20210903_1543'),
    ]

    operations = [
        migrations.AddField(
            model_name='metropolisplot',
            name='mean',
            field=models.DecimalField(decimal_places=3, default=0, help_text='Enter the mean of the distribution', max_digits=6),
        ),
        migrations.AddField(
            model_name='metropolisplot',
            name='std',
            field=models.DecimalField(decimal_places=3, default=1, help_text='Enter the standard devaition of the distribution', max_digits=6),
        ),
    ]
