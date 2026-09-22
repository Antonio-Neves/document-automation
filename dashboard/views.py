from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils import timezone
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'dashboard/index.html'


class ContractPdfView(TemplateView):
    pdf_template_name = None
    pdf_filename_prefix = None
    page_title = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.page_title
        return context

    def post(self, request, *args, **kwargs):
        from weasyprint import HTML

        fields = {
            key: value.strip()
            for key, value in request.POST.items()
        }

        html_string = render_to_string(
            self.pdf_template_name,
            {'fields': fields},
            request=request,
        )
        pdf_bytes = HTML(
            string=html_string,
            base_url=request.build_absolute_uri('/'),
        ).write_pdf()

        filename = self._pdf_filename()
        output_dir = settings.BASE_DIR / 'contract_files' / 'created_contracts'
        output_dir.mkdir(parents=True, exist_ok=True)
        (output_dir / filename).write_bytes(pdf_bytes)

        response = HttpResponse(pdf_bytes, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response

    def _pdf_filename(self):
        timestamp = timezone.localtime().strftime('%Y%m%d_%H%M')
        return f'{self.pdf_filename_prefix}_{timestamp}.pdf'


class ContractSaleVehicleView(ContractPdfView):
    template_name = 'dashboard/contract_sale_vehicle.html'
    pdf_template_name = 'dashboard/contract_sale_vehicle_pdf.html'
    pdf_filename_prefix = 'contract_sale_vehicle'
    page_title = 'Veículo Completo'


class ContractSalePropertyView(ContractPdfView):
    template_name = 'dashboard/contract_sale_property.html'
    pdf_template_name = 'dashboard/contract_sale_property_pdf.html'
    pdf_filename_prefix = 'contract_sale_property'
    page_title = 'Imóvel'


class ContractSaleLandView(ContractPdfView):
    template_name = 'dashboard/contract_sale_land.html'
    pdf_template_name = 'dashboard/contract_sale_land_pdf.html'
    pdf_filename_prefix = 'contract_sale_land'
    page_title = 'Terreno'
