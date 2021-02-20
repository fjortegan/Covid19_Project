import pandas as pd
import datetime
from django.core.management.base import BaseCommand

import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'COVID19_Andalucia.settings')
django.setup()
from AndaluciaCOVID_Dashboard.models import *

class Command(BaseCommand):
    help = 'Use this command to populate de DB automatically'

    Province.objects.all().delete()
    District.objects.all().delete()
    Township.objects.all().delete()
    def getProvinces(self):
        """ 
        Migrar a la base de datos las provincias,municipios y distritos de Andalucía
        """
        try:
            directory = 'https://raw.githubusercontent.com/Pakillo/COVID19-Andalucia/master/datos/muni_prov_dist.csv'
            df = pd.read_csv(directory, delimiter=",", names=[
                'province', 'distrit', 'township'])
            df.drop(df.index[[0, 2]])
            for prov in df.province:
                if (Province.objects.filter(name=prov).exists() == False):
                    province = Province(name=prov)
                    province.save()
        except IndexError as e:
            print(e)

    def getDistrFromProv(self):
        try:
            directory = 'https://raw.githubusercontent.com/Pakillo/COVID19-Andalucia/master/datos/muni_prov_dist.csv'
            df = pd.read_csv(directory, delimiter=",", names=[
                'province', 'distrit', 'township'])
            df.drop(df.index[[0, 2]])
            provinces = Province.objects.all()
            for province in provinces:
                for distr in df[df.province == province.name].distrit:
                    if (District.objects.filter(name=distr).exists() == False):
                        distr = District(name=distr, province=province)
                        distr.save()

        except IndexError as e:
            print(e)

    def getTownShipFromDistr(self):
        try:
            directory = 'https://raw.githubusercontent.com/Pakillo/COVID19-Andalucia/master/datos/muni_prov_dist.csv'
            df = pd.read_csv(directory, delimiter=",", names=[
                'province', 'distrit', 'township'])
            df.drop(df.index[[0, 2]])
            districts = District.objects.all()
            for district in districts:
                for ts in df[df.distrit == district.name].township:
                    if (Township.objects.filter(name=ts).exists() == False):
                        township = Township(name=ts, distrit=district)
                        township.save()
        except IndexError as e:
            print(e)

    def handle(self, *args, **options):
        print('Adding provinces...')
        self.getProvinces()
        print('Adding distrits...')
        self.getDistrFromProv()
        print('Adding townships...')
        self.getTownShipFromDistr()
        print('...MIGRATION SUCCESFUL!')
