from django.urls import path

from .views import (
    ContractSalePropertyCompleteView,
    ContractSalePropertyDeedView,
    ContractSalePropertySimpleView,
    ContractSaleVehicleCompleteView,
    IndexView,
)

urlpatterns = [
    path('', IndexView.as_view(), name='dashboard'),
    path(
        'contract-sale-vehicle-complete/',
        ContractSaleVehicleCompleteView.as_view(),
        name='contract_sale_vehicle_complete',
    ),
    path(
        'contract-sale-property-complete/',
        ContractSalePropertyCompleteView.as_view(),
        name='contract_sale_property_complete',
    ),
    path(
        'contract-sale-property-deed/',
        ContractSalePropertyDeedView.as_view(),
        name='contract_sale_property_deed',
    ),
    path(
        'contract-sale-property-simple/',
        ContractSalePropertySimpleView.as_view(),
        name='contract_sale_property_simple',
    ),
]
