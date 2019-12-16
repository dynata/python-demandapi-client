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


class TestSourceEndpoints(unittest.TestCase):
    def setUp(self):
        self.api = DemandAPIClient(client_id='test', username='testuser', password='testpass', base_host=BASE_HOST)
        self.api._access_token = 'Bearer testtoken'

    @responses.activate
    def test_get_sources(self):
        with open('./tests/test_files/get_sources.json', 'r') as sources_file:
            sources_json = json.load(sources_file)
        responses.add(responses.GET, '{}/sample/v1/sources'.format(BASE_HOST), json=sources_json, status=200)
        self.api.get_sources()
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(responses.calls[0].response.json(), sources_json)
