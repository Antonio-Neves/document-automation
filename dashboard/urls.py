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
        'contract-sale-property-complete/',
        views.ContractSalePropertyCompleteView.as_view(),
        name='contract_sale_property_complete',
    ),
    path(
        'contract-sale-property-deed/',
        views.ContractSalePropertyDeedView.as_view(),
        name='contract_sale_property_deed',
    ),
]
