from django.shortcuts import render


def index(request):
    return render(request, 'dashboard/index.html')


def vehicle(request):
    return render(request, 'dashboard/veiculo.html')
