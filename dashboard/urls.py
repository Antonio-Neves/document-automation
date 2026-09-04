from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='dashboard'),
    path(
        'contract-sale-vehicle/',
        views.ContractSaleVehicleView.as_view(),
        name='contract_sale_vehicle',
    ),
]
