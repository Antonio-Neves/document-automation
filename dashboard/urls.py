from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='dashboard'),
    path(
        'contract-sale-vehicle/',
        views.ContractSaleVehicleView.as_view(),
        name='contract_sale_vehicle',
    ),
    path(
        'contract-sale-property/',
        views.ContractSalePropertyView.as_view(),
        name='contract_sale_property',
    ),
    path(
        'contract-sale-land/',
        views.ContractSaleLandView.as_view(),
        name='contract_sale_land',
    ),
]
