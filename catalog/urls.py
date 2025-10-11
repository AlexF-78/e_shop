
from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import home
from . import views

app_name = CatalogConfig.name

urlpatterns = [
    path('', views.home, name='home'),
    path('contacts/', views.contact, name='contact'),
]