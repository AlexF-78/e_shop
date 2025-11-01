# #from django import views
# from django.urls import path
# #from django.views.generic import DetailView
#
# from catalog.apps import CatalogConfig
# from catalog.views import HomeView, ContactView, ProductView
# # from . import views
#
# app_name = CatalogConfig.name
#
# urlpatterns = [
#     #path('', views.home, name='home'),
#     path('', HomeView.as_view(), name='home'),
#     # path('contacts/', views.contact, name='contact'),
#     path('', ContactView.as_view(), name='contact'),
#     # path('product/<int:pk>/', views.product_detail, name='product_detail'),
#     path('', DetailView.as_view, name='product'),
#     path('product/<int:pk>/', views.ProductView.as_view(), name='product_detail'),
# ]


from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('product/<int:pk>/', views.ProductView.as_view(), name='product_detail'),
]