# Generated by Django 3.1.6 on 2021-02-07 23:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AndaluciaCOVID_Dashboard', '0002_historicprovince_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicprovince',
            name='date',
            field=models.CharField(default='', max_length=100),
        ),
    ]
