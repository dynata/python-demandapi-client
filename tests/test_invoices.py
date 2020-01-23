# encoding: utf-8
from __future__ import unicode_literals, print_function

import unittest
import responses

from dynatademand.api import DemandAPIClient

BASE_HOST = "http://test-url.example"


class TestInvoiceEndpoints(unittest.TestCase):
    def setUp(self):
        self.api = DemandAPIClient(client_id='test', username='testuser', password='testpass', base_host=BASE_HOST)
        self.api._access_token = 'Bearer testtoken'

    @responses.activate
    def test_get_invoice(self):
        with open('./tests/test_files/get_invoice.pdf', 'rb') as invoice_file:
            responses.add(
                responses.GET,
                '{}/sample/v1/projects/1337/invoices'.format(BASE_HOST),
                body=invoice_file.read(),
                content_type='application/pdf',
                stream=True,
                status=200)
        self.api.get_invoice(1337)
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(responses.calls[0].response.headers['content-type'], 'application/pdf')

    @responses.activate
    def test_get_invoices_summary(self):
        with open('./tests/test_files/get_invoices_summary.pdf', 'rb') as summary_file:
            responses.add(
                responses.GET,
                '{}/sample/v1/projects/invoices/summary'.format(BASE_HOST),
                body=summary_file.read(),
                content_type='application/pdf',
                stream=True,
                status=200)

        self.api.get_invoices_summary(startDate='2019-06-12', endDate='2019-06-19', extProjectId='010528ef-8984-48c1-a06d-4dae730da027')
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(responses.calls[0].response.headers['content-type'], 'application/pdf')
