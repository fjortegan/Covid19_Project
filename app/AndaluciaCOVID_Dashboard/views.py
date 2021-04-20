from django.shortcuts import render
import json
from .serializers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response

#APP VIEWS


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
        'Delete': '/task-delete/<str:pk>/',
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
def townshipHistoricDetail(request, name):
    tship = Township.objects.filter(name=name)[0]
    townshipHistorics = HistoricTownship.objects.filter(township = tship)
    serializer = TownshipHistoricDetailSerializer(townshipHistorics,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def provinceHistoricDetail(request, name):
    province = Province.objects.filter(name=name)[0]
    provinceHistorics = HistoricProvince.objects.filter(province = province)
    serializer = ProvinceHistoricDetailSerializer(provinceHistorics,many=True)
    return Response(serializer.data)    

@api_view(['GET'])
def regionHistoricDetail(request):
    regionHistorics = HistoricGeneral.objects.all()
    serializer = RegionHistoricDetailSerializer(regionHistorics,many=True)
    return Response(serializer.data)    

@api_view(['GET'])
def regionAccumulatedDetail(request):
    regionAcc= AcumulatedRegion.objects.all()
    serializer = RegionAccumulatedSerializer(regionAcc,many=True)
    return Response(serializer.data)        