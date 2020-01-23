# encoding: utf-8

import json
import unittest
import responses
from dynatademand.api import DemandAPIClient

BASE_HOST = "http://test-url.example"

START_DATE = '2019-06-12'
END_DATE = '2019-06-19'
EXT_PROJECT_ID = '010528ef-8984-48c1-a06d-4dae730da027'

class TestInvoicesSummaryEndpoints(unittest.TestCase):
    def setUp(self):
        self.api = DemandAPIClient(client_id='test', username='testuser', password='testpass', base_host=BASE_HOST)
        self.api._access_token = 'Bearer testtoken'

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

        self.api.get_invoices_summary(startDate=START_DATE, endDate=END_DATE, extProjectId=EXT_PROJECT_ID)
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(responses.calls[0].response.headers['content-type'], 'application/pdf')
