from django.shortcuts import render
import json
from .serializers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import timedelta, date, datetime

# APP VIEWS


def dash_general_view(request):
    dataAument = []
    dataHospitalizedCounter = []
    dataICU = []
    etiquetas1 = []
    etiquetas2 = []
    deceasedList = []
    recoveredList = []
    start = datetime.now() - timedelta(days=14)
    start_dt = start.date()
    end_dt = datetime.now().date()
    queryset2 = AcumulatedRegion.objects.filter(date__range=(start_dt, end_dt))
    count = 0
    size = queryset2.count()

    for register in queryset2:
        if (count == 0):
            regComp = queryset2[0]
        count += 1
        if (count < size):
            regComp = queryset2[count]
            etiquetas2.append(
                str(queryset2[count].date.day) + '/' + str(queryset2[count].date.month))
            etiquetas1.append(
                str(queryset2[count].date.day) + '/' + str(queryset2[count].date.month))
        dataICU.append(regComp.ICU - register.ICU)
        dataHospitalizedCounter.append(
            regComp.Hospitalized - register.Hospitalized - dataICU[count-1])

        dataAument.append(register.aument)
        deceasedList.append(regComp.deceased - register.deceased)
        recoveredList.append(regComp.recovered - register.recovered)

    incid14days = Region.objects.filter(pk=0)[0].tasa14days
    incid7days = Region.objects.filter(pk=0)[0].tasa7days
    deceased = Region.objects.filter(pk=0)[0].deceased
    recovered = Region.objects.filter(pk=0)[0].recovered

    regi1 = AcumulatedRegion.objects.order_by('-date')[0].aument
    regi2 = AcumulatedRegion.objects.order_by('-date')[1].aument

    percentageAument = round((regi1 - regi2)/regi2,2)

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
        'deceasedList': deceasedList,
        'recoveredList': recoveredList,
        'percentageAument':percentageAument
    })

def dash_search_view(request, template_name='dash_search_view.html'):
    listings = []
    context_dict = {}

    if request.GET.get('search'):
        nameFilter = request.GET.get('search')

        if (request.POST.get('id1', True) & (request.POST.get('id2',False))):
            listings = Township.objects.filter(name__contains=nameFilter)
        elif (request.POST.get('id1', False) & (request.POST.get('id2',True))):
            listings = Province.objects.filter(name__contains=nameFilter)
        else:
             listings = Province.objects.filter(name__contains=nameFilter)
             if (listings.count()==0):
                listings = Township.objects.filter(name__contains=nameFilter)

    if (listings.count()==0):
        template_name = "dash_not_found.html"
    else:
        if (isinstance(listings[0],Province)):
            territoryToView = listings[0]
            tasa14days =  listings[0].tasa14days
            template_name = "dash_province_detail_view.html"
        else:
            territoryToView = listings[0]
            tasa14days =  listings[0].tasa14days   
            template_name = "dash_township_detail_view.html"    
        context_dict = {'tasa14days': tasa14days}

    return render(request, template_name, context_dict)

def dash_province_view(request):
    provinces = Province.objects.order_by('name')
    etiquetas = []
    provincesIncidence = []
    ICU = []
    deceased = []
    recovered = []
    pcr14days = []
    pcr7days = []
    tasa14dias = []
    recovereList = []
    start = datetime.now() - timedelta(days=14)
    start_dt = start.date()
    end_dt = datetime.now().date()

    for province in provinces:
        registerAcum = AcumulatedProvinces.objects.order_by('-date').filter(province=province,date__range=(start_dt, end_dt))
        hospitalizedProv = []

        if (registerAcum.count()>0):
            etiquetas.append(province.name)
            deceasedToAdd = registerAcum[0].deceased - registerAcum[1].deceased
            recoveredToAdd = registerAcum[0].recovered - registerAcum[1].recovered
            pcr14days.append(registerAcum[0].pcr14days)
            pcr7days.append(registerAcum[0].pcr7days)
            ICU.append(registerAcum[0].ICU  - registerAcum[1].ICU)
            deceased.append(deceasedToAdd)
            recovered.append(recoveredToAdd)
            provincesIncidence.append(registerAcum[0].aument)
            tasa14dias.append(province.tasa14days)    
            recovereList.append(province.recovered)    
       
    return render(request, 'dash_province_view.html', {
        'labels': etiquetas,
        'provincesIncidence': provincesIncidence,
        'UCI':ICU,
        'pcr14days':pcr14days,
        'deceased': deceased,
        'recovered': recovered,
        'tasa14dias':tasa14dias,
        'recovereList':recovereList,
        'provinces':provinces,
        'pcr7days':pcr7days
    })

def dash_province_detail_view(request,pk):
    
    start = datetime.now() - timedelta(days=14)
    start_dt = start.date()
    end_dt = datetime.now().date()
    province = Province.objects.filter(pk=pk)[0]
    tships = Township.objects.all()
    districts = District.objects.filter(province=province)
    etiquetas = []
    provinceIncidence = []
    dataICU = []
    queryset = AcumulatedProvinces.objects.filter(province=province,date__range=(start_dt, end_dt))
    queryset2 = HistoricProvince.objects.filter(province=province,date__range=(start_dt, end_dt))
    townshipsProv = []
    townships500 = []
    townships1000 = []

    size = queryset.count()
    count = 0
    dataHospitalizedCounter = []
    dataAument = []
    deceasedList = []
    recoveredList = []

    for district in districts:
        for tship in tships:
            if (tship.distrit==district):
                townshipsProv.append(tship)

    for township in townshipsProv:
        if township.tasa14days > 500:
           townships500.append(township.name) 
        if township.tasa14days > 1000:
           townships1000.append(township.name)    

    for register in queryset:
        etiquetas.append(str(register.date.day) + '/' + str(register.date.month))
        dataAument.append(register.aument)
        deceasedList.append(register.deceased)
        recoveredList.append(register.recovered)
 
    for register in queryset2:
        dataICU.append(register.ICU)
        dataHospitalizedCounter.append(register.Hospitalized)

    incid14days = province.tasa14days
    incid7days = province.tasa7days
    deceased = province.deceased
    recovered = province.recovered

    regi1 = AcumulatedProvinces.objects.order_by('date')[0]
    regi2 = AcumulatedProvinces.objects.order_by('date')[1]


    print(request.GET.get('sel1'))
    print(request.GET.get('sel2'))


    return render(request, 'dash_province_detail_view.html', {
        'labels': etiquetas,
        'districts':districts,
        'dataAument': dataAument,
        'dataHospitalizedCounter': dataHospitalizedCounter,
        'dataICU': dataICU,
        'tasaInc14': incid14days,
        'tasaInc7': incid7days,
        'deceased': deceased,
        'recovered': recovered,
        'tships': tships,
        'townships500': townships500,
        'townships1000':townships1000,
        'townships500list': ",".join(townships500),
        'townships1000list': ",".join(townships1000)
    })

def dash_township_detail_view(request,pk):
    ts = Township.objects.filter(pk=pk)[0]
    etiquetas = []
    incidence = []
    ICU = []

    return render(request, 'dash_township_detail_view.html', {
        'labels': etiquetas,
        'provinceIncidence': provinceIncidence,
        'UCI':ICU
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
