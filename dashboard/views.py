from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'dashboard/index.html'


class ContractSaleVehicleView(TemplateView):
    template_name = 'dashboard/contract_sale_vehicle.html'
    page_title = 'Veículo'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.page_title
        return context
