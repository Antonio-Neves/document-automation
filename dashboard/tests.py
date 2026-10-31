from django.template import Context, Template
from django.test import SimpleTestCase

from dashboard.views import ContractPdfView


class GenderTagTests(SimpleTestCase):
    def render_gender(self, value, pair):
        template = Template('{% load contract_filters %}{% gender value pair %}')
        return template.render(Context({'value': value, 'pair': pair}))

    def test_masculine_uses_left_side(self):
        result = self.render_gender('masculine', 'do VENDEDOR|da VENDEDORA')
        self.assertEqual(result, 'do VENDEDOR')

    def test_feminine_uses_right_side(self):
        result = self.render_gender('feminine', 'do VENDEDOR|da VENDEDORA')
        self.assertEqual(result, 'da VENDEDORA')

    def test_missing_gender_falls_back_to_masculine(self):
        result = self.render_gender('', 'do VENDEDOR|da VENDEDORA')
        self.assertEqual(result, 'do VENDEDOR')

    def test_invalid_gender_falls_back_to_masculine(self):
        result = self.render_gender('other', 'do VENDEDOR|da VENDEDORA')
        self.assertEqual(result, 'do VENDEDOR')

    def test_pair_without_separator_returns_whole_text(self):
        result = self.render_gender('feminine', 'VENDEDOR')
        self.assertEqual(result, 'VENDEDOR')

    def test_empty_feminine_side_falls_back_to_masculine(self):
        result = self.render_gender('feminine', 'VENDEDOR|')
        self.assertEqual(result, 'VENDEDOR')

    def test_surrounding_spaces_are_trimmed(self):
        result = self.render_gender('feminine', ' do VENDEDOR | da VENDEDORA ')
        self.assertEqual(result, 'da VENDEDORA')


class GenderNormalizationTests(SimpleTestCase):
    def test_feminine_is_kept(self):
        self.assertEqual(ContractPdfView._normalize_gender('feminine'), 'feminine')

    def test_masculine_is_kept(self):
        self.assertEqual(ContractPdfView._normalize_gender('masculine'), 'masculine')

    def test_missing_value_defaults_to_masculine(self):
        self.assertEqual(ContractPdfView._normalize_gender(None), 'masculine')

    def test_invalid_value_defaults_to_masculine(self):
        self.assertEqual(ContractPdfView._normalize_gender('other'), 'masculine')
