from django.shortcuts import render
import json
from .serializers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response

# APP VIEWS


def dash_general_view(request):
    dataAument = []
    dataHospitalizedCounter = []
    dataICU = []
    etiquetas1 = []
    etiquetas2 = []
    deceasedList = []
    recoveredList = []
    queryset2 = AcumulatedRegion.objects.order_by('date')[:16]
    count = 0
    size = queryset2.count()

    for register in queryset2:
        if (count==0):
            regComp = queryset2[0]
        count += 1
        if (count < size):
            regComp = queryset2[count]
            etiquetas2.append(str(queryset2[count].date.day) + '/' + str(queryset2[count].date.month))           
        dataICU.append(regComp.ICU - register.ICU)
        dataHospitalizedCounter.append(
            regComp.Hospitalized - register.Hospitalized - dataICU[count-1])  
                 
        etiquetas1.append(str(register.date))
        dataAument.append(register.aument)
        deceasedList.append(regComp.deceased - register.deceased)
        recoveredList.append(regComp.recovered - register.recovered)

    incid14days = Region.objects.filter(pk=0)[0].tasa14days
    incid7days = Region.objects.filter(pk=0)[0].tasa7days
    deceased = Region.objects.filter(pk=0)[0].deceased
    recovered = Region.objects.filter(pk=0)[0].recovered

    regi1 = AcumulatedRegion.objects.order_by('date')[0]
    regi2 = AcumulatedRegion.objects.order_by('date')[1]

    isMajorThanYesterday14 = regi1.pcr14days > regi2.pcr14days
    isMajorThanYesterday7 = regi1.pcr7days > regi2.pcr7days

    return render(request, 'dash_general_view.html', {
        'labels': etiquetas1,
        'labels2': etiquetas2,
        'dataAument': dataAument,
        'dataHospitalizedCounter': dataHospitalizedCounter,
        'dataICU': dataICU,
        'tasaInc14': incid14days,
        'tasaInc7': incid7days,
        'deceased': deceased,
        'recovered': recovered,
        'isMajorThanYesterday14': isMajorThanYesterday14,
        'isMajorThanYesterday7': isMajorThanYesterday7,
        'deceasedList': deceasedList,
        'recoveredList': recoveredList
    })


def search(request):
    results = []
    query = request.GET.get('q')
    results.add(Province.objects.filter(name.contains(q)))
    results.add(Township.objects.filter(name.contains(q)))
    return render(request, 'account/index.html', {'results': results})


def dash_province_view(request):
    provinces = Province.objects.all()
    etiquetas = []

    provincesIncidence = {}
    for province in provinces:
        provincesIncidence[province.name] = province.tasa14days

    return render(request, 'dash_province_view.html', {
        'labels': etiquetas,
        'provincesIncidence': provincesIncidence
    })

# API VIEWS


@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'Lista de provincias': '/province-list/',
        'Lista de municipios': '/township-list/',
        'Lista de distritos': '/district-list/',
        'Histórico de una provincia': '/province-historic-detail/<str:name>/',
        'Histórico de un municipio': '/township-historic-detail/<str:name>/',
        'Histórico de Andalucía': '/region-historic-detail/',
        'Acumulados en la región': '/region-acumulated-all/',
        'Acumulados en las provincias': '/province-acumulated-all/',
        'Acumulados en los municipios': '/township-acumulated-all/'
    }
    return Response(api_urls)


@api_view(['GET'])
def provinceList(request):
    provinces = Province.objects.all()
    serializer = ProvinceSerializer(provinces, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def districtList(request):
    districts = District.objects.all()
    serializer = DistrictSerializer(districts, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def townshipList(request):
    townships = Township.objects.all()
    serializer = TownshipSerializer(townships, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def townshipHistoricDetail(request, pk):
    tship = Township.objects.filter(name=pk)[0].order_by('-date',)
    townshipHistorics = HistoricTownship.objects.filter(township=tship)
    serializer = TownshipHistoricDetailSerializer(townshipHistorics, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def provinceHistoricDetail(request, pk):
    province = Province.objects.filter(pk=pk)[0].order_by('-date',)
    provinceHistorics = HistoricProvince.objects.filter(province=province)
    serializer = ProvinceHistoricDetailSerializer(provinceHistorics, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def regionHistoricDetail(request):
    regionHistorics = HistoricGeneral.objects.all().order_by('-date',)
    serializer = RegionHistoricDetailSerializer(regionHistorics, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def regionAccumulatedAll(request):
    regionAcc = AcumulatedRegion.objects.all().order_by('-date',)
    serializer = RegionAccumulatedSerializer(regionAcc, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def provinceAccumulatedAll(request):
    provinceAcc = AcumulatedProvinces.objects.all().order_by('-date',)
    serializer = ProvincesAccumulatedSerializer(provinceAcc, many=True)
    return Response(serializer.data)
