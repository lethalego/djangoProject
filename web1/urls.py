from django.urls import path
from .views import list_earth_engine_catalogs, list_earth_engine_catalogsname

urlpatterns = [
    path('catalogs/', list_earth_engine_catalogs, name='list_earth_engine_catalogs'),
    path('catalogs/<str:catalog_name>/', list_earth_engine_catalogsname, name='list_earth_engine_catalogsname'),
    # Diğer pattern'lar...
]