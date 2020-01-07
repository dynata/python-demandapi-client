# encoding: utf-8
from __future__ import unicode_literals, print_function

import json
import unittest
import responses

from dynatademand.api import DemandAPIClient

BASE_HOST = "http://test-url.example"


class TestAttributeEndpoints(unittest.TestCase):
    def setUp(self):
        self.api = DemandAPIClient(client_id='test', username='testuser', password='testpass', base_host=BASE_HOST)
        self.api._access_token = 'Bearer testtoken'

    @responses.activate
    def test_get_attributes(self):
        with open('./tests/test_files/get_attributes.json', 'r') as attributes_file:
            attributes_json = json.load(attributes_file)
        responses.add(responses.GET, '{}/sample/v1/attributes/no/no'.format(BASE_HOST), json=attributes_json, status=200)
        self.api.get_attributes('no', 'no')
        self.assertEqual(len(responses.calls), 1)
        print('flaws')
        print(responses.calls[0].response.json())
        self.assertEqual(responses.calls[0].response.json(), attributes_json)
