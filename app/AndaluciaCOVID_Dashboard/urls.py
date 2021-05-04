from . import views
from django.urls import include, path
from django.conf.urls import url

urlpatterns = [
    path('general/', views.dash_general_view, name='dash_general_view'),
    path('provinces/', views.dash_province_view, name='dash_province_view')
]