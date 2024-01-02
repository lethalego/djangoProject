import os

from django.conf import settings
from django.http import HttpResponseServerError
from django.shortcuts import render
import ee

from web1.catalog_main_ids import catalog_ids


def about(request):
    return render(request, "about.html")


def initialize_ee_credentials():
    # Service account credentials
    service_account = 'serefkosnek-ee@ee-serefkosnek.iam.gserviceaccount.com'
    private_key_file = os.path.join(settings.BASE_DIR, '.private-key.json')

    # Initialize Earth Engine with service account credentials
    credentials = ee.ServiceAccountCredentials(service_account, private_key_file)
    ee.Initialize(credentials)


def list_earth_engine_catalogs(request):
    try:

        initialize_ee_credentials()

        catalog_main_id_list = catalog_ids

        selected_catalog = request.POST.get('catalogSelector', None)

        if selected_catalog:
            catalogs = ee.data.listAssets(params={'parent': selected_catalog})
            catalog_size = 0

            # Gruplama işlemi
            grouped_catalogs = {}
            for asset in catalogs['assets']:
                catalog_size = catalog_size + 1
                asset_type = asset['type']
                if asset_type not in grouped_catalogs:
                    grouped_catalogs[asset_type] = []
                grouped_catalogs[asset_type].append(asset)

            return render(request, "catalogs.html", {"catalog_main_id_list": catalog_main_id_list,
                                                     "selected_catalog": selected_catalog,
                                                     "grouped_catalogs": grouped_catalogs,
                                                     "catalog_size": catalog_size})
        else:
            catalogs = None
            return render(request, "catalogs.html", {"catalog_main_id_list": catalog_main_id_list,
                                                     "selected_catalog": selected_catalog,
                                                     "catalogs": catalogs,
                                                     "catalog_size": 0})

    except Exception as e:
        error_message = f"Hata oluştu: {str(e)}"
        print(f"Detaylı Hata: {e}")
        return HttpResponseServerError(error_message)


def list_earth_engine_catalogsname(request, catalog_name):
    try:

        # Seçilen kataloga ait bilgileri getir
        catalogs = ee.data.listAssets(params={'parent': catalog_name})

        print(f"{catalog_name} Catalogs:", catalogs)

        return render(request, "catalogs.html", {"selected_catalog": catalog_name, "catalogs": catalogs})

    except Exception as e:
        error_message = f"Hata oluştu: {str(e)}"
        print(f"Detaylı Hata: {e}")
        return HttpResponseServerError(error_message)
