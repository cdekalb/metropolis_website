# Generated by Django 2.2.5 on 2021-09-01 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('charts', '0003_auto_20210901_1400'),
    ]

    operations = [
        migrations.AlterField(
            model_name='metropolisplot',
            name='bins',
            field=models.IntegerField(help_text='Enter desired number of points in distribution'),
        ),
    ]
