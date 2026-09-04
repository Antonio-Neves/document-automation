from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='dashboard'),
    path('vehicle/', views.vehicle, name='vehicle'),
]
