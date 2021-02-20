import pandas as pd
import datetime
from django.core.management.base import BaseCommand

import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'COVID19_Andalucia.settings')
django.setup()
from AndaluciaCOVID_Dashboard.models import *

class Command(BaseCommand):
    args = '<Territory name ...>'
    help = 'Use this command to update the data of COVID19 from IECA in provinces'

    def getAcumulatedToday(self):
        try:
            directory = 'https://raw.githubusercontent.com/Pakillo/COVID19-Andalucia/master/datos/datos_provincias_clean.csv'
            df = pd.read_csv(directory, delimiter=",", names=[
                'fdiag', 'prov', 'pcrConfirmed','totalConfirmed','hospitalized','ICU','deceased'])
            df.drop(df.index[[0, 1]])
            provinces = Province.objects.all()
            for prov in provinces:
                for row in (df[df["prov"] == prov.name].values):
                    province = Province.objects.filter(name=row[1])
                    newHistoric = HistoricProvince(date=row[0],
                        province=province[0],
                        confirmedPDIA=int(row[2]),
                        totalConfirmed=int(row[3]),
                        Hospitalized=int(row[4]),
                        ICU=int(row[5]),
                        deceased=int(row[6])
                    )
                    newHistoric.save()
        except IndexError as e:
            print(e)

    def handle(self, *args, **options):
        print('Updating...')
        self.updateHistoricProvince()
        print('...MIGRATION SUCCESFUL!')