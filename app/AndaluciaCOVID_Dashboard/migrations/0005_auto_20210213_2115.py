# Generated by Django 3.1.6 on 2021-02-13 20:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('AndaluciaCOVID_Dashboard', '0004_auto_20210208_0030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicprovince',
            name='date',
            field=models.DateField(default='', max_length=100),
        ),
        migrations.CreateModel(
            name='HistoricTownship',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField(default='', max_length=100)),
                ('alias', models.CharField(max_length=100)),
                ('confirmedPCRTA', models.IntegerField(default=0)),
                ('confirmed14days', models.IntegerField(default=0)),
                ('confirmed14100hab', models.IntegerField(default=0)),
                ('totalConfirmed', models.IntegerField(default=0)),
                ('deceases', models.IntegerField(default=0)),
                ('distr', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AndaluciaCOVID_Dashboard.district')),
            ],
            options={
                'unique_together': {('id', 'date')},
            },
        ),
        migrations.CreateModel(
            name='HistoricDistrit',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField(default='', max_length=100)),
                ('alias', models.CharField(max_length=100)),
                ('confirmedPCRTA', models.IntegerField(default=0)),
                ('confirmed14days', models.IntegerField(default=0)),
                ('confirmed14100hab', models.IntegerField(default=0)),
                ('totalConfirmed', models.IntegerField(default=0)),
                ('deceases', models.IntegerField(default=0)),
                ('prov', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AndaluciaCOVID_Dashboard.province')),
            ],
            options={
                'unique_together': {('id', 'date')},
            },
        ),
    ]
