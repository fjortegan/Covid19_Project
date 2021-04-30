from . import views
from django.urls import include, path
from django.conf.urls import url

urlpatterns = [
    path('general/', views.dash_general_view, name='dash_general_view')
]