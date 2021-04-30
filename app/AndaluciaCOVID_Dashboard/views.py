from django.shortcuts import render
import json
from .serializers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response

# APP VIEWS


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


def dash_general_view(request):
    dataAument = []
    dataHospitalized = []
    dataICU = []
    etiquetas = []
    queryset = AcumulatedRegion.objects.order_by('date')[:14]
    count = 0
    size = queryset.count()

    for register in queryset:
        count += 1
        if (count < size):
            regComp = queryset[count]

        etiquetas.append(str(register.date.day) +
                         '/' + str(register.date.month))
        dataAument.append(register.aument)
        dataHospitalized.append(register.Hospitalized)
        dataICU.append(regComp.ICU - register.ICU)

    incid14days = Region.objects.filter(pk=0)[0].tasa14days
    incid7days = Region.objects.filter(pk=0)[0].tasa7days
    deceased = Region.objects.filter(pk=0)[0].deceased
    recovered = Region.objects.filter(pk=0)[0].recovered

    regi1 = AcumulatedRegion.objects.order_by('date')[0]
    regi2 = AcumulatedRegion.objects.order_by('date')[1]

    isMajorThanYesterday14 = regi1.pcr14days > regi2.pcr14days
    isMajorThanYesterday7 = regi1.pcr7days > regi2.pcr7days

    return render(request, 'dash_general_view.html', {
        'labels': etiquetas,
        'dataAument': dataAument,
        'dataHospitalized': dataHospitalized,
        'dataICU': dataICU,
        'tasaInc14': incid14days,
        'tasaInc7': incid7days,
        'deceased': deceased,
        'recovered': recovered,
        'isMajorThanYesterday14': isMajorThanYesterday14,
        'isMajorThanYesterday7': isMajorThanYesterday7
    })
