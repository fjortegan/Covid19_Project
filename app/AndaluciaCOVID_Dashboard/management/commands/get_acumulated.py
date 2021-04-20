import pandas as pd
import numpy as np
from datetime import timedelta,date,datetime
from django.core.management.base import BaseCommand

import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'COVID19_Andalucia.settings')
django.setup()
from AndaluciaCOVID_Dashboard.models import *

class Command(BaseCommand):
    args = '<Nombre de provincia ...>'
    help = 'Usa este comando para obtener los acumulados de las provincias y de la región de Andalucía '
    
    def add_arguments(self , parser):
        parser.add_argument("-p", "--territorio", type=str)

    def getAcumulatedTodayProv(self, provinceName, date):
        try:
            directory = 'https://raw.githubusercontent.com/Pakillo/COVID19-Andalucia/master/datos/acumulados.csv'
            df = pd.read_csv(directory, delimiter=";")
            df.replace(np.NaN, 0, inplace=True)
            df = df.iloc[1:]
            province = Province.objects.filter(name=provinceName)[0]
            listRegister = []
            dateDF = date.strftime('%d/%m/%Y')

            for listaDatos in (df[df["Territorio"] == province.name].values): 
                if (listaDatos[0]==dateDF):
                    listData = listaDatos.tolist()
                    listRegister.append(listData[3])
            registerExists = AcumulatedProvinces.objects.filter(province=province,date=date)
            if (registerExists.count()==0):
                newRegisterAccumulated = AcumulatedProvinces(
                    province = province,
                    date = date,
                    confirmedPDIA = int(listRegister[0]),
                    aument= int(listRegister[1]),
                    pcr14days = int(listRegister[2]),
                    pcr7days = int(listRegister[3]),
                    totalConfirmed = int(listRegister[4]),
                    Hospitalized = int(listRegister[5]),
                    ICU = int(listRegister[6]),
                    deceased = int(listRegister[7]),
                    recovered = int(listRegister[8]))
                newRegisterAccumulated.save()                    
        except IndexError as e:
            print(e)

    def getAcumulatedTodayReg(self,date):
        try:
            directory = 'https://raw.githubusercontent.com/Pakillo/COVID19-Andalucia/master/datos/acumulados.csv'
            df = pd.read_csv(directory, delimiter=";")
            df.replace(np.NaN, 0, inplace=True)
            listRegister = []
            regionObject = Region.objects.filter(name="Andalucía")[0]
            dateDF = date.strftime('%d/%m/%Y')

            for listaDatos in (df[df["Territorio"] == "Andalucía"].values): 
                if (listaDatos[0]==dateDF):
                    listData = listaDatos.tolist()
                    listRegister.append(listData[3])
            registerExists = AcumulatedRegion.objects.filter(ccaa=regionObject,date=date)
            if (registerExists.count()==0):
                newRegisterAccumulated = AcumulatedRegion(
                    ccaa = regionObject,
                    date = date,
                    confirmedPDIA = int(listRegister[0]),
                    aument= int(listRegister[1]),
                    pcr14days = int(listRegister[2]),
                    pcr7days = int(listRegister[3]),
                    totalConfirmed = int(listRegister[4]),
                    Hospitalized = int(listRegister[5]),
                    ICU = int(listRegister[6]),
                    deceased = int(listRegister[7]),
                    recovered = int(listRegister[8]))
                newRegisterAccumulated.save()       
                listRegister.clear()             
        except IndexError as e:
            print(e)

    def getAcumulatedTodayTship(self, munName):
        try:
            directory = 'https://raw.githubusercontent.com/Pakillo/COVID19-Andalucia/master/datos/municipios.dia/Municipios_todos_datoshoy.csv'
            df = pd.read_csv(directory, delimiter=";")
            df.replace(np.NaN, 0, inplace=True)
            df = df.iloc[1:]
            tship = Township.objects.filter(name=munName)[0]
            date = datetime.now().date()
            listRegister = []

            for listaDatos in (df[df["Lugar de residencia"] == tship.name].values):
                listData = listaDatos.tolist()
                listRegister.append(listData[2])
            print(listRegister)
            registerExists = AcumulatedTownsip.objects.filter(tship=tship,date=date)
            if (registerExists.count()==0):
                newRegisterAccumulated = AcumulatedTownsip(
                    tship = tship,
                    date = datetime.now().date(),
                    confirmedPDIA = int(listRegister[1]),
                    tasa14days = int(listRegister[4].split(",")[0]),
                    tasa7days = int(listRegister[6].split(",")[0]),
                    totalConfirmed = int(listRegister[7]),
                    deceased = int(listRegister[7]),
                    recovered = int(listRegister[9]))
                newRegisterAccumulated.save()                    
        except IndexError as e:
            print(e)         
    
    def daterange(self,date1, date2):
        for n in range(int ((date2 - date1).days)+1):
            yield date1 + timedelta(n)

    def handle(self, *args, **options):
        print('Updating...')
        argument = options["territorio"] if options["territorio"] else "mun"
        townships = Township.objects.all()
        start = datetime.now() - timedelta(days=14)
        start_dt = start.date()
        end_dt = datetime.now().date()
        for dt in self.daterange(start_dt, end_dt):
            if (argument=="Andalucía"):
                self.getAcumulatedTodayReg(dt)
            elif (argument!="mun"):
                self.getAcumulatedTodayProv(argument,dt)
        
        for township in townships:
            self.getAcumulatedTodayTship(township.name)
        print('...MIGRATION SUCCESFUL!')