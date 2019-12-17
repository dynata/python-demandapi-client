# encoding: utf-8
from __future__ import unicode_literals, print_function

import json
import unittest
import responses

try:
    from unittest.mock import patch
except ImportError:
    from mock import patch

from dynatademand.api import DemandAPIClient

BASE_HOST = "http://test-url.example"


class TestProjectEndpoints(unittest.TestCase):
    def setUp(self):
        self.api = DemandAPIClient(client_id='test', username='testuser', password='testpass', base_host=BASE_HOST)
        self.api._access_token = 'Bearer testtoken'

    @responses.activate
    def test_get_countries(self):
        with open('./tests/test_files/get_countries.json', 'r') as countries_file:
            countries_json = json.load(countries_file)
        responses.add(responses.GET, '{}/sample/v1/countries'.format(BASE_HOST), json=countries_json, status=200)
        self.api.get_countries()
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(responses.calls[0].response.json(), countries_json)
