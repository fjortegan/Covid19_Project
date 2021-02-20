# Generated by Django 3.1.6 on 2021-02-13 20:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('AndaluciaCOVID_Dashboard', '0005_auto_20210213_2115'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicdistrit',
            name='prov',
        ),
        migrations.AddField(
            model_name='historicdistrit',
            name='distr',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='AndaluciaCOVID_Dashboard.district'),
        ),
    ]
